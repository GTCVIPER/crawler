from terminal_layout.extensions.choice import *
from terminal_layout import *
import webbrowser


# from selenium import webdriver


def display_content(true_path, browser_path):
    c = Choice('资源展示',
               ['网页展示', '源码展示', '文件批注', '退出'],
               icon_style=StringStyle(fore=Fore.blue),
               selected_style=StringStyle(fore=Fore.blue))

    choice_ = c.get_choice()

    if choice_:
        _, value = choice_
        if value == '网页展示':
            web_display(true_path, browser_path)
            display_content(true_path, browser_path)
        elif value == '源码展示':
            stdio_display(true_path)
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
        display_content([x['true_path'] for x in show_list if x['show_path'] == value][0], browser_path)


def web_display(true_path, browser_path):
    # print(true_path)
    webbrowser.register('browser', None, webbrowser.BackgroundBrowser(browser_path))
    is_success = webbrowser.get('browser').open('file://' + true_path)
    # print(browser_path, is_success, sep='--->')
    if is_success:
        print('\n', Fore.blue, '[+] 成功打开浏览器 ......', Fore.reset, '\n')
    else:
        print('\n', Fore.red, '[-] 浏览器开启失败！ (请将路径用/分割) ', Fore.reset, '\n')


def stdio_display(true_path):
    with open(true_path, 'r', encoding='UTF-8') as f:
        print(f.read())
