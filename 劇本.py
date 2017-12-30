import sys
import os
import logging
import json
import pickle
import re, shlex
import yaml

from 環境 import 配置,工程路徑
import 鏡頭

class 讀者():
    def __init__(self):
        self.劇本棧=[open('%s/%s' %(工程路徑,配置['劇本入口']),encoding='utf-8')]
        self.箱庭={'goto':self.跳轉, 'push':self.棧跳轉, 'choice':self.產生選項}
        self.重置()
        self.步進()

    @property
    def 劇本文件(self):
        return self.劇本棧[-1]
    def 次行(self):
        return self.劇本文件.readline()
    @property
    def 當前狀態(self):
        return {'info':self.info,
                'word':self.word,
                'name':self.name,
                'ch'  :鏡頭.查詢(self.ch).轉html(),
                'bg'  :self.bg,
                'bgm' :self.bgm,
                'cg'  :self.cg,
                'choice' :[i[0] for i in self.選項]
            }

#————————————————————————————
#S/L方法
    def 存檔(self,path):
        with open(path,'wb') as f:
            pickle.dump([self.info_dict(),[self.文件展開(i) for i in self.劇本棧]] ,f)
    def 讀檔(self,path):
        with open(path,'rb') as f:
            data=pickle.load(f)
            self.unpack_info(data[0])
            self.劇本棧=[self.文件收縮(i) for i in data[1]]

    def 文件展開(self,file):
        return [file.name,file.tell()]
    def 文件收縮(self,file):
        f=open(file[0],encoding='utf8')
        f.seek(file[1])
        return f
    def 信息解包(self,info):
        self.info=info['info']
        self.word=info['word']
        self.name=info['name']
        self.ch  =info['ch']
        self.bg  =info['bg']
        self.bgm =info['bgm']
        self.cg  =info['cg']

#——————————————————————————————————————————————
#劇本控制(箱庭內可調用)
    def 跳轉(self,path=None,lable=None,彈=True):
        現名=self.劇本文件.name
        if path==None:
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
        self.選項=d

#——————————————————————————————————————————————
    def 有效次行(self):    #獲得劇本一行字
        if not self.劇本棧:
            return '【所有的劇本都結束了】'
        while True:
            text=self.次行()
            if text=='':
                self.劇本棧.pop()
                return self.有效次行()
            s=text.replace('\r','').replace('\n','').replace('\ufeff','')
            if s and s[-1]=='\\':
                s=s[:-1]+'\n'+self.有效次行()
            if s:
                try:
                    logging.debug('從%s中取到了 `%s` 。'%(self.劇本文件.name.split('/')[-1],s))
                except:
                    logging.debug('有unicode字元……')
                return s
        
    def 重置(self): 
        self.info=''
        self.word=''
        self.name=''
        self.ch=''
        self.bg=''
        self.bgm=''
        self.face=''
        self.cg=None
        self.選項=()
        
    def 步進(self):    
        if self.選項: return
        self.info=''
        text=self.有效次行()
        if text[:3]=='###':
            if text[3]=='#':
                cut='cut.jpg'
            else:
                cut=text[3:]
            self.重置()
            logging.debug('章節: %s'% cut )
            self.info=('cut', cut )
        elif text[0]=='#':
            參數 = shlex.split(text[1:])
            f=參數[0]
            if f=='VIDEO':
                self.重置()
                self.info=('video',參數[2])
                return
            if f=='BG':  self.bg =參數[1]
            if f=='BGM': self.bgm=參數[1]
            if f=='CG':  self.cg =參數[1]
            if f=='py':  self.進入py模式()
            if not self.選項:
                self.步進()
        elif text[0]=='+':
            d=yaml.load(text[1:])
            鏡頭.鏡頭(d)
            if not self.選項:
                self.步進()
        else:
            匹配結果 = re.search(配置['對話模式'], text) 
            if 匹配結果:
                d=匹配結果.groupdict()
                self.word = d['語']
                self.ch   = d['名']
                鏡頭.顏對應[self.ch]=d['顏']
                self.name = d['代'] or d['名']
            else:
                self.word = text
                self.ch   = ''
                self.name = ''
            
    def 進入py模式(self):
        tot=''
        while True:
            s=self.次行()
            if s[:6]=='#endpy': break
            tot+=s
        exec(tot,self.箱庭)


讀者=讀者()
