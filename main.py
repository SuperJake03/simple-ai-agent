import os
import sys

from dotenv import load_dotenv
from google import genai
from typing_extensions import final

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
    final_response = False
    for _ in range(20):
        final_response = generate_content(client, user_prompt, messages, args)
        if final_response:
            break
    if not final_response:
        sys.exit("No final response was produced!")


def generate_content(client, user_prompt, messages, args):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=genai.types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

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
        print("Final Response:")
        print(response.text)
        return True

    for function_call in response.function_calls:
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

    messages.append(genai.types.Content(role="user", parts=function_results))
    return False


if __name__ == "__main__":
    main()
