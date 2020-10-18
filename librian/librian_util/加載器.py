import os
import logging
    

def yaml(文件名, 默認=[]):
    import yaml
    return 加載(文件名, yaml.safe_load, 默認)
    
    
def 加載(文件名, 加載方法, 默認):
    if os.path.isfile(文件名):
        try:
            with open(文件名, encoding='utf8') as f:
                內容 = 加載方法(f)
            return 內容
        except Exception as e:
            logging.exception(e)
            logging.warning(f'「{文件名}」沒能讀入。')
    return 默認
    
    
    