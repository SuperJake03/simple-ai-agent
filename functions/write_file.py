import os

from google.genai import types


def write_file(working_directory, file_path, content):
    try:
        tgt_path = os.path.join(working_directory, file_path)
        absolute_tgt_path = os.path.abspath(tgt_path)
        absolute_path_work_dir = os.path.abspath(working_directory)
        if (
            not absolute_tgt_path.startswith(absolute_path_work_dir + os.path.sep)
            and absolute_tgt_path != absolute_path_work_dir
        ):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        with open(tgt_path, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to a file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
