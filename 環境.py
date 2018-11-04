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
        a=yaml.load(f)
        for i in a:
            配置.update(a[i])
    
    配置['psd路徑']=os.path.join(工程路徑,配置['立繪文件夾'])
    配置['圖片路徑']=f"./{工程路徑}/_臨時文件"
    配置['圖片相對網頁路徑']=f"../{工程路徑}/_臨時文件"