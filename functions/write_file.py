import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrites an existing file or writes to a new file if ti doesn't exist (and creats required parent dirs safely), constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write.",
            ),
            "contents": types.Schema(
                type=types.Type.STRING,
                description="The contents to write to the file as a string.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_filepath = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not abs_filepath.startswith(abs_working_dir):
        return f"Error: {file_path} is not in the working dir"
    
    parent_dir = os.path.dirname(abs_filepath)
    if not os.path.isdir(parent_dir):
        try:
            os.makedirs(parent_dir)
        except Exception as e:
            return f"Could not create parent dirs: {parent_dir} = {e.args}"
    if not os.path.isfile(abs_filepath):
        # # parent_dir = os.path.dirname(abs_filepath)
        
        # try:
        #     os.makedirs(parent_dir)
        # except Exception as e:
        #     return f"Error: {file_path} is not a file"
        pass
    
    try:
        with open(abs_filepath, "w") as f:
            f.write(content)
        return f"Successfully wrote to '{file_path}' ({len(content)} characters)"
    except Exception as e:
        return f"Failed to write to file: {file_path}, {e.args}"