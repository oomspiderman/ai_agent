import os

def get_file_content(working_directory, file_path):
  
    file_content_string = ""

    try:
        abs_file_path = os.path.join(os.path.abspath(working_directory),file_path)  
    except Exception as e:
        return f"Error: not found or is not a regular file"    

    try:
        if not abs_file_path.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    except Exception as e:
        return f"Error: not found or is not a regular file"    
    
    try:
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"' 
    except Exception as e:
        return f'Error: File not found or is not a regular file: "{file_path}"'

    MAX_CHARS = 10000
    try: 
        with open(abs_file_path, "r") as f:
            print(f"Opening {abs_file_path}...")
            file_content_string = f.read(MAX_CHARS)
    except Exception as e:
        return f"Error: Could not open file - {e}"

    if len(file_content_string) == MAX_CHARS:
        file_content_string = file_content_string + f'[...File "{file_path}" truncated at 10000 characters]'

    return file_content_string