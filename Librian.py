import os
import logging
import argparse
import yaml

import 環境

參數 = argparse.ArgumentParser(description='啓動Librian。')
參數.add_argument('--project', type=str, required=True)
參數.add_argument('--config', type=str)
參數 = 參數.parse_args()

import Librian虛擬機
import Librian虛擬機.虛擬機環境
Librian虛擬機.虛擬機環境.加載配置(參數.project)

if 參數.config:
    環境.導入全局配置(yaml.load(參數.config))
    

try:
    os.mkdir(f'{環境.工程路徑}/存檔資料')
except Exception as e:
    logging.debug('已有存檔。')
    
import 窗口
    
app = 窗口.app()

app.MainLoop()
