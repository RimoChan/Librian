import yaml
import logging
import os

with open('配置.yaml',encoding='utf8') as f:
    配置=yaml.load(f)
    if 配置['額外信息']:
        logging.basicConfig(level=logging.DEBUG)

工程路徑=None

def 設定工程路徑(路徑):
    global 工程路徑
    工程路徑=路徑
    with open('%s/工程配置.yaml'%工程路徑,encoding='utf8') as f:
        配置.update(yaml.load(f))
