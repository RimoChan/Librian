from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtGui import *
import time, threading
import os,sys
import logging


from 環境 import 配置,工程路徑
try:
    os.mkdir('%s/save_data' %工程路徑)
except:
    logging.debug('已有存檔。')

app = QApplication([])

import 劇本
import 窗口
import 鏡頭

app.exec_()
