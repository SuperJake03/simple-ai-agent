import os

"""
    Work here for lesson
"""


def get_files_info(working_directory, directory="."):
    try:
        tgt_path = os.path.join(working_directory, directory)
        absolute_tgt_path = os.path.abspath(tgt_path)
        absolute_path_work_dir = os.path.abspath(working_directory)
        if (
            not absolute_tgt_path.startswith(absolute_path_work_dir + os.path.sep)
            and absolute_tgt_path != absolute_path_work_dir
        ):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(tgt_path):
            return f'Error: "{directory}" is not a directory'

        contents = os.listdir(tgt_path)
        str_list = []
        for content in contents:
            file_path = os.path.join(tgt_path, content)
            file_size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
            info_str = f"- {content}: file_size={file_size} bytes, is_dir={is_dir}"
            str_list.append(info_str)

        return "\n".join(str_list)
    except Exception as e:
        return f"Error: {e}"
