import sys
import os
import logging
import copy
import json
import pickle
import re, shlex
import yaml

from 環境 import 配置
import 鏡頭
import 編譯
import 讀txt

def 別名適用(x):
    print(dir(x))
    for i,f in list(x.__dict__.items()):
        if '別名' in dir(f):
            for 各別名 in f.別名:
                x.__class__.__setattr__(x,各別名,f)
    return x
def 別名(*li):
    def f2(x):
        x.別名=li
        return x
    return f2

@別名適用
class 命令():
    def __init__(self,d):
        self.函數=d['函數']
        self.參數=[i['a'] for i in d['參數表']]
        self.原文=d['原文']
        if '代碼' in d:
            self.代碼=d['代碼']
    def 執行(self,讀者):
        try:
            eval(self.原文,{
                i:(lambda *li,f=f:f(self,讀者,*li))
                    for i,f in self.__class__.__dict__.items() 
                        if i!='py' and i[0]!='_'
            })
        except:
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
    @別名('背景')
    def BG(self,讀者,bg):
        讀者.狀態.背景=bg
    @別名('背景音樂','背景音乐')
    def BGM(self,讀者,bgm,音量=1):
        讀者.狀態.背景音樂=bgm,音量
    def CG(self,讀者,cg=None):
        讀者.狀態.CG=cg
    @別名('視頻','视频')
    def VIDEO(self,讀者,v):
        讀者.狀態.重置()
        讀者.狀態.額外信息=('video',v)
    @別名('快捷選項','快捷选项')
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
        self.語者=''
        self.背景=''
        self.背景音樂=('',1)
        self.CG=''
        self.選項=()

    def 導出(self,html=True):
        鏡頭.語者=self.語者
        if self.人物:
            if html:
                ch=鏡頭.查詢(self.人物).轉html()
            else:
                ch=鏡頭.查詢(self.人物).拆解()
        else:
            ch=''
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
    def __init__(self,初始劇本):
        self.劇本棧=[self.編譯(初始劇本)]
        self.狀態=狀態()
        self.狀態.重置()
        self.箱庭={
            'goto':self.跳轉, 
            'call':self.棧跳轉, 
            'choice':self.產生選項,
            'fusion':self.同化,
            'adv_end':self.演出終了,
            '跳轉':self.跳轉, 
            '調用':self.棧跳轉,
            '產生選項':self.產生選項,
            '同化':self.同化,
            '演出終了':self.演出終了,
        }
        鏡頭.鏡頭對應={}
    
    def 下一句(self):
        if not self.劇本棧:
            return {'旁白':'<small>【演出結束了】</small>','類型':'終焉'}
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
    def 縮減箱庭(self):
        鏡箱庭=copy.copy(self.箱庭)
        鏡箱庭2=copy.copy(self.箱庭)
        for i,x in 鏡箱庭2.items():
            try:
                pickle.dumps(x)
            except:
                鏡箱庭.pop(i)
        return 鏡箱庭
    def 存檔(self,path):
        with open(path,'wb') as f:
            pickle.dump({'狀態':self.狀態,
                         '衣對應':鏡頭.衣對應,
                         '顏對應':鏡頭.顏對應,
                         '鏡頭對應':鏡頭.鏡頭對應,
                         '劇本棧':self.劇本棧,
                         '箱庭':self.縮減箱庭(),
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
                self.箱庭=data['箱庭']
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
    
    def 同化(self,s):
        self.劇本棧.append(劇本(編譯.生編譯(iter([s])),'_字串'))
        
    def 演出終了(self):
        self.劇本棧=[]

#——————————————————————————————————————————————
    def 步進(self):    
        if self.狀態.選項: return
        self.狀態.額外信息=''
        
        s=self.下一句()
        類型=s['類型']
        if 類型 in ('註釋','躍點'):
            self.步進()
        if 類型=='函數調用':
            命令(s).執行(self)
            if not self.狀態.選項:
                self.步進()
        if 類型=='插入圖':
            logging.debug('插入圖: %s'% s['插入圖'] )
            self.狀態.額外信息=('cut', s['插入圖'] )
        if 類型=='終焉':
            self.狀態.額外信息=('終焉',)
            self.狀態.話語 = s['旁白']
            self.狀態.名字 = ''
            self.狀態.語者 = ''
        if 類型=='鏡頭':
            if s['鏡頭']=='+':
                d=yaml.load(s['內容'])
                鏡頭.生成鏡頭(d)
                self.步進()
            elif s['鏡頭']=='-':
                鏡頭.解除鏡頭(yaml.load(s['內容']))
                self.步進()
        if 類型=='旁白':
            self.狀態.話語 = s['旁白']
            self.狀態.名字 = ''
            self.狀態.語者 = ''
        if 類型=='人物對話':
            鏡頭.顏對應[s['名']]=s['顏']
            if 鏡頭.查詢(s['名']) and self.狀態.人物!=s['名']:
                self.狀態.人物 = s['名']
            self.狀態.話語 = s['語']
            self.狀態.名字 = s['代'] or s['名']
            self.狀態.語者 = s['名']
            logging.debug([s['名'],s['代'],s['顏'],s['語']].__str__())
        if 類型=='人物表情':
            鏡頭.顏對應[s['名']]=s['顏']
            if 鏡頭.查詢(s['名']) and self.狀態.人物!=s['名']:
                self.狀態.人物 = s['名']
            logging.debug([s['名'],s['代'],s['顏']].__str__())
            self.步進()

if __name__=='__main__':
    初讀者=讀者()
    for i in range(110):
        q=初讀者.狀態.導出()
        del q['ch']
        print(q)
        初讀者.步進()