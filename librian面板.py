from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
import shutil
import copy

class librian面板(QWidget):
    def __init__(self,app):
        super().__init__()
        self.app=app
        
        self.resize(400,400)
        self.setWindowTitle('Librian面板')
        self.setWindowIcon(QIcon('資源/librian.ico'))
        
        self.btn1 = QPushButton('選擇工程', self)
        self.btn1.setGeometry(100,100, 100, 100)
        self.btn1.clicked.connect(lambda:self.選擇工程())

        self.btn2 = QPushButton('新建工程', self)
        self.btn2.setGeometry(200,200, 100, 100)
        self.btn2.clicked.connect(lambda:self.新建工程())
        
        self.show()
        
    def 選擇工程(self):
        工程路徑 = QFileDialog.getExistingDirectory(self,
                                    "选取文件夹",
                                    "./project")   
        self.答案 = 工程路徑
        self.app.exit()

    
    def 新建工程(self):
        s,go=QInputDialog.getText(self, "喵喵喵","工程名",QLineEdit.Normal, "") 
        if not go: return
        新工程路徑=os.path.join('.','project',s)
        if os.path.isdir(新工程路徑):
            self.box=QMessageBox(QMessageBox.Warning, "喵喵喵", "已經有這個工程了。")
            self.box.show()
            return
        shutil.copytree('./project/_默認工程', 新工程路徑)
        os.system(f'start {新工程路徑}')
        
app = QApplication([])
def 詢問():
    a=librian面板(app)
    app.exec_()
    return a.答案

if __name__=='__main__':
    print(詢問())