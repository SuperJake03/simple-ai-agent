import os
import sys
from dotenv import load_dotenv
from google import genai


def main():
    load_dotenv()

    args = sys.argv[1:]

    if not args:
        print("No prompt provided\n")
        print('Usage: python main.py "your prompt here"')
        sys.exit(1)
    prompt = " ".join(args)

    messages = [
        genai.types.Content(role="user", parts=[genai.types.Part(text=prompt)]),
    ]

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(response.text)


if __name__ == "__main__":
    main()
