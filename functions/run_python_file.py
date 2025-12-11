import os


def run_python_file(working_directory, file_path, args=[]):
    try:
        tgt_path = os.path.join(working_directory, file_path)
        abs_tgt_path = os.path.abspath(tgt_path)
        abs_wkdir_path = os.path.abspath(working_directory)
        if (
            not abs_tgt_path.startswith(abs_wkdir_path + os.path.sep)
            and abs_tgt_path != abs_wkdir_path
        ):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(tgt_path):
            return f'Error: File "{file_path}" not found.'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        # continue function here for lesson
    except Exception as e:
        return f"Error: {e}"
