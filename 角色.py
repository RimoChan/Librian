import yaml
import os
import psd拆包
from 環境 import 配置,工程路徑

角色表={}

class 角色:
    def __init__(self, 名字, 立繪表=None):
        self.衣圖層=立繪表['衣']
        self.顏圖層=立繪表['顏']
        self.固有縮放=立繪表.get('縮放',1)
        self.名字=名字
        角色表[self.名字]=self
        self.現顏='_默認'
        self.現衣='_默認'
        self.現特效=None
    @property
    def 現衣圖層(self):
        return self.衣圖層[self.現衣 or '_默認']
    @property
    def 現顏圖層(self):
        return self.顏圖層[self.現顏 or '_默認']
    
    def __repr__(self):
        return f'角色({self.名字}->[衣:{self.衣圖層}],[顏:{self.顏圖層}])  '
        
with open(f'{配置["psd路徑"]}/映射.yaml',encoding='utf8') as f:
    映射=yaml.load(f)
    if 映射:
        for i in 映射: 
            角色(i,映射[i])
            if not os.path.isdir('%s/%s'%(配置["圖片路徑"],i)):
                psd拆包.拆包(f'{配置["psd路徑"]}/{i}.psd',配置["圖片路徑"])
    for i in os.listdir(配置["psd路徑"]):
        if i.endswith('.png'):
            前名=os.path.basename(os.path.splitext(i)[0])
            if not os.path.isdir('%s/%s'%(配置["圖片路徑"],前名)):
                全名=os.path.join(配置["psd路徑"],i)
                psd拆包.png假裝拆包(全名,配置["圖片路徑"])
            角色(前名,{
                '衣':{'_默認':['_']},
                '顏':{'_默認':[]},
            })