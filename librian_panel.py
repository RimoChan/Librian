import logging
import os
import sys
import json
import subprocess
import threading
import shutil
import datetime
from pathlib import Path

import yaml
import dulwich.repo

try:
    import wx
    import Librian_util.wxcef as wxcef
except ModuleNotFoundError:
    logging.warning('沒能import wx，改爲使用pyside2。')
    import Librian_util.fake_wx as wx
    import Librian_util.qtcef as wxcef

from Librian本體.帶有vue的山彥 import 帶有vue的山彥
from Librian本體.Librian虛擬機 import 虛擬機環境

from Librian_util import 加載器, 文件


r = dulwich.repo.Repo('.')
最後提交unix時間 = r[r.head()].author_time
最後提交時間 = datetime.datetime.fromtimestamp(最後提交unix時間)


class 山彥(帶有vue的山彥):
    def __init__(self, *li, **d):
        super().__init__(*li, **d)
        self.vue.存檔資料 = 加載器.yaml('./存檔資料/存檔資料.yaml')
        self.vue.最後提交時間 = 最後提交時間.strftime('%y-%m-%d')

    def js(self, x):
        self.窗口.browser.ExecuteJavascript(x)

    def alert(self, title, icon=None, text=None):
        msg = {"title": title, "icon": icon, "text": text}
        self.js(f'Swal.fire({json.dumps(msg)})')

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
            logging.exception(e)
            self.alert('工程配置文件不正確。', 'error')
        self.js(f'進入工程()')

    def 開啓工程(self, 工程路徑=None):
        if 工程路徑:
            self.同調(工程路徑)
        else:
            with wx.DirDialog(self.窗口, "选择文件夹") as dlg:
                dlg.SetPath(str(Path('./Librian本體/project').resolve()))
                if dlg.ShowModal() == wx.ID_OK:
                    self.同調(dlg.GetPath())

    def 建立工程(self, 新工程名, 使用潘大爺的模板):
        新工程路徑 = (Path('Librian本體/project') / 新工程名).resolve()
        if 新工程路徑.is_dir():
            self.alert('已經有這個工程了。', 'error')
            return
        if 使用潘大爺的模板:
            shutil.copytree('./Librian本體/模板/潘大爺的模板', 新工程路徑)
        else:
            shutil.copytree('./Librian本體/模板/默認模板', 新工程路徑)
        self.同調(新工程路徑)

    def 運行(self):
        if wxcef.WINDOWS:
            subprocess.Popen(['cd', 'Librian本體', '&', sys.executable, 'librian.py', '--project', self.vue.工程路徑], shell=True)
        else:
            env = dict()
            env.update(os.environ)
            env['LD_LIBRARY_PATH'] = wxcef.ld_library_path
            subprocess.Popen(
                [sys.executable, 'Librian.py', '--project', self.vue.工程路徑],
                shell=False,
                cwd='Librian本體',
                env=env)

    def 運行同時編寫(self):
        if wxcef.WINDOWS:
            subprocess.Popen([
                'cd', 'Librian本體', '&',
                sys.executable, 'librian.py', '--project', self.vue.工程路徑,
                '--config', '{編寫模式: True}'
            ], shell=True)
            劇本文件名 = f'{self.vue.工程路徑}/{虛擬機環境.劇本入口}'
            if 文件.查詢文件打開方式(劇本文件名):
                os.system(f'"{劇本文件名}"')
            else:
                os.system(f'notepad "{劇本文件名}"')
        else:
            env = dict()
            env.update(os.environ)
            env['LD_LIBRARY_PATH'] = wxcef.ld_library_path
            subprocess.Popen(
                [sys.executable, 'Librian.py', '--project', self.vue.工程路徑,
                 '--config', '{編寫模式: True}'],
                shell=False,
                cwd='Librian本體',
                env=env)
            if wxcef.MAC:
                subprocess.Popen(['open', f'{self.vue.工程路徑}/{虛擬機環境.劇本入口}'],
                                 shell=False)
            elif wxcef.LINUX:
                subprocess.Popen(
                    ['xdg-open', f'{self.vue.工程路徑}/{虛擬機環境.劇本入口}'],
                    shell=False)

    def 打開文件夾(self):
        if wxcef.WINDOWS:
            subprocess.Popen(['start', self.vue.工程路徑], shell=True)
        elif wxcef.MAC:
            subprocess.Popen(['open', self.vue.工程路徑], shell=False)
        elif wxcef.LINUX:
            subprocess.Popen(['xdg-open', self.vue.工程路徑], shell=False)

    def 生成exe(self):
        from Librian本體 import 構建
        if 虛擬機環境.圖標:
            構建.構建工程(self.vue.工程路徑, 虛擬機環境.標題, f'{self.vue.工程路徑}/{虛擬機環境.圖標}')
        else:
            構建.構建工程(self.vue.工程路徑, 虛擬機環境.標題)
        self.alert('好了', 'success')

    def 生成html(self, 目標路徑):
        from Librian本體 import 幻象
        目標路徑 = Path(目標路徑)
        if 目標路徑.is_dir():
            self.alert('目录已经存在', 'error')
        else:
            幻象.幻象化(目標路徑)
            self.alert('好了', 'success')

    def 瀏覽器打開(self, s):
        import webbrowser
        webbrowser.open(s)
    
    def 自我更新(self, callback):
        git路徑 = 'git'
        try:
            subprocess.check_call('git --version', stdout=subprocess.DEVNULL)
        except Exception as e:
            嵌入的git路徑 = './MinGit-2.25.0-busybox-64-bit/cmd/git.exe'
            if Path(嵌入的git路徑).is_file():
                git路徑 = 嵌入的git路徑
            else:
                self.alert('需要一個Git', 'info', '更新功能需要你有Git命令可用，或者使用relase版本中嵌入的Git。')
                return
        def t():
            r = subprocess.run(f'{git路徑} pull origin master', stderr=subprocess.PIPE, encoding='utf8')
            callback.Call([r.returncode, r.stderr])
        l = threading.Thread(target=t).start()
        
    def 退出(self):
        exit()
        

if any([ord(i) > 255 for i in os.getcwd()]):
    logging.warning('Librian在python路徑有漢字(非ACSII字符)的場合可能出問題。')

app, 瀏覽器 = wxcef.group(title='librian面板', url=文件.轉爲網址路徑('./面板前端/面板.html'), icon='./Librian本體/資源/librian.ico', size=(960, 540))
真山彥 = 山彥(app.frame)
app.frame.set_browser_object("山彥", 真山彥)
app.MainLoop()
