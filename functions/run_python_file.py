import os
import subprocess


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
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        command = ["python", abs_tgt_path]
        command.extend(args)

        result = subprocess.run(
            command, cwd=abs_wkdir_path, capture_output=True, text=True, timeout=30
        )
        output = ""

        if result.returncode != 0:
            output += "Process exited with code X/n"
        if result.stderr is None or result.stdout is None:
            output += "No output produced/n"

        output += f"STDOUT: {result.stdout} STDERR: {result.stderr}"

        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"
