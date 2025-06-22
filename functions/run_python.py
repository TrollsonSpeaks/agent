import os
import subprocess

def run_python_file(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_dir = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_dir.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_dir):
        return f'Error: File "{file_path}" not found.'
 
    if not abs_dir.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(
            ["python3", os.path.basename(abs_dir)],
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        output = ""
        if result.stdout:
            output += f"STDOUT:\n{result.stdout}"
        if result.stderr:
            if output:
                output += "\n"
            output += f"STDERR:\n{result.stderr}"
        if result.returncode != 0:
            if output:
                output += "\n"
            output += f"Process exited with code {result.returncode}"
        if not output:
            output = "No output produced."
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"
