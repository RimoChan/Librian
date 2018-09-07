from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
app = QApplication([])

def q(w):
    工程路徑 = QFileDialog.getExistingDirectory(w,
                                    "选取文件夹",
                                    "./")   
    w.答案 = 工程路徑
    app.exit()

def 詢問():     
    w = QWidget()
    w.resize(400,400)
    w.setWindowTitle('Librian面板')
    w.setWindowIcon(QIcon('資源/librian.ico'))
    
    btn = QPushButton('選擇工程', w)
    btn.setGeometry(100,100, 200, 200)
    btn.clicked.connect(lambda:q(w))
    
    w.show()
    app.exec_()
    
    return w.答案
    
if __name__=='__main__':
    print(詢問())