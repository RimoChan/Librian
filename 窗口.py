import logging
import os

import wxcef

from 環境 import 配置, 工程路徑
import 山彥
from Librian虛擬機.util import 文件


def app():

    if 配置['編寫模式']:
        url = './html/adv.html'
    elif 配置['標題畫面']:
        url = f'{工程路徑}/{配置["標題畫面"]}'
    else:
        url = './html/默認標題畫面/標題.html'

    標題url = 文件.轉爲網址路徑(url)

    if 配置['圖標']:
        圖標 = f'{工程路徑}/{配置["圖標"]}'
    else:
        圖標 = './資源/librian.ico'

    app, 瀏覽器 = wxcef.group(title=配置['標題'], url=標題url, icon=圖標, size=配置['主解析度'])
    山彥.綁定(app, 標題url=標題url)

    return app
