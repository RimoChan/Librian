import time
import threading
import os
import sys
import logging
import argparse

from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtGui import *

參數 = argparse.ArgumentParser(description='啓動Librian。')
參數.add_argument('--project', type=str)
參數 = 參數.parse_args()

import 環境
from 環境 import 配置


def 路徑處理(路徑):
    return os.path.relpath(路徑).replace('\\', '/')


if 參數.project is not None:
    工程路徑 = 路徑處理(參數.project)
    環境.設定工程路徑(工程路徑)
else:
    import librian面板
    工程路徑 = 路徑處理(librian面板.詢問())
    環境.設定工程路徑(工程路徑)

try:
    os.mkdir(f'{工程路徑}/存檔資料')
except:
    logging.debug('已有存檔。')

app = QApplication([])

import 窗口

app.exec_()
