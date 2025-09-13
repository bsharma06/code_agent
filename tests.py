from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def main():
    working_dir = "calculator"

    # print(write_file(working_dir, "pkg2/lorem.txt", "This is new file content"))
    print(run_python_file(working_dir, "main.py", ["3 + 5"]))

if __name__ == "__main__":
    main()