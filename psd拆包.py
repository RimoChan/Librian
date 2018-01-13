import os

import yaml
from psd_tools import PSDImage
import PIL

def 拆包(文件名):
    psd = PSDImage.load(文件名)
    前名=文件名[:-4] +'/' #網頁路徑問題的patch……什麼鬼2333
    print(前名)
    d={}
    def 記錄(層,path=''):
        try:
            os.mkdir(前名+path)
        except:
            None
        if hasattr(層,'layers'):
            for i in 層.layers:
                記錄(i,path+層.name+'/')
        else:
            名=path+層.name
            d[名]={'x':層.bbox.x1,'y':層.bbox.y1}
            layer_image = 層.as_PIL()
            layer_image.save(前名+'%s.png' %名)
    
    for i in psd.layers:
        記錄(i)
    
    with open('%s/位置.yaml'%前名,'w',encoding='utf8') as f:
        yaml.dump(d,f,default_flow_style=False,allow_unicode=1)

if __name__=='__main__':
    拆包('../project/test/立繪/靈夢.psd')