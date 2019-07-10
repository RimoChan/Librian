import os
import tempfile
import subprocess

import win32api
import win32con

此處 = os.path.dirname(os.path.abspath(__file__))

def 構建工程(工程路徑, 標題, 圖標=None):
    if 圖標:
        subprocess.Popen(f'{此處}\\構建用\\ResourceHacker.exe -open {此處}\\構建用\\虛僞的exe.exe -save {標題}.exe -action addoverwrite -res {圖標} -mask ICONGROUP,1,0')
    else:
        os.system(f'copy {此處}\\構建用\\虛僞的exe.exe {標題}.exe')
        
    if os.path.isfile(f'_{標題}.kuzu'):
        win32api.SetFileAttributes(f'_{標題}.kuzu', win32con.FILE_ATTRIBUTE_NORMAL)
    with open(f'_{標題}.kuzu', 'w') as f:
        f.write(f'cmd /c "cd Librian本體 & ..\\python36\\python.exe Librian.py --project {工程路徑}"')
    win32api.SetFileAttributes(f'_{標題}.kuzu', win32con.FILE_ATTRIBUTE_HIDDEN)


def 構建Librian面板():
    f = tempfile.NamedTemporaryFile(delete=False)
    b = 'import os;os.system(\'\""./python36/python\"" -m librian_panel.py\');os.system("pause")'.encode('utf8')
    f.write(b)
    f.close()
    os.system(f'pyinstaller {f.name} --name Librian面板.exe --distpath ./ -F -i 資源/librian.ico')


if __name__ == '__main__':
    構建Librian面板()
