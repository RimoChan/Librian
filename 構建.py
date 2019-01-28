import os
import tempfile


def 構建工程():
    f = tempfile.NamedTemporaryFile(delete=False)
    b = 'import os;os.system(\'\""./python36/python.exe\"" -m Librian.py --project ./project/極夜所在的星之海 \');os.system("pause")'.encode('utf8')
    f.write(b)
    f.close()
    os.system(f'pyinstaller {f.name} --name Ragnarok.exe --distpath ./ -F -i ./project/極夜所在的星之海/畫面/圖標.ico')


def 構建Librian面板():
    f = tempfile.NamedTemporaryFile(delete=False)
    b = 'import os;os.system(\'\""./python36/python.exe\"" -m librian_panel.py\');os.system("pause")'.encode('utf8')
    f.write(b)
    f.close()
    os.system(f'pyinstaller {f.name} --name Librian面板.exe --distpath ./ -F -i 資源/librian.ico')


構建Librian面板()
