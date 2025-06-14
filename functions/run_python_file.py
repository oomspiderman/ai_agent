import os 
import subprocess

def run_python_file(working_directory, file_path):

    working_directory = os.path.abspath(working_directory)

    target_path = os.path.abspath(os.path.join(working_directory, file_path))

    # print(f'Working Directory = {working_directory}')

    if os.path.commonpath([working_directory, target_path]) != working_directory:
        return f'Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory'

    if not os.path.exists(target_path):
        return f'Error: File \"{file_path}\" not found.'

    if not target_path.endswith('.py'):
        return f'Error: \"{file_path}\" is not a Python file.'

    args = []
    args.append(f'python3')
    args.append(f'{file_path}')

    try: 
        result = subprocess.run(args,cwd=working_directory,timeout=30, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        return f"Error: executing Python file: {e}"

    stdout = result.stdout.decode()
    stderr = result.stderr.decode()
    exit_code = result.returncode

    result_string = []

    if stdout =='' and stderr =='':
        return "No output produced."

    result_string.append(f'STDOUT: {stdout}')
    result_string.append(f'STDERR: {stderr}')
    if exit_code != 0: 
        result_string.append(f'Process exited with code {exit_code}')
    
    return '\n'.join(result_string)