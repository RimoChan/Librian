import os
import shutil

import yaml
from psd_tools import PSDImage
import PIL

def png假裝拆包(文件名,目標文件夾):
    try:
        os.mkdir(目標文件夾)
    except:
        None
    前名=os.path.basename(os.path.splitext(文件名)[0])
    圖片文件夾=os.path.join(目標文件夾,前名)
    try:
        os.mkdir(圖片文件夾)
    except:
        None
    shutil.copy(文件名,os.path.join(圖片文件夾,'_.png'))
    
    with open(os.path.join(圖片文件夾,'位置.yaml' ),'w',encoding='utf8') as f:
        f.write('_:\n  x: 0\n  y: 0')

def 拆包(文件名,目標文件夾):
    try:
        os.mkdir(目標文件夾)
    except:
        None
    前名=os.path.basename(os.path.splitext(文件名)[0])
    圖片文件夾=os.path.join(目標文件夾,前名)
    psd = PSDImage.load(文件名)
    d={}
    def 記錄(層,path=''):
        print(path)
        try:
            os.mkdir(os.path.join(圖片文件夾,path))
        except:
            None
        if hasattr(層,'layers'):
            for i in 層.layers:
                記錄(i,path+層.name+'/')
        else:
            名=path+層.name
            d[名]={'x':層.bbox.x1,'y':層.bbox.y1}
            layer_image = 層.as_PIL()
            layer_image.save(os.path.join(圖片文件夾,f'{名}.png'))
    
    for i in psd.layers:
        記錄(i)
    
    with open(os.path.join(圖片文件夾,'位置.yaml' ),'w',encoding='utf8') as f:
        yaml.dump(d,f,default_flow_style=False,allow_unicode=1)

if __name__=='__main__':
    拆包('project/test/立繪/靈夢.psd',目標文件夾='project/test/_臨時文件')