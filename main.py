import sys
import os
from functions.call_function import call_function
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    if len(sys.argv) < 2:
        print("Error: no prompt provided.")
        sys.exit(1)
        
    user_prompt = sys.argv[1]

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )

    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Retrieves the content of the specified file, constrained to the working directory. If no file path is provided, a default behavior may be applied.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the file whose content should be retrieved, relative to the working directory. Optional.",
                ),
            },
        ),
    )

    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Executes the specified Python file, constrained to the working directory. If no file path is provided, a default behavior may be applied.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the Python file to be executed, relative to the working directory. Optional.",
                ),
            },
        ),
    )

    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Writes content to the specified file path, constrained to the working directory. If no file path or content is provided, a default behavior may be applied.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the file where content should be written, relative to the working directory. Optional.",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content to write to the file. Optional.",
                ),
            },
        ),
    )

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    for i in range(20):
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            )
        )
      
        prompt_token_count = response.usage_metadata.prompt_token_count
        candidates_token_count = response.usage_metadata.candidates_token_count
        is_verbose = '--verbose' in sys.argv
    
        if is_verbose:
            print(f'User prompt: {user_prompt}')
            print(f'Prompt tokens: {prompt_token_count}')
            print(f'Response tokens: {candidates_token_count}')
 
        function_calls_made = False
        for candidate in response.candidates:
            messages.append(candidate.content)
    
            for part in candidate.content.parts:
                print(f"Part type: {type(part)}")
                print(f"Part attributes: {dir(part)}")
                if hasattr(part, 'function_call') and part.function_call is not None:                
                    print(f"Has function_call: {part.function_call}")
                    print(f"Function call type: {type(part.function_call)}")
                    function_calls_made = True
                    function_call_result = call_function(part.function_call, is_verbose)
                    if not function_call_result.parts[0].function_response.response:
                        raise Exception("Function call result missing expected response")
                    if is_verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                    messages.append(function_call_result)
            
        if function_calls_made:
            continue
        else:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'text'):
                    print(part.text)
                    break
            break    

if __name__ == "__main__":
    main()
