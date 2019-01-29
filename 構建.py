import os
import tempfile


def 構建工程(工程路徑, 標題, 圖標):
    f = tempfile.NamedTemporaryFile(delete=False)
    b = f'import os;os.system(\'\""./python36/python\"" -m Librian.py --project {工程路徑} \');os.system("pause")'.encode('utf8')
    f.write(b)
    f.close()
    os.system(f'pyinstaller {f.name} --name output.exe --distpath ./ -F -i {圖標}')
    os.system(f'del "{標題}.exe"')
    os.system(f'rename output.exe "{標題}.exe"')


def 構建Librian面板():
    f = tempfile.NamedTemporaryFile(delete=False)
    b = 'import os;os.system(\'\""./python36/python\"" -m librian_panel.py\');os.system("pause")'.encode('utf8')
    f.write(b)
    f.close()
    os.system(f'pyinstaller {f.name} --name Librian面板.exe --distpath ./ -F -i 資源/librian.ico')


if __name__ == '__main__':
    構建Librian面板()
