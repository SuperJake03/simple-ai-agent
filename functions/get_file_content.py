import os


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

        # Finish func here

    except Exception as e:
        return f"Error: {e}"
