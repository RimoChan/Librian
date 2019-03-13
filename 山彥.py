import os
import json
import logging

import wx
from cefpython3 import cefpython as cef

import 讀txt
import 劇本
from 環境 import 配置, 工程路徑


def 綁定(app):
    讀者 = 劇本.讀者(f'{工程路徑}/{配置["劇本入口"]}')
    bindings = cef.JavascriptBindings()
    bindings.SetObject("山彥", 山彥改(app.frame, app.frame.browser, 讀者))
    app.frame.browser.SetJavascriptBindings(bindings)


class 山彥:
    def __init__(self,  窗口, 瀏覽器, 讀者):
        self.瀏覽器 = 瀏覽器
        self.窗口 = 窗口
        self.讀者 = 讀者

    def js(self, x):
        self.瀏覽器.ExecuteJavascript(x)

    def 更新(self):
        狀態 = self.讀者.狀態.導出()
        self.js(f'演出.改變演出狀態({json.dumps(狀態)})')

    def 選擇讀檔文件(self):
        with wx.FileDialog(self.窗口, '讀檔', wildcard='pickle 文件 (*.pkl)|*.pkl',
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            fileDialog.SetPath(f'{工程路徑}/存檔資料/')
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return None
            return fileDialog.GetPath()

    def 選擇存檔文件(self):
        with wx.FileDialog(self.窗口, '存檔', wildcard='pickle 文件 (*.pkl)|*.pkl',
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            fileDialog.SetPath(f'{工程路徑}/存檔資料/')
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return None
            return fileDialog.GetPath()

    def 步進(self):
        if 配置['編寫模式']:
            return
        self.讀者.步進()

    def 步進更新(self):
        self.步進()
        self.更新()

    def 初始化(self):
        圖片文件夾 = os.path.join(f'../{工程路徑}', 配置['圖片文件夾']).replace('\\', '/')
        音樂文件夾 = os.path.join(f'../{工程路徑}', 配置['音樂文件夾']).replace('\\', '/')
        視頻文件夾 = os.path.join(f'../{工程路徑}', 配置['視頻文件夾']).replace('\\', '/')
        自定css = os.path.join(f'../{工程路徑}', 配置['自定css']).replace('\\', '/')
        主題css = os.path.join(f'主題', 配置['主題css'] + '.css').replace('\\', '/')

        演出配置 = {
            '解析度': 配置['主解析度'],
            '邊界': 配置['顯示繪圖邊界'],
            '主題css': 主題css,
            '自定css': 自定css,
            '圖片文件夾': 圖片文件夾,
            '音樂文件夾': 音樂文件夾,
            '視頻文件夾': 視頻文件夾,
        }

        s = f'''
            演出.配置({json.dumps(演出配置)});
            演出.準備工作();
        '''

        try:
            with open(f'{工程路徑}/存檔資料/用戶設置.json', encoding='utf8') as f:
                s += f"設置.應用用戶設置('{f.read()}');"
        except:
            logging.warning('用戶設置加載失敗')

        self.js(s)
        if 配置['編寫模式']:
            self.更新終態()

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
        self.讀者.存檔(f'{工程路徑}/存檔資料/快速存檔.pkl')
        self.js('演出.提示("存檔好了。")')

    def 快速讀檔(self):
        self.讀者.讀檔(f'{工程路徑}/存檔資料/快速存檔.pkl')
        self.更新()

    def 從title讀檔(self):
        文件名, 文件類型 = self.選擇讀檔文件()
        if 文件名:
            self.讀者.讀檔(文件名)
            self.js('開始()')

    def 從劇本開始(self, 劇本):
        入口 = f'{工程路徑}/{配置["劇本入口"]}'
        self.讀者.__init__(f'{os.path.dirname(入口)}/{劇本}')
        self.js('開始();')

    def 退出(self):
        exit()

    def 回標題(self):
        self.讀者.__init__(f'{工程路徑}/{配置["劇本入口"]}')
        self.js(f'window.location.href="file:///{工程路徑}/{配置["標題畫面"]}"')

    def 切換全屏(self):
        主窗口.切換全屏()

    def 設置(self, 參數):
        with open(f'{工程路徑}/存檔資料/用戶設置.json', 'w', encoding='utf8') as f:
            f.write(參數)

    def 選(self, 參數):
        t = self.讀者.狀態.選項[int(參數)][1]
        self.讀者.狀態.選項 = ()
        t()
        logging.debug('選擇了「%s」。' % 參數)
        self.讀者.步進()
        self.更新()


class 山彥改(山彥):
    def __init__(self, *li, **d):
        super().__init__(*li, **d)
        if 配置['編寫模式']:
            import threading

            def 監視():
                原字 = ''
                while True:
                    with 讀txt.讀(f'{工程路徑}/{配置["劇本入口"]}') as f:
                        字 = f.read()
                        if 字 != 原字:
                            self.更新終態()
                            原字 = 字
            t = threading.Thread(target=監視)
            t.setDaemon(True)
            t.start()

    def 更新終態(self):
        self.讀者.從一而終(f'{工程路徑}/{配置["劇本入口"]}')
        self.更新()
