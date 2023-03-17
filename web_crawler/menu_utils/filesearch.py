import os
# from web_crawler.proj_path import path_


def get_file_paths(directory):
    """
    递归遍历目录并返回每个文件的路径
    """
    # global root
    file_paths = []  # 存储每个文件的路径
    for root, directories, files in os.walk(directory):
        # print(root, directories, files, sep='---->')
        for filename in files:
            # 获取文件的绝对路径
            file_path = os.path.join(root, filename)
            file_path = file_path.replace('\\', '/')
            file_paths.append(file_path)
    return file_paths


# if __name__ == '__main__':
#     # print(path_)
#     get_file_paths(path_ + '/uploads')
