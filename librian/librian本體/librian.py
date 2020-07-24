import os
import logging

import fire

from . import 環境
from . import librian虛擬機
from .librian虛擬機 import 虛擬機環境


def librian_main(project, config=None):
    logging.info('librian_main啓動。')
    librian虛擬機.虛擬機環境.加載配置(project)
    if config:
        環境.導入全局配置(config)

    os.makedirs(f'{虛擬機環境.工程路徑}/存檔資料/手動存檔', exist_ok=True)
        
    from . import 窗口
    app = 窗口.啓動app()
    app.MainLoop()


fire.Fire(librian_main)
