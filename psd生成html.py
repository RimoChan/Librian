import os
import logging

import yaml
from 環境 import 配置,工程路徑

import psd拆包

相對網頁路徑="../%s/立繪" %工程路徑
立繪路徑='%s/立繪' %工程路徑
try:
    with open('%s/映射.yaml' %立繪路徑,encoding='utf8') as f:
        映射=yaml.load(f)
except Exception as e: 
    logging.warning('立繪立即被停用。立繪映射加載失敗了，由於%s'%e)
    映射=None

def 生成html(包,衣=None,顏=None,位置=[0,0,1]):
    if 包==''or not 映射:
        return ''
    衣=衣 or '_默認'
    顏=顏 or '_默認'
    if len(位置)==2:
        位置.append(1)
    位置=tuple(位置)

    if not os.path.isdir('%s/%s'%(立繪路徑,包)):
        try:
            包名='%s/%s.psd'%(立繪路徑,包)
            psd拆包.拆包(包名)
        except:
            logging.warning('拆包「%s」時出錯了' % 包名)
            return '' 
    with open('%s/%s/位置.yaml'%(立繪路徑,包),encoding='utf8') as f:
        d=yaml.load(f)
    人物=映射[包]

    tot=''
    tot+="<div style='position:relative; left:%d; top:%d; transform:scale(%.2f);'>\n" %位置
    try:
        for 物件 in 人物['衣'][衣][::-1]+人物['顏'][顏][::-1]:
            if 物件:
                x,y=d[物件]['x'],d[物件]['y']
                tot+=" <img src='%s/%s/%s.png' style='position:absolute; left:%d; top:%d;'/>\n" %(相對網頁路徑,包,物件,x,y)
    except Exception as e:
        if 配置['嚴格模式']:
            raise e
        else:
            logging.warning('生成立繪時出錯了。'+e.__repr__())
    tot+='</div>\n'
    return tot

if __name__=='__main__':
    with open('1.html','w',encoding='utf8') as f:
        f.write(生成html('靈夢',顏='笑'))