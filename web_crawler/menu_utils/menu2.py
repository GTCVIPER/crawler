import os.path

from terminal_layout.extensions.choice import *
from terminal_layout import *
import webbrowser
import sys
import shutil
from menu3 import input_dest

sys.path.append('/pythonProject3/web_crawler/')
from proj_path import *
from utils import *




# C:/Users/52252/Desktop
def display_content(true_path, browser_path):
    c = Choice('资源展示',
               ['网页展示', '源码展示', '文件批注', '查看批注', '备份批注', '退出'],
               icon_style=StringStyle(fore=Fore.blue),
               selected_style=StringStyle(fore=Fore.blue))

    choice_ = c.get_choice()
    # origin_name = true_path.rsplit('/')[-1]
    origin_name = os.path.basename(true_path)
    file_name = origin_name.replace('.', '_') + '.txt'
    file_p = path_ + '/comments' + true_path.rsplit('uploads')[-1].replace(origin_name, file_name)
    # re_num = input_2()

    if choice_:
        _, value = choice_
        if value == '网页展示':
            web_display(true_path, browser_path)
            display_content(true_path, browser_path)
        elif value == '源码展示':
            stdio_display(true_path)
            display_content(true_path, browser_path)
        elif value == '文件批注':
            text = ''
            print('\n', Fore.ex_cyan_2, '[!] 正在对', true_path, '做批注。。。', Fore.reset, '\n')
            print('\n', Fore.ex_cyan_2, '[!] 请输入批注内容 (单独输入 :wq 结束输入)', Fore.reset, '\n')
            while True:
                line = input()
                text += line + '\n'
                if line == ':wq':
                    break
            write_comment(origin_name, file_p, true_path, text)
            display_content(true_path, browser_path)
        elif value == '查看批注':
            if os.path.isfile(file_p):
                comm_display(file_p)
            else:
                print('\n', Fore.red, '[-] 该文件目前还没有批注！ ', Fore.reset, '\n')
            display_content(true_path, browser_path)
        elif value == '备份批注':
            bak_comment(file_p, file_name)
            display_content(true_path, browser_path)


def display_list(show_list, browser_path):
    show_li = []
    for ele_dict in show_list:
        show_li.append(ele_dict['show_path'])
    # print(show_li)

    c = Choice('文件列表',
               show_li,
               icon_style=StringStyle(fore=Fore.blue),
               selected_style=StringStyle(fore=Fore.blue))

    choice_ = c.get_choice()

    if choice_:
        _, value = choice_

        # 列表推导式
        # print([x['true_path'] for x in show_list if x['show_path'] == value][0])
        true_path = [x['true_path'] for x in show_list if x['show_path'] == value][0]

        # charset = [x['charset'] for x in files_dists if x['file'] == true_path][0]
        display_content(true_path, browser_path)


def web_display(true_path, browser_path):
    # print(true_path)
    webbrowser.register('browser', None, webbrowser.BackgroundBrowser(browser_path))
    is_success = webbrowser.get('browser').open('file://' + true_path)
    # print(browser_path, is_success, sep='--->')
    if is_success:
        print('\n', Fore.blue, '[+] 成功打开浏览器 ......', Fore.reset, '\n')
    else:
        print('\n', Fore.red, '[-] 请输入正确的浏览器路径！ (请将路径用/分割) ', Fore.reset, '\n')


def stdio_display(true_path):
    if true_path.rsplit('.')[-1] not in ['png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'ico', 'docx', 'ppt',
                                         'pptx']:
        with open(true_path, 'r', encoding='utf-8') as f:
            print(f.read())
    else:
        with open(true_path, 'rb') as f:
            print(f.read())

def comm_display(true_path):
    with open(true_path, 'r') as f:
        print(f.read())



def write_comment(origin_name, file_name, true_path, text):
    # print(true_path)
    root_p = file_name[0:file_name.rfind('/')]

    if not os.path.exists(root_p):
        os.makedirs(root_p)

    with open(file_name, 'a', encoding='UTF-8') as f:
        f.writelines(f'对 {origin_name} 的批注 ------------------------------- {getCurrentTime()}\n')
        f.writelines(f'-----=={true_path}==-----\n\n')
        f.write(text)


def bak_comment(comm_path, file_name):
    if os.path.exists(comm_path):
        dest_path = input_dest()
        # print(dest_path)

        file_name = getCurrentTimes() + '_' + file_name

        target_file_path = os.path.join(dest_path, file_name)

        # 备份文件
        try:
            shutil.move(comm_path, target_file_path)
            print('\n', Fore.green, '[+] 文件备份成功！！！ ', Fore.reset, '\n')
        except:
            print('\n', Fore.red, '[-] 文件备份失败！！！ ', Fore.reset, '\n')
    else:
        print('\n', Fore.red, '[-] 没有批注文件！！！ ', Fore.reset, '\n')

    # print(comm_path, file_name)
