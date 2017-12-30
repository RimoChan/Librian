from psd生成html import 生成html

衣對應={}
顏對應={}

鏡頭對應={}
class 鏡頭:
    def __init__(self,所有位置):
        self.所有位置=所有位置
        for 人 in 所有位置:
            鏡頭對應[人]=self
    def 轉html(self):
        tot=''
        for 人 in self.所有位置:
            tot+=生成html(人,衣對應.get(人),顏對應.get(人),self.所有位置[人])
        return tot
空鏡頭=鏡頭({})

def 查詢(人):
    if 人 not in 鏡頭對應:
       鏡頭( {人:(300,0)} )
    return 鏡頭對應[人]
    
