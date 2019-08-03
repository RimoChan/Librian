import os
import json
import logging

import wx
from cefpython3 import cefpython as cef

from Librian虛擬機 import 劇本
from Librian虛擬機 import 虛擬機環境
from Librian虛擬機.util import 讀txt
from Librian虛擬機.util import 文件

from 帶有vue的山彥 import 帶有vue的山彥
from 環境 import 配置


def 綁定(app, 標題url):
    讀者 = 劇本.讀者(f'{虛擬機環境.工程路徑}/{虛擬機環境.劇本入口}')
    app.frame.set_browser_object("山彥", 極山彥(app.frame, app.frame.browser, 讀者, 標題url))


class 山彥(帶有vue的山彥):
    def __init__(self, 窗口, 瀏覽器, 讀者, 標題url):
        super().__init__(窗口)
        self.瀏覽器 = 瀏覽器
        self.讀者 = 讀者
        self.標題url = 標題url

    def js(self, x):
        self.瀏覽器.ExecuteJavascript(x)

    def 選擇讀檔文件(self):
        with wx.FileDialog(self.窗口, '讀檔', wildcard='pickle 文件 (*.pkl)|*.pkl',
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            fileDialog.SetPath(f'{虛擬機環境.工程路徑}/存檔資料/')
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return None
            return fileDialog.GetPath()

    def 選擇存檔文件(self):
        with wx.FileDialog(self.窗口, '存檔', wildcard='pickle 文件 (*.pkl)|*.pkl',
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            fileDialog.SetPath(f'{虛擬機環境.工程路徑}/存檔資料/')
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return None
            return fileDialog.GetPath()

    def 存檔(self):
        文件名 = self.選擇存檔文件()
        if 文件名:
            self.讀者.存檔(文件名)
            self.js('演出.提示("存檔好了。")')

    def 讀檔(self):
        文件名 = self.選擇讀檔文件()
        if 文件名:
            self.讀者.讀檔(文件名)
            self.更新()

    def 快速存檔(self):
        self.讀者.存檔(f'{虛擬機環境.工程路徑}/存檔資料/快速存檔.pkl')
        self.js('演出.提示("存檔好了。")')

    def 快速讀檔(self):
        self.讀者.讀檔(f'{虛擬機環境.工程路徑}/存檔資料/快速存檔.pkl')
        self.更新()

    def 退出(self):
        exit()

    def 切換全屏(self):
        self.窗口.toggleFullScreen()

    def vue更新(self, 內容):
        t = self.vue.用戶設置 if '用戶設置' in self.vue._內容 else None
        if t!=內容['用戶設置']:
            with open(f'{虛擬機環境.工程路徑}/存檔資料/用戶設置.json', 'w', encoding='utf8') as f:
                f.write(json.dumps(內容['用戶設置'], ensure_ascii=False))
        super().vue更新(內容)

class 演出山彥(山彥):
    def 回標題(self):
        self.讀者.__init__(f'{虛擬機環境.工程路徑}/{虛擬機環境.劇本入口}')
        self.js(f'window.location.href="{self.標題url}"')

    def 更新(self):
        狀態 = self.讀者.狀態.導出()
        self.js(f'演出.改變演出狀態({json.dumps(狀態)})')

    def 步進(self):
        if 配置['編寫模式']:
            return
        self.讀者.步進()

    def 步進更新(self):
        self.步進()
        self.更新()

    def 初始化(self):
        self.vue.圖片文件夾 = os.path.join(f'../{虛擬機環境.工程路徑}', 虛擬機環境.圖片文件夾).replace('\\', '/')
        self.vue.音樂文件夾 = os.path.join(f'../{虛擬機環境.工程路徑}', 虛擬機環境.音樂文件夾).replace('\\', '/')
        self.vue.視頻文件夾 = os.path.join(f'../{虛擬機環境.工程路徑}', 虛擬機環境.視頻文件夾).replace('\\', '/')
        self.vue.自定css = os.path.join(f'../{虛擬機環境.工程路徑}', 虛擬機環境.自定css).replace('\\', '/')
        self.vue.主題css = os.path.join(f'主題', 虛擬機環境.主題css + '.css').replace('\\', '/')
        self.vue.解析度 = 虛擬機環境.主解析度
        self.vue.邊界 = 配置['顯示繪圖邊界']

        if os.path.isfile(f'{虛擬機環境.工程路徑}/存檔資料/用戶設置.json'):
            try:
                with open(f'{虛擬機環境.工程路徑}/存檔資料/用戶設置.json', encoding='utf8') as f:
                    用戶設置 = json.loads(f.read())
                self.vue.用戶設置 = 用戶設置
            except Exception as e:
                logging.warning('用戶設置失效。')
            
        self.js('演出.準備工作()')

    def 選(self, 參數):
        t = self.讀者.狀態.選項[參數][1]
        self.讀者.狀態.選項 = ()
        t()
        logging.debug('選擇了「%s」。' % 參數)
        self.讀者.步進()
        self.更新()


class 帶標題山彥(演出山彥):
    def 開始(self):
        self.步進()
        self.js(f'window.location.href="{文件.轉爲網址路徑("./html/adv.html")}";')

    def 從title讀檔(self):
        文件名 = self.選擇讀檔文件()
        if 文件名:
            self.讀者.讀檔(文件名)
            self.js(f'window.location.href="{文件.轉爲網址路徑("./html/adv.html")}";')

    def 從劇本開始(self, 劇本):
        入口 = f'{工程路徑}/{配置["劇本入口"]}'
        self.讀者.__init__(f'{os.path.dirname(入口)}/{劇本}')
        self.js('開始();')


class 極山彥(帶標題山彥):
    def __init__(self, *li, **d):
        super().__init__(*li, **d)
        if 配置['編寫模式']:
            import threading

            def 監視():
                原字 = ''
                while True:
                    with 讀txt.讀(f'{虛擬機環境.工程路徑}/{虛擬機環境.劇本入口}') as f:
                        字 = f.read()
                        if 字 != 原字:
                            self.更新終態()
                            原字 = 字
            t = threading.Thread(target=監視)
            t.setDaemon(True)
            t.start()

    def 更新終態(self):
        self.讀者.從一而終(f'{虛擬機環境.工程路徑}/{虛擬機環境.劇本入口}')
        self.更新()

    def 初始化(self):
        super().初始化()
        if 配置['編寫模式']:
            self.更新終態()
