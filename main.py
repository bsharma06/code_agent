import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from call_function import call_function
from config import MAX_ITERS

load_dotenv()

def main():
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=gemini_api_key)
    
    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read the content of a file
        - Write to a file (create or update)
        - Run a Python file with optional arguments

        When the user asks about the code project - they are referring to the
        working directory. So, you should typically start by looking at the
        projects's files, and figuring out how to run the project and how to
        run it's tests. You'll always want to test the tests and the actual project
        to verify that behavior is working.

        All paths you provide should be relative to the working directory.
        You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

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

    available_function = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file
        ]
    )

    config = types.GenerateContentConfig(
        tools=[available_function], system_instruction=system_prompt
    )

    for i in range(0, MAX_ITERS):

        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents = messages,
            config= config
        )
        
        if response is None or response.usage_metadata == None:
            print("There is some problem with LLM response!")
            return None
        
        if verbose_flag:
            print(f"User prompt: {prompt}")
            print(f"Input tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Output tokens: {response.usage_metadata.candidates_token_count}")

        if response.candidates:
            for candidate in response.candidates:
                if candidate is None or candidate.content is None:
                    continue
                messages.append(candidate.content)

        if response.function_calls:
            # print(response.function_calls)
            for function_call_part in response.function_calls:
                # print(f"Calling function: {function_call_part.name}({function_call_part.args})")
                result = call_function(function_call_part, verbose_flag)
                # print(result)
                messages.append(
                    result
                )
        else:
            # Final agent text message
            print(response.text)
            return 

if __name__ == "__main__":
    main()