from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtGui import *
import logging
import json

from 劇本 import 讀者
from 環境 import 配置,工程路徑


def js(code):
    主窗口.頁面.runJavaScript(code)
def 更新():
    js('state_Change(%s)' % json.dumps(讀者.狀態.導出()))
#————————————————————————————
#接受gui回傳的資訊
class 山彥(QObject):
    def __init__(self,頁面):
        super().__init__()
        self.頁面=頁面

    def 選擇讀檔文件(self):
        return QFileDialog.getOpenFileName(
            self.頁面.parent(),
            '讀檔',
            f'{工程路徑}/存檔資料',
            'pickle 文件 (*.pkl)'
        )
    def 選擇存檔文件(self):
        return QFileDialog.getSaveFileName(
            self.頁面.parent(),
            '存檔',
            f'{工程路徑}/存檔資料',
            'pickle 文件 (*.pkl)'
        )
        
    def 更新(self):
        更新()
    def 步進(self):
        讀者.步進()
    def 步進更新(self):
        讀者.步進()
        更新()
    def 初始化(self):
        js(f'''path="../{工程路徑}/"; 
              自定css="{配置['自定css']}";
              解析度={配置['主解析度']};
              邊界={int(配置['顯示繪圖邊界'])};
              link_on=true; 
              準備工作();
           ''')
    def 存檔(self):
        文件名, 文件類型 = self.選擇存檔文件()
        if 文件名:
            讀者.存檔(文件名)
            js('提示("存檔好了。")')
    def 讀檔(self):
        文件名, 文件類型 = self.選擇讀檔文件()
        if 文件名:
            讀者.讀檔(文件名)
            更新()
    def 快速存檔(self):
        讀者.存檔(f'{工程路徑}/存檔資料/快速存檔.pkl')
        js('提示("存檔好了。")')
    def 從title讀檔(self):
        文件名, 文件類型 = self.選擇讀檔文件()
        if 文件名:
            讀者.讀檔(文件名)
            js('開始()')
    def 退出(self):
        exit()
    def 回標題(self):
        讀者.__init__()
        js(f'window.location.href="file:///{工程路徑}/{配置["標題畫面"]}"')
        
    @pyqtSlot(str)
    def rec(self,令):
        logging.debug(f'受到頁面來的指令: 「{令}」')
        if 令 in 山彥.__dict__:
            山彥.__dict__[令](self)
        elif 令[0]=='選':
            令=令[1:]
            t=讀者.狀態.選項[int(令)][1]
            讀者.狀態.選項=()
            t()
            logging.debug('選擇了「%s」。'%令)
            讀者.步進()
            更新()
        else:
            raise Exception(f'命令「{令}」無法理解。')
                
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
            self.load(QUrl(f'file:///{工程路徑}/{配置["標題畫面"]}'))
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
        QShortcut(QKeySequence('alt+enter'), self).activated.connect(lambda:self.切換全屏())

    def resizeEvent(self,ev):
        self.頁面.setZoomFactor(min(self.width()/配置['主解析度'][0],self.height()/配置['主解析度'][1]))

    # 媽的到底怎麼固定比例……
    def 不用的resizeEvent(self,ev):
        self.頁面.setZoomFactor(min(self.width()/配置['主解析度'][0],self.height()/配置['主解析度'][1]))
        if self.全屏: return
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

    
主窗口 = gal窗口()
