import sys
import os
import logging
import json
import pickle
import re, shlex
import yaml

from 環境 import 配置,工程路徑
import 鏡頭

def 硬命令(s):
    return 命令('>'+s)
class 命令():
    def __new__(cls,s):
        if s[0]!='>':
            return None
        return super().__new__(cls)
    def __init__(self,text):
        t=shlex.split(text[1:])
        self.方法=t[0]
        self.參數=t[1:]
    def __str__(self):
        return '[命令]%s(%s)'%(self.方法,', '.join(self.參數))
    def __eq__(self,b):
        return self.__str__()==b.__str__()
    def 執行(self,讀者):
        try:
            方法=eval('self.'+self.方法)
            方法(*([讀者]+self.參數))
        except Exception as e:
            s='%s(%s)' % (self.方法,', '.join(self.參數))
            logging.warning('在劇本中執行方法「%s」時遇到了意外%s'%(s,e))

    #——————————————————————————————
    def py(self,讀者):
        讀者.進入py模式()
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

    def 導出(self):
        return {'info':self.額外信息,
                'word':self.話語,
                'name':self.名字,
                'ch'  :鏡頭.查詢(self.人物).轉html(),
                'bg'  :self.背景,
                'bgm' :self.背景音樂,
                'cg'  :self.CG,
                'choice' :[i[0] for i in self.選項]
            }

    def 重置(self):
        self.__init__()

class 讀者():
    def __init__(self):
        self.劇本棧=[open('%s/%s' %(工程路徑,配置['劇本入口']),encoding='utf-8')]
        self.箱庭={'goto':self.跳轉, 'push':self.棧跳轉, 'choice':self.產生選項}
        self.狀態=狀態()
        self.狀態.重置()
        self.步進()

    @property
    def 劇本文件(self):
        return self.劇本棧[-1]
    def 次行(self):
        return self.劇本文件.readline()

#————————————————————————————
#S/L方法
    def 存檔(self,path):
        with open(path,'wb') as f:
            pickle.dump({'狀態':self.狀態,
                         '衣對應':鏡頭.衣對應,
                         '顏對應':鏡頭.顏對應,
                         '鏡頭對應':鏡頭.鏡頭對應,
                         '劇本棧':[self.文件展開(i) for i in self.劇本棧],
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
                self.劇本棧=[self.文件收縮(i) for i in data['劇本棧']]
        except Exception as e:
            logging.warning('讀檔失敗……因爲%s'%e)

    def 文件展開(self,file):
        return [file.name,file.tell()]
    def 文件收縮(self,file):
        f=open(file[0],encoding='utf8')
        f.seek(file[1])
        return f

#——————————————————————————————————————————————
#劇本控制
    def 跳轉(self,path=None,lable=None,彈=True):
        現名=self.劇本文件.name
        if not path:
            path=現名
        else:
            path='%s/%s' %(os.path.dirname(現名),path)
        
        if 彈: 
            self.劇本棧.pop()
        self.劇本棧.append(open(path,encoding='utf-8'))
        if lable:
            while True:
                t=self.次行()
                if not t or t[:-1]==lable:
                    break

    def 棧跳轉(self,path=None,lable=None):
        self.跳轉(path,lable,彈=False)

    def 產生選項(self,*d):
        d=[(i[0],i[1]) for i in d]
        self.狀態.選項=d

#——————————————————————————————————————————————
    def 有效次行(self):    #獲得劇本一行字
        if not self.劇本棧:
            return '<small>【所有的劇本都結束了】</small>'
        while True:
            text=self.次行()
            if text=='':
                self.劇本棧.pop()
                return self.有效次行()
            s=text.replace('\r','').replace('\n','').replace('\ufeff','')
            if s and s[-1]=='\\':
                s=s[:-1]+'\n'+self.有效次行()
            if s:
                logging.debug('從%s中取到了 `%s` 。'%(self.劇本文件.name.split('/')[-1],s))
                return s
        
    def 步進(self):    
        if self.狀態.選項: return
        self.狀態.額外信息=''
        text=self.有效次行()
        令=命令(text)
        if 令:
            令.執行(self)
            if not self.狀態.選項:
                self.步進()
        elif text[:3]=='###':
            if text[3]=='#':
                cut='cut.jpg'
            else:
                cut=text[3:]
            self.狀態.重置()
            logging.debug('章節: %s'% cut )
            self.狀態.額外信息=('cut', cut )
        elif text[0]=='#':
            self.步進()
        elif text[0]=='+':
            d=yaml.load(text[1:])
            鏡頭.生成鏡頭(d)
            self.步進()
        elif text[0]=='-': 
            鏡頭.解除鏡頭(yaml.load(text[1:]))
            self.步進()
        else:
            通常結果 = re.search(配置['對話模式']['通常'], text)
            隱式結果 = re.search(配置['對話模式']['隱式'], text)
            if 通常結果:
                d=通常結果.groupdict()
                鏡頭.顏對應[d['名']]=d['顏']
                if 鏡頭.查詢(d['名']) and self.狀態.人物!=d['名']:
                    self.狀態.人物 = d['名']
                self.狀態.話語 = d['語']
                self.狀態.名字 = d['代'] or d['名']
                logging.debug([d['名'],d['代'],d['顏'],d['語']].__str__())
            elif 隱式結果:
                d=隱式結果.groupdict()
                鏡頭.顏對應[d['名']]=d['顏']
                if 鏡頭.查詢(d['名']) and self.狀態.人物!=d['名']:
                    self.狀態.人物 = d['名']
                logging.debug([d['名'],d['代'],d['顏']].__str__())
                self.步進()
            else:
                self.狀態.話語 = text
                self.狀態.名字 = ''
            
    def 進入py模式(self):
        tot=''
        while True:
            s=self.次行()
            if 命令(s)==硬命令('endpy'): break
            tot+=s
        exec(tot,self.箱庭)


讀者=讀者()
