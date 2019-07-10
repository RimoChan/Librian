import logging
import os
import subprocess
import shutil
import wx

from Librian本體 import wxcef
from Librian本體.Librian虛擬機 import 虛擬機環境


def js(x):
    真山彥.窗口.browser.ExecuteJavascript(x)


def alert(s):
    js(f'alert("{s}")')


class 山彥:
    def __init__(self, 窗口):
        self.窗口 = 窗口

    def 同調(self, 工程路徑):
        try:
            self.工程路徑 = 工程路徑
            虛擬機環境.加載配置(工程路徑)
            if 虛擬機環境.圖標:
                圖標路徑 = os.path.relpath(f'{工程路徑}/{虛擬機環境.圖標}', './html面板')
            else:
                圖標路徑 = '../Librian本體/資源/librian.ico'
            js(f'v.工程路徑={工程路徑.__repr__()}')
            js(f'v.圖標路徑={圖標路徑.__repr__()}')
            js(f'v.標題={虛擬機環境.標題.__repr__()}')
            js(f'v.主解析度={虛擬機環境.主解析度.__repr__()}')
        except Exception as e:
            print(e)
            alert('工程配置文件不正確。')
        js(f'進入工程()')

    def 開啓工程(self):
        with wx.DirDialog(self.窗口, "选择文件夹") as dlg:
            dlg.SetPath(os.path.abspath('./Librian本體/project'))
            if dlg.ShowModal() == wx.ID_OK:
                self.同調(dlg.GetPath())

    def 建立工程(self):
        with wx.TextEntryDialog(self.窗口, '工程名: ', '小面板') as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                新工程路徑 = os.path.join('.', 'project', dlg.GetValue())
                if os.path.isdir(新工程路徑):
                    alert('已經有這個工程了。')
                    return
                shutil.copytree('./Librian本體/project/_默認工程', 新工程路徑)
                self.同調(新工程路徑)

    def 運行(self):
        subprocess.Popen(f'cmd /c cd Librian本體 & "../python36/python" librian.py --project {self.工程路徑}')
        
    def 運行同時編寫(self):
        subprocess.Popen(
            'cmd /c cd Librian本體 & ' +
            f'"../python36/python" librian.py --project {self.工程路徑} '
            + '--config "{編寫模式: True}"'
        )
        os.system(f'"{self.工程路徑}/{虛擬機環境.劇本入口}"')

    def 打開文件夾(self):
        os.system(f'start {self.工程路徑}')

    def 生成exe(self):
        from Librian本體 import 構建
        if 虛擬機環境.圖標:
            構建.構建工程(self.工程路徑, 虛擬機環境.標題, f'{self.工程路徑}/{虛擬機環境.圖標}')
        else:
            構建.構建工程(self.工程路徑, 虛擬機環境.標題)
        alert('好了。')

    def 生成html(self):
        from Librian本體 import 虛擬演繹
        虛擬演繹.生成虛擬核心()
        alert('好了。')


app, 瀏覽器=wxcef.group(title = 'librian面板', url = 'file:///html面板/面板.html', icon = './Librian本體/資源/librian.ico', size = (800, 450))
真山彥=山彥(app.frame)
app.frame.set_browser_object("山彥", 真山彥)
app.MainLoop()
