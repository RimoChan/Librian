import os
import json
import shutil
from pathlib import Path

from .環境 import 配置

from librian.librian_util import 路徑

from .librian虛擬機 import 虛擬機環境
from .librian虛擬機 import 讀者



def 演出固化(劇本文件):
    讀者實例 = 讀者.讀者(劇本文件)
    演出步 = list(讀者實例.迭代器())
    return 演出步


def 生成虛擬核心():
    圖片文件夾 = 路徑.虛擬相對前端路徑(虛擬機環境.圖片文件夾)
    音樂文件夾 = 路徑.虛擬相對前端路徑(虛擬機環境.音樂文件夾)
    視頻文件夾 = 路徑.虛擬相對前端路徑(虛擬機環境.視頻文件夾)
    psd立繪路徑 = 路徑.虛擬相對前端路徑(os.path.relpath(虛擬機環境.psd立繪路徑, start=虛擬機環境.工程路徑))
    自定css = [路徑.虛擬相對前端路徑(i) for i in 虛擬機環境.自定css]
    主題css = os.path.join('主題', 虛擬機環境.主題css + '.css').replace('\\', '/')

    演出步 = 演出固化(f'{虛擬機環境.工程路徑}/{虛擬機環境.劇本入口}')

    虛擬核心 = {
        '作品名': 虛擬機環境.標題,
        '解析度': 虛擬機環境.主解析度,
        '邊界': int(配置["顯示繪圖邊界"]),
        '圖片文件夾': 圖片文件夾,
        '音樂文件夾': 音樂文件夾,
        '視頻文件夾': 視頻文件夾,
        'psd立繪路徑': psd立繪路徑,
        '自定css': 自定css,
        '主題css': 主題css,
        '演出步': 演出步
    }
    json數據 = json.dumps(虛擬核心, indent=2, ensure_ascii=False)
    return f'window.虛擬核心 = {json數據}'


def 幻象化(目標路徑):
    目標路徑 = Path(目標路徑)
    依賴 = [
        '黑科技',
        'librian/librian本體/前端/dist',
        'librian/librian本體/前端/素材',
        'librian/librian本體/前端/主題',
        'librian/librian本體/前端/adv.html',
        虛擬機環境.工程路徑.relative_to(路徑.librian外層),
    ]
    for i in 依賴:
        源路徑 = 路徑.librian外層 / i
        if 源路徑.is_dir():
            shutil.copytree(源路徑, 目標路徑 / i)
        elif 源路徑.is_file():
            shutil.copy(源路徑, 目標路徑 / i)
        else:
            raise Exception('哈？')

    with open(目標路徑 / 'librian/librian本體/前端/虛擬核心.js', 'w', encoding='utf-8') as f:
        f.write(生成虛擬核心())

    with open(目標路徑 / '說明.txt', 'w', encoding='utf-8') as f:
        f.write('因爲它有一些奇怪的操作所以不能直接拉進瀏覽器運行。\n你需要自建服務器，一個可行的方法是安裝http-server，在這個路徑啓動。然後「http://localhost:8080/librian/librian本體/前端/adv.html」。')
