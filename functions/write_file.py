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
    description="Writes text content to a specified file within the working directory (overwriting if the file exists)",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="ath to the file to write, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text content to write to the file",
            ),
        },
    ),
)
