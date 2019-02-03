import logging
import json
import os
import subprocess
import shutil

from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtGui import *

import 環境


def js(code):
    主窗口.網頁.頁面.runJavaScript(code)


def alert(s):
    js(f'alert("{s}")')


class 山彥(QObject):
    def __init__(self, 頁面):
        super().__init__()
        self.頁面 = 頁面

    def 初始化(self):
        pass

    def 同調(self, 工程路徑):
        try:
            self.工程路徑 = 工程路徑
            環境.設定工程路徑(工程路徑)
            配置 = 環境.配置
            if 配置['圖標']:
                圖標路徑 = os.path.relpath('%s/%s' % (工程路徑, 配置['圖標']), './html面板')
            else:
                圖標路徑 = '../資源/librian.ico'
            js(f'v.工程路徑={工程路徑.__repr__()}')
            js(f'v.圖標路徑={圖標路徑.__repr__()}')
            js(f'v.標題={配置["標題"].__repr__()}')
            js(f'v.主解析度={配置["主解析度"].__repr__()}')
        except Exception as e:
            print(e)
            alert('工程配置文件不正確。')
        js(f'進入工程()')

    def 開啓工程(self):
        工程路徑 = QFileDialog.getExistingDirectory(主窗口,
                                                "選取文件夾",
                                                "./project")
        if 工程路徑:
            self.同調(工程路徑)

    def 建立工程(self):
        s, go = QInputDialog.getText(主窗口, "小面板", "工程名", QLineEdit.Normal, "")
        if not go:
            return
        新工程路徑 = os.path.join('.', 'project', s)
        if os.path.isdir(新工程路徑):
            self.box = QMessageBox(QMessageBox.Warning, "小面板", "已經有這個工程了。")
            self.box.show()
            return
        shutil.copytree('./project/_默認工程', 新工程路徑)
        self.同調(新工程路徑)

    def 運行(self):
        os.system(f'""./python36/python"" ./librian.py --project {self.工程路徑}')

    def 運行同時編寫(self):
        subprocess.Popen(
            f'"./python36/python" ./librian.py --project {self.工程路徑} ' +
            '--config "{編寫模式: True}"'
        )

    def 打開文件夾(self):
        os.system(f'start {self.工程路徑}')

    def 生成exe(self):
        import 構建
        構建.構建工程(self.工程路徑, 環境.配置["標題"], '%s/%s' % (self.工程路徑, 環境.配置['圖標']))
        alert('好了。')

    def 生成html(self):
        import 虛擬演繹
        虛擬演繹.生成虛擬核心()
        alert('好了。')

    @pyqtSlot(str, str)
    def rec2(self, 令, 參數):
        logging.debug(f'收到頁面來的指令:「{令}({參數})」')
        if 令 in 山彥.__dict__:
            山彥.__dict__[令](self, 參數)
        else:
            raise Exception(f'命令「{令}」無法理解。')
        js('link_on=true')

    @pyqtSlot(str)
    def rec1(self, 令):
        logging.debug(f'收到頁面來的指令: 「{令}」')
        if 令 in 山彥.__dict__:
            山彥.__dict__[令](self)
        else:
            raise Exception(f'命令「{令}」無法理解。')
        js('link_on=true')


class gal窗口(QWebEngineView):

    def __init__(self, *li):
        super().__init__(*li)
        self.準備網頁()
        self.做界面()

    def 準備網頁(self):
        self.頁面 = self.page()
        self.頻道 = QWebChannel()
        self.handler = 山彥(self.頁面)
        self.頻道.registerObject('handler', self.handler)
        self.頁面.setWebChannel(self.頻道)

    def 做界面(self):
        self.resize(800, 450)
        self.load(QUrl('file:///html面板/面板.html'))
        self.show()


class 統合窗口(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('./資源/librian.ico'))
        self.setWindowTitle('librian面板')
        self.resize(800, 450)
        self.網頁 = gal窗口(self)
        self.show()


app = QApplication([])
主窗口 = 統合窗口()
app.exec_()
