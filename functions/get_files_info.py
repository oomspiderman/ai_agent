import os

def get_files_info(working_directory, directory=None):
    
    try:
        abs_path_target_dir  = os.path.abspath(directory)
        abs_path_work_dir    = os.path.abspath(working_directory)
    except Exception as e:
        print("Error: Invalid path input")
        return f"Error: Invalid path input - {e}"

    if not abs_path_target_dir.startswith(abs_path_work_dir):
        print(f"Abs target:  {abs_path_target_dir}")
        print(f"Abs working: {abs_path_work_dir}")
        print("Error: outside the permitted working directory")
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    try:
        if not os.path.isdir(directory):
            print("Error: Not a directory")
            return f'Error: "{directory}" is not a directory'        
        dir_content = os.listdir(directory)
    except Exception as e:
        print("Error: Could not list directory")
        return f"Error: Could not list directory - {e}"

    lines = []

    for item in dir_content: 
        file_name = item
        try:
            file_size_in_bytes = os.path.getsize(os.path.join(abs_path_target_dir,item))
            is_directory       = os.path.isdir(os.path.join(abs_path_target_dir,item))
        except Exception as e:
            # lines.append(f"Error: error reading file info - {e}")
            continue        
        
        lines.append(f"- {file_name}: file_size={file_size_in_bytes} bytes, is_dir={is_directory}")
    
    return "\n".join(lines)