import os

from config import MAX_CHARS
from google.genai import types


def get_file_content(working_directory, file_path):
    try:
        tgt_path = os.path.join(working_directory, file_path)
        absolute_tgt_path = os.path.abspath(tgt_path)
        absolute_path_work_dir = os.path.abspath(working_directory)
        if (
            not absolute_tgt_path.startswith(absolute_path_work_dir + os.path.sep)
            and absolute_tgt_path != absolute_path_work_dir
        ):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(tgt_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(tgt_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)

            if os.path.getsize(tgt_path) > MAX_CHARS:
                file_content_string = (
                    file_content_string
                    + f'[...File "{file_path}" truncated at 10000 characters]'
                )

        return file_content_string

    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Prints out a files contents. Max characters printed is {MAX_CHARS}",
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
