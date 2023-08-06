import os
import re
import time

import pyperclip


def main():
    current_clipboard = pyperclip.paste()

    # 网易云音乐格式匹配
    _re_s = re.compile(r"^\s*https://music\.163\.com/song\?id=\d+&userid=\d+\s*$")

    while True:
        if pyperclip.paste() != current_clipboard:
            # 剪切板内容已变化
            current_clipboard = pyperclip.paste()
            print('剪贴板内容已更改:', current_clipboard)

            # 判断是否是网易云音乐连接格式
            if _re_s.match(current_clipboard):
                os.system('pyncm --no-overwrite "{}"'.format(current_clipboard.strip()))

            time.sleep(0.1)


if __name__ == "__main__":
    main()
