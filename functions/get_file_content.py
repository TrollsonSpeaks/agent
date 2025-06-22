import os

def get_file_content(working_directory, file_path):

    abs_working_dir = os.path.abspath(working_directory)
    abs_dir = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_dir.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_dir):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        MAX_CHARS = 10000

        with open(abs_dir, "r") as f:
            file_content_string = f.read(MAX_CHARS + 1)

        if len(file_content_string) > 10000:
            return file_content_string[:10000] + f'[...File "{file_path}" truncated at 10000 characters]'
        else:
            return file_content_string
        
    except Exception as e:
        return f'Error: {str(e)}'
