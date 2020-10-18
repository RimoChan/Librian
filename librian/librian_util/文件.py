import os
import logging


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