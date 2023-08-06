import os


def is_empty(directory_path):
    if not os.path.exists(directory_path):
        return False

    # 列出目录中的文件和子目录
    contents = os.listdir(directory_path)

    # 判断目录是否为空
    if len(contents) == 0:
        return True
    else:
        return False
