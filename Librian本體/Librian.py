import os
import logging

import yaml
import fire

import 環境

import Librian虛擬機
import Librian虛擬機.虛擬機環境


def librian_main(project, config=None):
    Librian虛擬機.虛擬機環境.加載配置(project)
    if config:
        環境.導入全局配置(config)

    os.makedirs(f'{Librian虛擬機.虛擬機環境.工程路徑}/存檔資料/手動存檔', exist_ok=True)
        
    import 窗口

    app = 窗口.app()
    app.MainLoop()


fire.Fire(librian_main)
