import os

def get_files_info(working_directory, directory=None):

    abs_working_dir = os.path.abspath(working_directory)
    abs_dir = os.path.abspath(os.path.join(working_directory, directory))

    if not abs_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(abs_dir):
        return f'Error: "{directory}" is not a directory'

    try:
        info_lines = []
        for entry in os.listdir(abs_dir):
            full_path = os.path.join(abs_dir, entry)
            is_dir = os.path.isdir(full_path)
            size = os.path.getsize(full_path)
            line = f'- {entry}: file_size={size} bytes, is_dir={is_dir}'
            info_lines.append(line)
        return "\n".join(info_lines)
    except Exception as e:
        return f'Error: {str(e)}'
