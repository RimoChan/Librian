from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtGui import *
import logging
import json

from 劇本 import 讀者
from 環境 import 配置,工程路徑
#————————————————————————————
#接受gui回傳的資訊
class 山彥(QObject):
    def __init__(self,頁面):
        super().__init__()
        self.頁面=頁面

    @pyqtSlot(str)
    def rec(self,令):
        logging.debug(令)
        if 令=='更新':
            更新()
        elif 令=='步進更新':
            讀者.步進()
            更新()
        elif 令=='同步路徑':
            js('path="../%s/"; 自定css="%s"; link_on=true; 準備工作();' % (工程路徑,配置['自定css']))
        elif 令=='存檔':
            讀者.存檔('%s/save_data/save_1.dat' %工程路徑)
        elif 令=='讀檔':
            讀者.讀檔('%s/save_data/save_1.dat' %工程路徑)
            更新()
        elif 令=='退出':
            exit()
        else:
            t=讀者.選項[int(令)][1]
            讀者.選項=()
            t()
            logging.debug('選擇了「%s」。'%令)
            讀者.步進()
            更新()
                
        js('link_on=true')

#————————————————————————————
#視窗介面
class gal窗口(QWebEngineView):

    def __init__(self):
        super().__init__()
        self.準備網頁()
        self.準備快速鍵()
        self.做界面()

    def 準備網頁(self): 
        self.頁面=self.page()
        self.頻道 = QWebChannel()
        self.handler = 山彥(self.頁面)
        self.頻道.registerObject('handler',self.handler)
        self.頁面.setWebChannel(self.頻道)

    def 做界面(self):
        self.setWindowTitle(配置['標題'])
        self.setWindowIcon(QIcon('%s/%s' %(工程路徑,配置['圖標']) ))

        if 配置['標題畫面']:
            self.load(QUrl('file:///%s/%s' %(工程路徑,配置['標題畫面']) ))
        else:
            self.load(QUrl('file:///html/title.html'))
            
        self.全屏=False
        self.resize(*配置['主解析度'])
        self.show()

    def 切換全屏(self):
        self.全屏=not self.全屏
        if self.全屏:
            self.showFullScreen()
        else:
            self.showNormal()

    def 準備快速鍵(self):
        #我也不知道為什麼enter就是綁定不了2333
        QShortcut(QKeySequence('alt+\\'), self).activated.connect(lambda:self.切換全屏())

    def resizeEvent(self,ev):
        self.頁面.setZoomFactor(min(self.width()/配置['主解析度'][0],self.height()/配置['主解析度'][1]))
        if self.全屏: return
        # 媽的到底怎麼固定比例……
        比例=配置['主解析度'][0]/配置['主解析度'][1]
        w,h=ev.size().width() , ev.size().height()
        try:
            if w>=self.w and h>=self.h:
                self.setMinimumWidth(h*比例-1)
                self.setMinimumHeight(w/比例-1)
                self.setMaximumWidth(9999)
                self.setMaximumHeight(9999)
            else:
                self.setMaximumWidth(h*比例+1)
                self.setMaximumHeight(w/比例+1)
                self.setMinimumWidth(300*比例)
                self.setMinimumHeight(300)
        except BaseException as e:
            None
        self.w,self.h=self.width(),self.height()

def js(code):
    主窗口.頁面.runJavaScript(code)

def 更新():
    js('state_Change(%s)' % json.dumps(讀者.當前狀態))
    
主窗口 = gal窗口()
