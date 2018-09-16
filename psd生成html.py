import os
import logging
import random
import yaml
from 環境 import 配置,工程路徑

import psd拆包

相對網頁路徑=os.path.join("../%s" %工程路徑,配置['立繪文件夾'])
立繪路徑=os.path.join(工程路徑,配置['立繪文件夾'])
try:
    with open('%s/映射.yaml' %立繪路徑,encoding='utf8') as f:
        映射=yaml.load(f)
except Exception as e: 
    logging.warning('立繪立即被停用。立繪映射加載失敗了，由於%s'%e)
    映射=None

def 位置轉html(位置):
    return f'left:{位置[0]}; top:{位置[1]}; transform:scale({位置[2]});'

def 生成html(包,衣=None,顏=None,位置=[0,0,1],上次生成=None):
    if 包==''or not 映射:
        return ''
    衣=衣 or '_默認'
    顏=顏 or '_默認'
    if len(位置)==2:
        位置.append(1)

    if not os.path.isdir('%s/%s'%(立繪路徑,包)):
        try:
            包名='%s/%s.psd'%(立繪路徑,包)
            psd拆包.拆包(包名)
        except:
            logging.warning('拆包「%s」時出錯了' % 包名)
            return '' 
    with open('%s/%s/位置.yaml'%(立繪路徑,包),encoding='utf8') as f:
        d=yaml.load(f)
    人物配件=映射[包]
    類=[]
    css=''
    if 包 not in 上次生成:
        類.append('淡入')
    elif 上次生成[包]!=位置:
        原位置=上次生成[包]
        新位置=位置
        print(原位置,新位置)
        臨時名='移動'+str(random.randint(0,999999))
        動畫名='_'+臨時名
        css+='@keyframes %s { 0%% { %s;}100%% { %s;} }' % (動畫名,位置轉html(原位置),位置轉html(新位置))
        css+='.%s { animation: %s 0.4s;animation-fill-mode:forwards; }' % (臨時名,動畫名)
        類.append(臨時名)
        
    頭html='<style>%s</style>' % css
    人物html=''
    人物html+=f"<div class='{' '.join(類)}' style='position:relative;{位置轉html(位置)}'>\n"
    try:
        for 物件 in 人物配件['衣'][衣][::-1]+人物配件['顏'][顏][::-1]:
            if 物件:
                x,y=d[物件]['x'],d[物件]['y']
                人物html+=" <img src='%s/%s/%s.png' style='position:absolute; left:%d; top:%d;'/>\n" %(相對網頁路徑,包,物件,x,y)
    except Exception as e:
        if 配置['嚴格模式']:
            raise e
        else:
            logging.warning('生成立繪時出錯了。'+e.__repr__())
    人物html+='</div>\n'
    return 頭html+人物html

if __name__=='__main__':
    with open('1.html','w',encoding='utf8') as f:
        f.write(生成html('靈夢',顏='笑'))