from psd生成html import 生成html
from 環境 import 配置
import logging

默認位置=配置['默認立繪位置']

衣對應={}
顏對應={}
鏡頭對應={}

上次生成={}

class 鏡頭:
    def __init__(self,所有位置):
        self.所有位置=所有位置
        for 人 in 所有位置:
            鏡頭對應[人]=self
    def 轉html(self):
        tot=''
        try:
            global 上次生成
            for 人 in self.所有位置:
                tot+=生成html(人,衣對應.get(人),顏對應.get(人),self.所有位置[人],上次生成)
            上次生成={}
            for 人 in self.所有位置:
                上次生成[人]=self.所有位置[人]
        except Exception as e:   
            if 配置['嚴格模式']:
                raise e    
            logging.warning('立繪立即被停用，因爲立繪生成出現問題了「%s」。' %e.__repr__())
            self.轉html=lambda:None
        return tot
    def __repr__(self):
        return str(self.所有位置)
    def __bool__(self):
        return bool(self.所有位置)
        
空鏡頭=鏡頭({})

def 查詢(人):
    if 人 not in 鏡頭對應:
       鏡頭( {人:默認位置[1][0]} )
    return 鏡頭對應[人]
    
#['潘大爺'] -> {'潘大爺':[0,0]}
def 生成鏡頭(x):
    if type(x)==dict:
        return 鏡頭(x)
    if type(x)==list:
        m=默認位置[len(x)]
        a=dict(zip(x,m))
        return 鏡頭(a)
def 解除鏡頭(人):
    鏡頭對應[人]=空鏡頭

if __name__=='__main__':
    print(查詢('潘大爺'))
    print(空鏡頭)