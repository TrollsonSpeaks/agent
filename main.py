import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    if len(sys.argv) < 2:
        print("Error: no prompt provided.")
        sys.exit(1)
        
    user_prompt = sys.argv[1]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
    )

    prompt_token_count = response.usage_metadata.prompt_token_count
    candidates_token_count = response.usage_metadata.candidates_token_count
    is_verbose = '--verbose' in sys.argv

    print(response.text)
    if is_verbose:
        print(f'User prompt: {user_prompt}')
        print(f'Prompt tokens: {prompt_token_count}')
        print(f'Response tokens: {candidates_token_count}')

if __name__ == "__main__":
    main()
