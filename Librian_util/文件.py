import os
import logging

import win32api
import win32con


def 補充擴展名(文件名, 擴展名表, 路徑='./'):
    if '.' in os.path.split(文件名)[-1]:
        if not os.path.isfile(f'{路徑}/{文件名}'):
            logging.warning(f'「{文件名}」不存在。')
        return 文件名
    for 擴展名 in 擴展名表:
        if os.path.isfile(f'{路徑}/{文件名}.{擴展名}'):
            return f'{文件名}.{擴展名}'
    logging.warning(f'「{文件名}」不存在。')
    return 文件名


def 轉爲網址路徑(路徑):
    絕對路徑 = os.path.abspath(路徑)
    return f'file:///{絕對路徑}'


def 查詢文件打開方式(文件名): 
    ext = os.path.splitext(文件名)[-1]
    try:
        key = win32api.RegOpenKey(win32con.HKEY_CLASSES_ROOT, ext, 0, win32con.KEY_READ)
    except:
        return None
    q = win32api.RegQueryValue(key, '')
    key = win32api.RegOpenKey(win32con.HKEY_CLASSES_ROOT, f'{q}\shell\open\command', 0, win32con.KEY_READ)
    q = win32api.RegQueryValue(key, '')
    return q
