import os
import json
from pathlib import Path

from .環境 import 配置

from .Librian虛擬機 import 虛擬機環境
from .Librian虛擬機 import 劇本

此處 = os.path.dirname(os.path.abspath(__file__))

def 生成虛擬核心():
    讀者 = 劇本.讀者(f'{虛擬機環境.工程路徑}/{虛擬機環境.劇本入口}')

    圖片文件夾 = os.path.join(f'../../{虛擬機環境.工程路徑}', 虛擬機環境.圖片文件夾).replace('\\', '/')
    音樂文件夾 = os.path.join(f'../../{虛擬機環境.工程路徑}', 虛擬機環境.音樂文件夾).replace('\\', '/')
    視頻文件夾 = os.path.join(f'../../{虛擬機環境.工程路徑}', 虛擬機環境.視頻文件夾).replace('\\', '/')
    臨時立繪文件夾 = os.path.join(f'../../{虛擬機環境.工程路徑}', 虛擬機環境.臨時立繪文件夾).replace('\\', '/')
    自定css = [os.path.join(f'../../{虛擬機環境.工程路徑}', i).replace('\\', '/') for i in 虛擬機環境.自定css]
    
    主題css = os.path.join(f'主題', 虛擬機環境.主題css + '.css').replace('\\', '/')
    
    演出步 = list(讀者.迭代器())

    with open(Path(此處) / '前端/虛擬核心.js', 'w', encoding='utf-8') as f:
        虛擬核心 = {
            '作品名': 虛擬機環境.標題,
            '解析度': 虛擬機環境.主解析度,
            '邊界': int(配置["顯示繪圖邊界"]),
            '圖片文件夾': 圖片文件夾,
            '音樂文件夾': 音樂文件夾,
            '視頻文件夾': 視頻文件夾,
            '臨時立繪文件夾': 臨時立繪文件夾,
            '自定css': 自定css,
            '主題css': 主題css,
            '演出步': 演出步
        }
        json數據 = json.dumps(虛擬核心, indent=2, ensure_ascii=False)
        f.write(f'window.虛擬核心 = {json數據}')
