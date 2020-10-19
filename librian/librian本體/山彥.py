import os
import json
import time
import pickle
import logging
import datetime

import yaml
from rimo_utils import good_open
from rimo_utils.cef_tools.vue_ob import vue_ob

from librian.librian_util import 文件, 加載器, 路徑

from .librian虛擬機 import 讀者
from .librian虛擬機 import 虛擬機環境

from .環境 import 配置


def 綁定(app, 標題url):
    讀者實例 = 讀者.讀者(f'{虛擬機環境.工程路徑}/{虛擬機環境.劇本入口}')
    app.frame.set_browser_object("山彥", 極山彥(app.frame, app.frame.browser, 讀者實例, 標題url))


class 山彥(vue_ob):
    def __init__(self, 窗口, 瀏覽器, 讀者, 標題url):
        super().__init__()
        self.窗口 = 窗口
        self.瀏覽器 = 瀏覽器
        self.讀者 = 讀者
        self.標題url = 標題url

    def js(self, x):
        self.瀏覽器.ExecuteJavascript(x)

    def 取檔(self, callback):
        檔表 = os.listdir(f'{虛擬機環境.工程路徑}/存檔資料/手動存檔')
        檔表 = sorted(檔表, reverse=True)
        檔信息表 = []
        for i in 檔表:
            try:
                with open(f'{虛擬機環境.工程路徑}/存檔資料/手動存檔/{i}', 'rb') as f:
                    存檔信息 = pickle.load(f)['存檔信息']
                    檔信息表.append({
                        '名字': i,
                        '描述': 存檔信息['描述'],
                        '截圖': 存檔信息['截圖'],
                        '時間': datetime.datetime.fromtimestamp(存檔信息['存檔時間']).strftime('%Y-%m-%d %H:%M'),
                    })
            except Exception as e:
                logging.exception(e)
                logging.warning(f'存檔「{i}」有問題。')
        callback.Call(檔信息表)

    def 存檔(self, 文件名, 描述, 截圖):
        存檔信息 = {
            '描述': 描述,
            '截圖': 截圖,
            '存檔時間': time.time(),
        }
        self.讀者.存檔(f'{虛擬機環境.工程路徑}/存檔資料/手動存檔/{文件名}', 存檔信息)

    def 讀檔(self, 文件名):
        self.讀者.讀檔(f'{虛擬機環境.工程路徑}/存檔資料/手動存檔/{文件名}')
        self.更新(瞬間化=True)

    def 快速存檔(self):
        self.讀者.存檔(f'{虛擬機環境.工程路徑}/存檔資料/快速存檔.pkl')
        self.js('_py演出.提示("存檔好了。")')

    def 快速讀檔(self):
        self.讀者.讀檔(f'{虛擬機環境.工程路徑}/存檔資料/快速存檔.pkl')
        self.更新(瞬間化=True)

    def 切換全屏(self):
        self.窗口.toggleFullScreen()
        
    def 退出(self):
        exit()

    def vue更新(self, 內容):
        t = self.vue.用戶設置 if '用戶設置' in self.vue._內容 else None
        if t != 內容['用戶設置']:
            with open(f'{虛擬機環境.工程路徑}/存檔資料/用戶設置.yaml', 'w', encoding='utf8') as f:
                f.write(yaml.dump(內容['用戶設置']))
        super().vue更新(內容)


class 演出山彥(山彥):
    def 回標題(self):
        self.讀者.__init__(f'{虛擬機環境.工程路徑}/{虛擬機環境.劇本入口}')
        self.js(f'window.location.href={self.標題url.__repr__()}')

    def 步進(self):
        if 配置['編寫模式']:
            return
        self.讀者.步進()

    def 更新(self, 瞬間化=False):
        狀態 = self.讀者.狀態.導出()
        self.js(f'_py演出.改變演出狀態({json.dumps(狀態)},{json.dumps(瞬間化)})')

    def 狀態回調(self, 步進, callback):
        if 步進:
            self.步進()
        狀態 = self.讀者.狀態.導出()
        callback.Call(狀態)

    def 初始化(self, callback):
        self.vue.圖片文件夾 = 虛擬機環境.工程路徑 / 虛擬機環境.圖片文件夾
        self.vue.音樂文件夾 = 虛擬機環境.工程路徑 / 虛擬機環境.音樂文件夾
        self.vue.視頻文件夾 = 虛擬機環境.工程路徑 / 虛擬機環境.視頻文件夾
        self.vue.psd立繪路徑 = 虛擬機環境.psd立繪路徑
        self.vue.自定css = [虛擬機環境.工程路徑 / i for i in 虛擬機環境.自定css]
        self.vue.主題css = os.path.join('主題', 虛擬機環境.主題css + '.css').replace('\\', '/')
        self.vue.解析度 = 虛擬機環境.主解析度
        self.vue.邊界 = 配置['顯示繪圖邊界']
        self.vue.翻譯 = 虛擬機環境.翻譯

        用戶設置 = 加載器.yaml(f'{虛擬機環境.工程路徑}/存檔資料/用戶設置.yaml')
        if 用戶設置:
            self.vue.用戶設置 = 用戶設置
        callback.Call()

    def 選(self, 參數):
        t = self.讀者.狀態.選項[參數][1]
        self.讀者.狀態.選項 = []
        t()
        logging.debug(f'選擇了「{參數}」。')
        self.讀者.步進()
        self.更新()


class 帶標題山彥(演出山彥):
    def 開始(self):
        self.步進()
        self.js(f'window.location.href={文件.轉爲網址路徑(路徑.librian本體 / "前端/adv.html").__repr__()};')

    def 讀檔畫面(self):
        self.js(f'window.location.href={(文件.轉爲網址路徑(路徑.librian本體 / "./前端/adv.html")+"?入口=讀檔").__repr__()};')

    def 從劇本開始(self, 劇本):
        入口 = f'{虛擬機環境.工程路徑}/{虛擬機環境.劇本入口}'
        self.讀者.__init__(f'{os.path.dirname(入口)}/{劇本}')
        self.開始()


class 極山彥(帶標題山彥):
    def __init__(self, *li, **d):
        super().__init__(*li, **d)
        if 配置['編寫模式']:
            import threading
            
            def 監視():
                原字 = ''
                while True:
                    with good_open(f'{虛擬機環境.工程路徑}/{虛擬機環境.劇本入口}') as f:
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

    def 初始化(self, *li, **d):
        super().初始化(*li, **d)
        if 配置['編寫模式']:
            self.更新終態()
