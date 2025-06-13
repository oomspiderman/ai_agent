import os

def write_file(working_directory, file_path, content):
    
    abs_file_path = os.path.join(os.path.abspath(working_directory),file_path)

    if not abs_file_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(os.path.dirname(abs_file_path)):
        print(f'NEED TO and trying to create {os.path.dirname(abs_file_path)}')
        os.makedirs(os.path.dirname(abs_file_path))

    try: 
        with open(abs_file_path, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error: Could not create {abs_file_path}"
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'