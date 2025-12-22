import os
import sys

from dotenv import load_dotenv
from google import genai

from call_function import available_functions
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

    if "--verbose" in args:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    print(response.text)


if __name__ == "__main__":
    main()
