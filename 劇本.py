import sys
import os
import logging
import json
import pickle
import re, shlex
import yaml

from 環境 import 配置,工程路徑
import 鏡頭
import 編譯
import 讀txt

def 硬命令(s):
    return 命令('>'+s)
class 命令():
    def __init__(self,d):
        self.函數=d['函數']
        self.參數=[i['a'] for i in d['參數表']]
        if '代碼' in d:
            self.代碼=d['代碼']
    def 執行(self,讀者):
        try:
            函數=eval('self.'+self.函數)
            函數(*([讀者]+self.參數))
        except Exception as e:
            if 配置['嚴格模式']:
                raise e
            s='%s(%s)' % (self.函數,', '.join(self.參數))
            logging.warning('在劇本中執行方法「%s」時遇到了意外%s'%(s,e.__repr__()))

    #——————————————————————————————
    def py(self,讀者):
        exec(self.代碼,讀者.箱庭)
    def BG(self,讀者,bg):
        讀者.狀態.背景=bg
    def BGM(self,讀者,bgm,音量=1):
        讀者.狀態.背景音樂=bgm,音量
    def CG(self,讀者,cg=None):
        讀者.狀態.CG=cg
    def VIDEO(self,讀者,v):
        讀者.狀態.重置()
        讀者.狀態.額外信息=('video',v)
    def WRAP(self,讀者,*li):
        包=lambda x: (lambda:讀者.棧跳轉(*x[1:]))
        li=[yaml.load(i) for i in li]
        li=[(i[0],包(i)) for i in li]
        讀者.產生選項(*li)


class 狀態():
    def __init__(self):
        self.額外信息=''
        self.話語=''
        self.名字=''
        self.人物=''
        self.背景=''
        self.背景音樂=('',1)
        self.CG=''
        self.選項=()

    def 導出(self,html=True):
        鏡頭.語者=self.名字
        if html:
            ch=鏡頭.查詢(self.人物).轉html()
        else:
            ch=鏡頭.查詢(self.人物).拆解()
        return {'info':self.額外信息,
                'word':self.話語,
                'name':self.名字,
                'ch'  :ch,
                'bg'  :self.背景,
                'bgm' :self.背景音樂,
                'cg'  :self.CG,
                'choice' :[i[0] for i in self.選項]
            }

    def 重置(self):
        self.__init__()
        
class 劇本():
    def __init__(self,內容,名):
        self.內容=內容
        self.指針=0
        self.名=名
    def 下一句(self):
        if self.指針>=len(self.內容):
            return None
        r=self.內容[self.指針]
        self.指針+=1
        return r

class 讀者():
    def __init__(self):
        self.劇本棧=[self.編譯(f'{工程路徑}/{配置["劇本入口"]}')]
        self.箱庭={'goto':self.跳轉, 'push':self.棧跳轉, 'choice':self.產生選項}
        self.狀態=狀態()
        self.狀態.重置()
        鏡頭.鏡頭對應={}
    
    def 下一句(self):
        if not self.劇本棧:
            return {'旁白':'<small>【演出結束了】</small>','終焉':True}
        s=self.劇本文件.下一句()
        if s:
            return s
        else:
            self.劇本棧.pop()
            return self.下一句()

    def 編譯(self,s):
        f=讀txt.讀(s)
        return 劇本(編譯.編譯(f),s)

    @property
    def 劇本文件(self):
        return self.劇本棧[-1]
        
#————————————————————————————
#S/L方法
    def 存檔(self,path):
        with open(path,'wb') as f:
            pickle.dump({'狀態':self.狀態,
                         '衣對應':鏡頭.衣對應,
                         '顏對應':鏡頭.顏對應,
                         '鏡頭對應':鏡頭.鏡頭對應,
                         '劇本棧':self.劇本棧,
                         }
                         ,f)
    def 讀檔(self,path):
        try:
            with open(path,'rb') as f:
                data=pickle.load(f)
                鏡頭.衣對應=data['衣對應']
                鏡頭.顏對應=data['顏對應']
                鏡頭.鏡頭對應=data['鏡頭對應']
                self.狀態=data['狀態']
                self.狀態.額外信息=('load',)
                self.劇本棧=data['劇本棧']
        except Exception as e:
            logging.warning('讀檔失敗……因爲%s'%e)

#——————————————————————————————————————————————
#劇本控制
    def 跳轉(self,path=None,lable=None,彈=True):
        現名=self.劇本文件.名
        if not path:
            path=現名
        else:
            path='%s/%s' %(os.path.dirname(現名),path)
        
        if 彈: 
            self.劇本棧.pop()
        self.劇本棧.append(self.編譯(path))
        if lable:
            while True:
                t=self.劇本文件.下一句()
                if t is None:
                    raise Exception(f'沒有找到躍點「{lable}」')
                if '躍點' in t and t['躍點']==lable:
                    break

    def 棧跳轉(self,path=None,lable=None):
        self.跳轉(path,lable,彈=False)

    def 產生選項(self,*d):
        d=[(i[0],i[1]) for i in d]
        self.狀態.選項=d

#——————————————————————————————————————————————
    def 步進(self):    
        if self.狀態.選項: return
        self.狀態.額外信息=''
        
        s=self.下一句()
            
        if any([i in s for i in ('註釋','躍點')]):
            self.步進()
        if '函數' in s:
            命令(s).執行(self)
            if not self.狀態.選項:
                self.步進()
        #不是H的圖……
        if '插入圖' in s:
            logging.debug('插入圖: %s'% s['插入圖'] )
            self.狀態.額外信息=('cut', s['插入圖'] )
        if '終焉' in s:
            self.狀態.額外信息=('終焉',)
        if '鏡頭' in s:
            if s['鏡頭']=='+':
                d=yaml.load(s['內容'])
                鏡頭.生成鏡頭(d)
                self.步進()
            elif s['鏡頭']=='-':
                鏡頭.解除鏡頭(yaml.load(s['內容']))
                self.步進()
        if '旁白' in s:
            self.狀態.話語 = s['旁白']
            self.狀態.名字 = ''
        if '名' in s:
            if '語' in s:
                鏡頭.顏對應[s['名']]=s['顏']
                if 鏡頭.查詢(s['名']) and self.狀態.人物!=s['名']:
                    self.狀態.人物 = s['名']
                self.狀態.話語 = s['語']
                self.狀態.名字 = s['代'] or s['名']
                logging.debug([s['名'],s['代'],s['顏'],s['語']].__str__())
            else:
                鏡頭.顏對應[s['名']]=s['顏']
                if 鏡頭.查詢(s['名']) and self.狀態.人物!=s['名']:
                    self.狀態.人物 = s['名']
                logging.debug([s['名'],s['代'],s['顏']].__str__())
                self.步進()

讀者=讀者()
if __name__=='__main__':
    for i in range(110):
        q=讀者.狀態.導出()
        del q['ch']
        print(q)
        讀者.步進()