import logging
import subprocess
import base64
import hashlib

import requests

from . import 路徑, release信息


嵌入的python路徑 = 路徑.librian外層 / 'python36/python.exe'

嵌入的git路徑 = 路徑.librian外層 / 'MinGit-2.25.0-busybox-64-bit/cmd/git.exe'


def 自我更新():
    if release信息.是release:
        git路徑 = 嵌入的git路徑
    else:
        try:
            git路徑 = 'git'
            subprocess.check_call('git --version', stdout=subprocess.DEVNULL)
        except FileNotFoundError:
            raise FileNotFoundError('需要一個Git。更新功能需要你有Git命令可用，或者使用release版本中嵌入的Git。')
    subprocess.run(
        [str(git路徑), 'pull', 'origin', 'master'],
        shell=True,
        check=True,
        stderr=subprocess.PIPE,
        cwd=路徑.librian外層,
    )

    if release信息.是release:
        subprocess.run(
            [str(嵌入的python路徑), '-m', 'pip', 'install', '-r', 'requirements_release.txt'],
            shell=True,
            check=True,
            stderr=subprocess.PIPE,
            cwd=路徑.librian外層,
        )
        build文件更新()


def build文件更新(): 
    def md5(fname):
        hash_md5 = hashlib.md5()
        with open(fname, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return base64.b64encode(hash_md5.digest()).decode('utf-8')

    def 下載(文件名, 網址):
        r = requests.get(網址)
        with open(文件名, 'wb') as f:
            f.write(r.content)

    文件表 = {
        'Librian面板.exe': 'https://rimosto-cdn.azureedge.net/librian/Librian面板.exe'
    }
    for 文件名, 網址 in 文件表.items():
        文件真名 = 路徑.librian外層 / 文件名
        if 文件真名.is_file():
            本地md5 = md5(文件真名)
            在線md5 = requests.head(網址).headers['Content-MD5']
            if 本地md5 == 在線md5:
                continue
            logging.warning(f'{文件名}過期了。')
        下載(文件名, 網址)
        logging.warning(f'下載{文件名}。')
