import sys
import os
import logging
import yaml
import shutil

import 環境
環境.設定工程路徑('./project/極夜所在的星之海')

from 環境 import 配置,工程路徑
from 劇本 import 讀者

臨時立繪文件夾=工程路徑+'/_臨時文件/'
輕文立繪文件夾=工程路徑+'/_輕文立繪/'

def 立繪壓平():
    try:
        os.mkdir(輕文立繪文件夾)
    except:
        None
    for root ,dirs ,files in os.walk(臨時立繪文件夾):
        r=os.path.relpath(root,臨時立繪文件夾)
        for i in files:
            if i.endswith('.png'):
                舊名=os.path.join(r,i)
                新名=r.replace('\\','_')+'_'+i
                shutil.copy(臨時立繪文件夾+舊名,輕文立繪文件夾+新名)
    
def 路徑變換(p):
    s=os.path.relpath(p, '../'+臨時立繪文件夾)
    s=s.replace('\\','_')[:-4]
    return s

def 輕立繪(ch):
    t=''
    if not ch:
        return t
    層數=1
    for 人 in ch:
        if not 人: continue
        縮放=人['位置'][2]
        for 圖 in 人['圖層']:
            圖["文件"]=路徑變換(圖["文件"])
            x=人['位置'][0]+圖['子位置'][0]*縮放
            y=人['位置'][1]+圖['子位置'][1]*縮放
            t+=f'@in CHR{層數} url={圖["文件"]} x={int(x)} y={int(y)} zoom={int(縮放*100)} \n@action CHR{層數} zoomcenter=(0,0)\n'
            層數+=1
    return t
def 輕立繪解除(ch):
    t=''
    if not ch:
        return t
    層數=1
    for 人 in ch:
        if not 人: continue
        for 圖 in 人['圖層']:
            t+=f'@in CHR{層數} url=None\n'
            層數+=1
    return t
    

def 輕句(q):
    t=''
    if q["bg"]:
        t+=f'@in BG1 url={q["bg"][:-4]}\n'
    t+=f'@dianame {q["name"]}\n'
    t+=輕立繪(q['ch'])
    t+=f'「{q["word"]}」[p]\n'
    t+=輕立繪解除(q['ch'])
    return f'\n{t}\n'
    
if __name__=='__main__':
    t=''
    t+='@msgdia\n'
    for i in range(10000):
        讀者.步進()
        q=讀者.狀態.導出(html=False)
        t+=輕句(q)
        if '終焉' in q['info']: break
    立繪壓平()
    with open('輕.txt','w',encoding='utf8') as f:
        f.write(t)