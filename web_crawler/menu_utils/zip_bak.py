import os
import sys
import zipfile

from terminal_layout.extensions.choice import *
from terminal_layout import *
from menu3 import input_dest
from filesearch import get_file_paths

sys.path.append('/pythonProject3/web_crawler/')
from proj_path import path_
from utils import getCurrentTimes

upload_root_p = path_ + '/uploads'


def target_choice():
    if os.path.exists(upload_root_p) and len(os.listdir(upload_root_p)) > 0:
        show_baks = os.listdir(upload_root_p)
        c = Choice('资源备份 (zip) 文件 (按 q 键退出)',
                   show_baks,
                   icon_style=StringStyle(fore=Fore.blue),
                   selected_style=StringStyle(fore=Fore.blue))
        choice_ = c.get_choice()

        if choice_:
            _, value = choice_
            src_path = upload_root_p + '/' + value
            bak_file_name = getCurrentTimes() + '_' + value + '.zip'
            dest_path = input_dest()

            if os.path.exists(dest_path):
                # 创建备份文件的全路径
                bak_file_path = os.path.join(dest_path, bak_file_name)

                # 创建一个 zip 文件并打开它
                backup_zip = zipfile.ZipFile(bak_file_path, 'w')

                # 遍历指定目录下的所有文件和子目录，并将它们添加到备份文件中
                for bak in get_file_paths(src_path):
                    backup_zip.write(bak, bak[len(src_path):])

                # 关闭备份文件
                backup_zip.close()
                print('\n', Fore.green, '[+] 资源备份成功！', Fore.reset, '\n')
            else:
                print('\n', Fore.red, '[-] 目标路径不存在！', Fore.reset, '\n')
    else:
        print('\n', Fore.red, '[-] 请先爬取资源！', Fore.reset, '\n')
