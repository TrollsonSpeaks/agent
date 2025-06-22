import os
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file

def main():
    print(get_file_content({'file_path': 'main.py'}))
    print(write_file({'file_path': 'main.txt', 'content': 'hello'}))
    print(run_python_file({'file_path': 'main.py'}))
    print(get_files_info({'directory': 'pkg'}))

if __name__ == "__main__":
    main()
