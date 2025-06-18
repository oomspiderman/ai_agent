# from functions.get_file_content import get_file_content
# from functions.get_files_info import get_files_info
# from functions.run_python_file import run_python_file
# from functions.write_file_content import write_file

from google.genai import types 

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file_content import schema_write_file

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file_content import write_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

def call_function(function_call_part, verbose=False):

    if verbose: 
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else: 
        print(f" - Calling function: {function_call_part.name}")

    function_call_args = function_call_part.args.copy()
    needs_working_dir = {"get_file_content", "get_files_info", "write_file", "run_python_file"}
    if function_call_part.name in needs_working_dir:
        function_call_args["working_directory"] = "./calculator"

    functions = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    if function_call_part.name not in functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ], 
        )
    
    try: 
        function_response = functions[function_call_part.name](**function_call_args)
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Error in function '{function_call_part.name}': {str(e)}"},
                )
            ], 
        )           
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_response},
            )
        ],
    )