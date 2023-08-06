import os
import re
import threading
import queue

import pyperclip

# pyperclip.copy("复制内容")  # 复制到剪切板
# print(pyperclip.paste())   # 从剪切板粘贴(获取内容),并打印
# pyperclip.waitForPaste()，当剪贴板上有非空字符串时，飞回字符串类型的值。
# pyperclip.waitForNewPaste()，当剪贴板上的文本改变时，传返回值。

# 音乐队列
song_queue = queue.Queue()


# 下载器
class DL(threading.Thread):

    def __init__(self):
        super().__init__()
        # 记录已下载的歌曲
        self._dl_song_list = []

    def run(self) -> None:
        while True:
            # 获取一首歌曲
            song = song_queue.get()

            # 判断是否已经下载
            if song in self._dl_song_list:
                print("已下载:", song)
            else:
                print("下载:", song)
                # 下载
                cmd = 'pyncm --no-overwrite "{}"'.format(song.strip())
                print(cmd)
                os.system(cmd)

                # 加入已下载列表
                self._dl_song_list.append(song)


def watch_clp():
    """
    监控剪切板
    """
    # 网易云音乐格式匹配
    _re_s = re.compile(r"^\s*https://music\.163\.com/song\?id=\d+&userid=\d+\s*$")

    while True:
        # 当剪贴板上的文本改变时
        current_clp = pyperclip.waitForNewPaste()

        # 判断是否是网易云音乐连接格式
        if _re_s.match(current_clp):
            # 加入到队列
            song_queue.put(current_clp)

            # 清空剪切板
            pyperclip.copy("")


def main():
    dl = DL()

    # 随主线程退出
    dl.setDaemon(True)

    # 开启下载线程
    dl.start()

    try:
        # 监控剪切板
        watch_clp()
    except KeyboardInterrupt as e:
        pass


if __name__ == "__main__":
    main()
