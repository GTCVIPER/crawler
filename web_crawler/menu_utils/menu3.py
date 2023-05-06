from terminal_layout import *
from terminal_layout.extensions.input import *


def input_dest():
    ctl = LayoutCtl.quick(TableRow,
                          [TextView('', '输入备份目标地址的绝对路径: (请将路径用/分割) ', fore=Fore.magenta),
                           TextView('input', '', width=11, fore=Fore.blue)])
    # auto_re_draw=False 这样就不会重新加载字幕了
    ctl.draw(auto_re_draw=False)
    ok, s = InputEx(ctl).get_input('input')
    if ok:
        return s
