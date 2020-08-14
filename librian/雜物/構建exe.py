import os
import subprocess
from pathlib import Path

import win32api
import win32con

import librian.librian_util.路徑 as 路徑


此處 = Path(__file__).parent


def 構建工程(工程路徑, 標題, 圖標=None):
    if 圖標:
        subprocess.Popen(f'{此處}\\構建用\\ResourceHacker.exe -open {此處}\\構建用\\沒有窗口的虛僞的exe.exe -save {標題}.exe -action addoverwrite -res {圖標} -mask ICONGROUP,1,0')
    else:
        os.system(f'copy {此處}\\構建用\\沒有窗口的虛僞的exe.exe {標題}.exe')

    if os.path.isfile(f'_{標題}.kuzu'):
        win32api.SetFileAttributes(f'_{標題}.kuzu', win32con.FILE_ATTRIBUTE_NORMAL)
    with open(f'_{標題}.kuzu', 'w') as f:
        f.write(f'-m librian.librian本體.librian --project "{os.path.relpath(工程路徑, start=路徑.librian外層)}"')
    win32api.SetFileAttributes(f'_{標題}.kuzu', win32con.FILE_ATTRIBUTE_HIDDEN)
