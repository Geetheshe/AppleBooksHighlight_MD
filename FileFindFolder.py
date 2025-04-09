from pathlib import Path


def find_file(folder_path, file_name):
    # 在指定文件夹及其子文件夹中查找指定文件
    root_path = Path(folder_path)
    for file in root_path.rglob(file_name):  # 递归搜索
        return file.resolve()  # 返回文件的绝对路径
    return None
