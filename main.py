import os
from dotenv import load_dotenv
from google import genai

load_dotenv()



def main():
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=gemini_api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", contents="Why is the sky blue?"
    )
    print(response.text)


if __name__ == "__main__":
    main()
