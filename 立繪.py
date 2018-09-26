import os
import yaml
import logging
from 環境 import 配置,工程路徑

相對網頁路徑=os.path.join("../%s" %工程路徑,配置['立繪文件夾'])
立繪路徑=os.path.join(工程路徑,配置['立繪文件夾'])
try:
    with open('%s/映射.yaml' %立繪路徑,encoding='utf8') as f:
        映射=yaml.load(f)
except Exception as e: 
    logging.warning('立繪立即被停用。立繪映射加載失敗了，由於%s'%e)
    映射=None
    
def 人物拆解(包,參數):
    衣=參數['衣']
    顏=參數['顏']
    位置=參數['位置']
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
    
    人={'圖層':[],'位置':位置,'動作':參數['動作']}
    for 物件 in 人物配件['衣'][衣][::-1]+人物配件['顏'][顏][::-1]:
        x,y=d[物件]['x'],d[物件]['y']
        人['圖層'].append(
            {'文件':'%s/%s/%s.png'%(相對網頁路徑,包,物件),
            '子位置':(x,y)}
        )
                
    return 人

