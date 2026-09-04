import os
import tempfile

from librian.librian_util import 文件
from librian.librian_util import 路徑

from . import 山彥
from .環境 import 配置

from .librian虛擬機 import 虛擬機環境


def 啓動app():
    if 配置['編寫模式'] or 配置['跳過標題畫面'] or 配置['監聽模式']:
        url = 路徑.librian本體 / '前端/adv.html'
    elif 虛擬機環境.標題畫面:
        url = f'{虛擬機環境.工程路徑}/{虛擬機環境.標題畫面}'
    else:
        url = 路徑.librian本體 / '前端/默認標題畫面/標題.html'

    標題url = 文件.轉爲網址路徑(url)

    if 虛擬機環境.圖標:
        圖標 = f'{虛擬機環境.工程路徑}/{虛擬機環境.圖標}'
    else:
        圖標 = 路徑.librian本體 / '資源/librian.ico'

    from .webview窗口 import 創建窗口

    cache_path = os.path.join(tempfile.gettempdir(), 'librian_webview')
    os.makedirs(cache_path, exist_ok=True)

    app = 創建窗口(
        title=虛擬機環境.標題,
        url=標題url,
        icon=圖標,
        size=虛擬機環境.主解析度,
        storage_path=cache_path,
    )
    山彥.綁定(app, 標題url=標題url)

    return app
