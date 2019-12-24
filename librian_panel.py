import logging
import os
import subprocess
import shutil
from pathlib import Path

import wx
import yaml

from Librian本體 import wxcef
from Librian本體.帶有vue的山彥 import 帶有vue的山彥
from Librian本體.Librian虛擬機 import 虛擬機環境
from Librian本體.Librian虛擬機.util import 加載器


def js(x):
    真山彥.窗口.browser.ExecuteJavascript(x)


def alert(s):
    js(f'alert("{s}")')


class 山彥(帶有vue的山彥):
    def __init__(self, *li, **d):
        super().__init__(*li, **d)
        self.vue.存檔資料 = 加載器.yaml('./存檔資料/存檔資料.yaml')

    def vue更新(self, 內容):
        t = self.vue.用戶設置 if '用戶設置' in self.vue._內容 else None
        if t != 內容['存檔資料']:
            if not os.path.isdir('./存檔資料'):
                os.mkdir('./存檔資料')
            with open(f'./存檔資料/存檔資料.yaml', 'w', encoding='utf8') as f:
                f.write(yaml.dump(內容['存檔資料']))
        super().vue更新(內容)

    def 讀取工程信息(self, 工程路徑):
        虛擬機環境.加載配置(工程路徑)
        if 虛擬機環境.圖標:
            圖標路徑 = Path(工程路徑) / 虛擬機環境.圖標
        else:
            圖標路徑 = '../Librian本體/資源/librian.ico'
        主解析度 = 虛擬機環境.主解析度
        標題 = 虛擬機環境.標題
        self.vue.存檔資料 = [{'工程路徑': 工程路徑, '圖標路徑': 圖標路徑, '標題': 標題}] + \
            [工程信息 for 工程信息 in self.vue.存檔資料 if 工程信息['工程路徑'] != 工程路徑]
        return 圖標路徑, 主解析度, 標題

    def 同調(self, 工程路徑):
        v = self.vue
        try:
            v.工程路徑 = 工程路徑
            v.圖標路徑, v.主解析度, v.標題 = self.讀取工程信息(工程路徑)
        except Exception as e:
            logging.warning(e.__repr__())
            alert('工程配置文件不正確。')
        js(f'進入工程()')

    def 開啓工程(self, 工程路徑=None):
        if 工程路徑:
            self.同調(工程路徑)
        else:
            with wx.DirDialog(self.窗口, "选择文件夹") as dlg:
                dlg.SetPath(str(Path('./Librian本體/project').resolve()))
                if dlg.ShowModal() == wx.ID_OK:
                    self.同調(dlg.GetPath())

    def 建立工程(self):
        with wx.TextEntryDialog(self.窗口, '工程名: ', '建立工程') as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                新工程路徑 = (Path('Librian本體/project') / dlg.GetValue()).resolve()
                if 新工程路徑.is_dir():
                    alert('已經有這個工程了。')
                    return
                shutil.copytree('./Librian本體/模板/默認工程', 新工程路徑)
                self.同調(新工程路徑)

    def 運行(self):
        subprocess.Popen(f'cmd /c cd Librian本體 & "../python36/python" librian.py --project {self.vue.工程路徑}')

    def 運行同時編寫(self):
        subprocess.Popen(
            'cmd /c cd Librian本體 & ' +
            f'"../python36/python" librian.py --project {self.vue.工程路徑} ' +
            '--config "{編寫模式: True}"'
        )
        os.system(f'"{self.vue.工程路徑}/{虛擬機環境.劇本入口}"')

    def 打開文件夾(self):
        os.system(f'start {self.vue.工程路徑}')

    def 生成exe(self):
        from Librian本體 import 構建
        if 虛擬機環境.圖標:
            構建.構建工程(self.vue.工程路徑, 虛擬機環境.標題, f'{self.vue.工程路徑}/{虛擬機環境.圖標}')
        else:
            構建.構建工程(self.vue.工程路徑, 虛擬機環境.標題)
        alert('好了。')

    def 生成html(self):
        from Librian本體 import 幻象
        with wx.TextEntryDialog(self.窗口, '目标路径: ', '幻象') as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                目標路徑 = Path(dlg.GetValue())
                if 目標路徑.is_dir():
                    alert('不行')
                else:
                    幻象.幻象化(目標路徑)
                    alert('好了。')


app, 瀏覽器 = wxcef.group(title='librian面板', url='file:///html面板/面板.html', icon='./Librian本體/資源/librian.ico', size=(800, 450))
真山彥 = 山彥(app.frame)
app.frame.set_browser_object("山彥", 真山彥)
app.MainLoop()
