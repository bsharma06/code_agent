import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

load_dotenv()

def main():
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=gemini_api_key)
    
    if len(sys.argv) < 2:
        print("I need prompt!")
        sys.exit(1)

    verbose_flag = False
    if len(sys.argv) == 3 and sys.argv[2]=="--verbose":
        verbose_flag = True
    
    prompt = sys.argv[1]
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001", contents = messages
    )
    
    print(response.text)
    
    if response.usage_metadata == None:
        print("There is some problem with LLM response!")
        return None
    
    if verbose_flag:
        print(f"Input tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Output tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    # main()
    
    # print(get_files_info("calculator", "../"))

    print(get_file_content("calculator","pkg/calculator.py"))