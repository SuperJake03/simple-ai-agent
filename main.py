import os
import sys

from dotenv import load_dotenv
from google import genai

from call_function import available_functions, call_function
from prompts import system_prompt


def main():
    load_dotenv()

    args = sys.argv[1:]

    if not args:
        print("No prompt provided\n")
        print('Usage: python main.py "your prompt here" [--verbose]')
        sys.exit(1)
    user_prompt = args[0]

    messages = [
        genai.types.Content(role="user", parts=[genai.types.Part(text=user_prompt)]),
    ]

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=genai.types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if response.usage_metadata is None:
        raise RuntimeError("Error when getting a response")

    verbose = False
    if "--verbose" in args:
        verbose = True
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    function_results = []

    if response.function_calls is None:
        print(response.text)
    else:
        for function_call in response.function_calls:
            # print(f"Calling function: {function_call.name}({function_call.args})")
            function_call_result = call_function(function_call, verbose)
            if not function_call_result.parts:
                raise Exception("Function call result is empty")
            if function_call_result.parts[0].function_response is None:
                raise Exception("Function response is None")
            if function_call_result.parts[0].function_response.response is None:
                raise Exception("Response is None")
            function_results.append(function_call_result.parts[0])
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")


if __name__ == "__main__":
    main()
