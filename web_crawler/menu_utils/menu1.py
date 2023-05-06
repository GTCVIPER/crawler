import os
import sys
from terminal_layout import *
from terminal_layout.extensions.input import *
import re

sys.path.append('/pythonProject3/web_crawler/')
from proj_path import path_
from utils import *

title_style = {
    'width': 20,
    'gravity': Gravity.center,
    'fore': Fore.ex_dark_slate_gray_3,
    'back': Back.ex_dark_gray
}
table_color = {
    # 'fore': Fore.ex_dark_slate_gray_3,
    'back': Back.ex_deep_sky_blue_3a
}
ctl = LayoutCtl.quick(TableLayout,
                      [
                          # row_0:title
                          [TextView('step1', 'Step 1', **title_style),
                           TextView('step2', 'Step 2', **title_style),
                           TextView('step3', 'Step 3', **title_style)
                           ],
                          # row_1:tip
                          [TextView('tip1', '(your URL)', **title_style),
                           TextView('tip2', '(your PATH)', **title_style),
                           TextView('tip3', '(confirm)', **title_style)
                           ],
                          # row_2:line
                          [
                              TextView('', '-' * 60)
                          ],
                          # row_3:input
                          [TextView('', '    input: ', ),
                           TextView('input', '', )
                           ],
                          # row_4:empty
                          [
                              TextView('', ' ', ),
                          ],
                          # row_5:table-name
                          [TextView('', '    '),
                           TextView('', 'URL: ', width=7, gravity=Gravity.right, **table_color),
                           TextView('URL', '', width=50, gravity=Gravity.left, **table_color),
                           ],
                          # row_6:table-age
                          [TextView('', '    '),
                           TextView('', 'PATH: ', width=7, gravity=Gravity.right, **table_color),
                           TextView('PATH', '', width=50, gravity=Gravity.left, **table_color),
                           ],
                          # row_7:line
                          [
                              TextView('', '-' * 60)
                          ],
                          # row_8:help
                          [
                              TextView('', '(press enter to confirm)\t\t\t'),
                              TextView('', '(press backspace to quit)')
                          ],

                      ])


def change_step(last_i, new_i):
    for i, back in [[last_i, title_style['back']], [new_i, Back.ex_slate_blue_3b], ]:
        v = ctl.find_view_by_id('step' + str(i))
        if not v:
            continue
        v.set_back(back)
        v = ctl.find_view_by_id('tip' + str(i))
        v.set_back(back)


def clear_input():
    v = ctl.find_view_by_id('input')
    v.set_text('')


def get_data():
    step = 1
    data = {}
    for i, key in enumerate(['URL', 'PATH', ]):
        step += i
        clear_input()
        change_step(step - 1, step)
        ctl.re_draw()
        ok, v = InputEx(ctl).get_input('input')
        data[key] = v
    return data


def update_table(show_table, data):
    for id in ['root_row_3', 'root_row_4']:
        v = ctl.find_view_by_id(id)
        v.set_visibility(Visibility.gone if show_table else Visibility.visible)
    for id in ['root_row_5', 'root_row_6']:
        v = ctl.find_view_by_id(id)
        v.set_visibility(Visibility.visible if show_table else Visibility.gone)
        if id == 'root_row_5':
            v = ctl.find_view_by_id('URL')
            v.set_text(data.get('URL', ''))
        if id == 'root_row_6':
            v = ctl.find_view_by_id('PATH')
            v.set_text(data.get('PATH', ''))
    ctl.re_draw()


ctl.draw(auto_re_draw=False)
update_table(False, {})

data = get_data()
change_step(2, 3)
update_table(True, data)

kl = KeyListener()

# 防止远程 RCE 漏洞注入
pattern_1 = r'(&&|;|\||\|\|)'
pattern_2 = r'(&&|;|\||\|\||&)'

# data["URL"] == '' and data["PATH"] == '':
# print('\n', Fore.red, '[-] 请输入目标URL和包名！', Fore.reset, '\n')
@kl.bind_key(Key.ENTER)
def _(kl, e):
    if not data["URL"]  or not data["PATH"] or not is_url(data["URL"]):
        # print(data["URL"],data["PATH"] )
        print('\n', Fore.red, '[-] 请输入 正确的 目标URL和包名！', Fore.reset, '\n')
    elif not re.search(pattern_1, data['URL']) and not re.search(pattern_2, data["PATH"]):
        # print(path_)

        if not os.path.exists(path_ + '/logs'):
            os.makedirs(path_ + '/logs')

        if sys.platform == 'win32':
            os.system(
                f'start /B scrapy crawl gtc_spider -a url={data["URL"]} -a path={data["PATH"]} > {path_}/logs/{data["PATH"]}.log')
        else:
            os.system(
                f'scrapy crawl gtc_spider -a url={data["URL"]} -a path={data["PATH"]} > {path_}/logs/{data["PATH"]}.log &')
            print('\n', Fore.blue, '[+] Crawling ', data['URL'], '......', Fore.reset, '\n')

    else:
        print('\n', Fore.red, '[-] 禁止输入违规字符串！', Fore.reset, '\n')
    # os.system(f'whoami')
    kl.stop()


@kl.bind_key(Key.BACKSPACE)
def _(kl, e):
    kl.stop()


kl.listen()
