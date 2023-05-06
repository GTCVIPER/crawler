import sys

from terminal_layout import *
from terminal_layout.extensions.input import *
from filesearch import get_file_paths
from menu2 import display_list

sys.path.append('/pythonProject3/web_crawler/')
from proj_path import path_


def input_():
    ctl = LayoutCtl.quick(TableRow,
                          [TextView('', '输入查询路径: (Press Enter to show ALL, Press q to quit)', fore=Fore.magenta),
                           TextView('input', '', width=11, fore=Fore.blue)])

    # auto_re_draw=False 这样就不会重新加载字幕了
    ctl.draw(auto_re_draw=False)
    ok, s = InputEx(ctl).get_input('input')
    if ok:
        path_lists = get_file_paths(path_ + '/uploads')
        is_matched = False
        show_list = []
        s = 'uploads' if s == '' else s
        for pat in path_lists:
            # show_pat = '~/' + pat[pat.find('uploads'):-1]
            if s in pat:
                is_matched = True
                show_pat = '~/' + pat[pat.find(s):-1]
                # print(pat[pat.find(s):-1])
                show_list.append({'show_path': show_pat, 'true_path': pat})
        if not is_matched:
            # print('未搜到结果！！！')
            print('\n', Fore.red, '[-] 未搜到结果！！！ ', Fore.reset, '\n')
        else:
            # print(input_1())
            display_list(show_list, input_1())

    # menu2(path_lists)


def input_1():
    ctl = LayoutCtl.quick(TableRow,
                          [TextView('', '输入浏览器的绝对路径: (请将路径用/分割) ', fore=Fore.magenta),
                           TextView('input', '', width=11, fore=Fore.blue)])
    # auto_re_draw=False 这样就不会重新加载字幕了
    ctl.draw(auto_re_draw=False)
    ok, s = InputEx(ctl).get_input('input')
    if ok:
        return s
