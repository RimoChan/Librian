import logging

import wxcef
import 山彥
from 環境 import 配置

from Librian虛擬機.util import 文件
from Librian虛擬機 import 虛擬機環境


def app():

    if 配置['編寫模式']:
        url = './前端/adv.html'
    elif 虛擬機環境.標題畫面:
        url = f'{虛擬機環境.工程路徑}/{虛擬機環境.標題畫面}'
    else:
        url = './前端/默認標題畫面/標題.html'

    標題url = 文件.轉爲網址路徑(url)

    if 虛擬機環境.圖標:
        圖標 = f'{虛擬機環境.工程路徑}/{虛擬機環境.圖標}'
    else:
        圖標 = './資源/librian.ico'

    app, 瀏覽器 = wxcef.group(title=虛擬機環境.標題, url=標題url, icon=圖標, size=虛擬機環境.主解析度)
    山彥.綁定(app, 標題url=標題url)

    return app
