import yaml
import os
import psd拆包
import logging
from 環境 import 配置, 工程路徑

角色表 = {}

def 取角色(名字):
    if 名字 in 角色表:
        return 角色表[名字]
    else:
        return 角色(名字)

class 角色:
    def __init__(self, 名字, 立繪表=None):
        self.有立繪 = bool(立繪表)
        if self.有立繪:
            self.衣圖層 = 立繪表['衣']
            self.顏圖層 = 立繪表['顏']
            self.固有縮放 = 立繪表.get('縮放', 1)
            self.現顏 = '_默認'
            self.現衣 = '_默認'
            self.現特效 = None
        else:
            logging.warning(f'新建了沒有立繪的角色「{名字}」')
        self.名字 = 名字
        self.顯示名字 = None
        角色表[self.名字] = self

    @property
    def 現衣圖層(self):
        try:
            return self.衣圖層[self.現衣 or '_默認']
        except:
            logging.warning(f'衣「{self.現衣}」沒有配置。')
            return []
    @property
    def 現顏圖層(self):
        try:
            return self.顏圖層[self.現顏 or '_默認']
        except:
            logging.warning(f'顏「{self.現顏}」沒有配置。')
            return []

    def __repr__(self):
        return f'角色{"|"+self.顯示名字 if self.顯示名字 else ""}({self.名字}->[衣:{self.衣圖層}],[顏:{self.顏圖層}])  '


with open(f'{配置["psd路徑"]}/映射.yaml', encoding='utf8') as f:
    映射 = yaml.load(f)
    if 映射:
        for i in 映射:
            角色(i, 映射[i])
            if not os.path.isdir('%s/%s' % (配置["圖片路徑"], i)):
                psd拆包.拆包(f'{配置["psd路徑"]}/{i}.psd', 配置["圖片路徑"])
    for i in os.listdir(配置["psd路徑"]):
        if i.endswith('.png'):
            前名 = os.path.basename(os.path.splitext(i)[0])
            if not os.path.isdir('%s/%s' % (配置["圖片路徑"], 前名)):
                全名 = os.path.join(配置["psd路徑"], i)
                psd拆包.png假裝拆包(全名, 配置["圖片路徑"])
            角色(前名, {
                '衣': {'_默認': ['_']},
                '顏': {'_默認': []},
            })
