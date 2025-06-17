import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types

verbose = True

# sys.argv
# The list of command line arguments passed to a Python script. 
# argv[0] is the script name (it is operating system dependent whether this is a full pathname or not). 
# If the command was executed using the -c command line option to the interpreter, argv[0] is set to the string '-c'. 
# If no script name was passed to the Python interpreter, argv[0] is the empty string.
# To loop over the standard input, or the list of files given on the command line, see the fileinput module.
# See also sys.orig_argv.
# Note On Unix, command line arguments are passed by bytes from OS. Python decodes them with filesystem encoding and 
# “surrogateescape” error handler. When you need original bytes, you can get it by [os.fsencode(arg) for arg in sys.argv].

if len(sys.argv) > 2:
    if sys.argv[2] == "--verbose":
        verbose = True

if len(sys.argv) < 2:
    print("Error: prompt is required.")
    sys.exit(1)
else:
    user_prompt = sys.argv[1]

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

model_name = 'gemini-2.0-flash-001'

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
    description="Read file contents",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file of which the contents is to be inspected",
            ),
        },
    ),
)
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute Python files with optional arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to be executed",
            ),
        },
    ),
)
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite files",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to be written or overwritten",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to be written to the file",
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

response = client.models.generate_content(
    model=model_name,  
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    )
)

if verbose: 
    print(f"User prompt: {user_prompt}")    
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if response.function_calls is None:
    print(f'{response.text}')
else:
    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        