import os
import sys

from terminal_layout.extensions.choice import *
from terminal_layout import *
from input import input_
from zip_bak import target_choice

c = Choice('网站爬取和管理系统',
           ['爬取网站', '资源管理', '资源备份', '退出'],
           icon_style=StringStyle(fore=Fore.blue),
           selected_style=StringStyle(fore=Fore.blue))
#
key_listener = KeyListener()
#
choice = c.get_choice()
if choice:
    _, value = choice
    if value == '爬取网站':
        os.system('python menu1.py')
        os.system('python menu.py')
        key_listener.stop()
    elif value == '资源管理':
        # os.system('python input.py')
        input_()
        os.system('python menu.py')
        key_listener.stop()
    elif value == '资源备份':
        target_choice()
        os.system('python menu.py')
        key_listener.stop()
    elif value == '退出':
        key_listener.stop()
        sys.exit()
