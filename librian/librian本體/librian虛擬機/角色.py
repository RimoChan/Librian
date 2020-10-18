import os
import logging

import yaml
from rimo_utils import good_open

from . import 虛擬機環境


角色表 = {}


def 初始化():    
    if '了' in dir(初始化):
        return
    初始化.了 = True
    導入有立繪的角色()


def 取角色(名字):
    初始化()
    if 名字 in 角色表:
        return 角色表[名字]
    else:
        return 角色(名字)


def 導入有立繪的角色():
    try:
        with good_open(虛擬機環境.psd立繪路徑 / '映射.yaml') as f:
            映射表 = yaml.load(f, Loader=yaml.BaseLoader)
            if 映射表:
                for 角色名 in 映射表:
                    角色(角色名, 映射表[角色名])
            for i in os.listdir(虛擬機環境.psd立繪路徑):
                if i.endswith('.png'):
                    前名 = os.path.basename(os.path.splitext(i)[0])
                    角色(前名, 使用png=True)
    except Exception as e:
        logging.warning('角色立繪沒有導入。')
        logging.exception(e)


class 角色:
    def __init__(self, 名字: str, 立繪表: dict = None, 使用png=False):
        self.名字 = 名字
        self.顯示名字 = None
        self.使用png = 使用png
        self.有立繪 = bool(立繪表 or 使用png)
        if not self.有立繪:
            logging.warning(f'新建了沒有立繪的角色「{名字}」')
        if 立繪表:
            self.衣圖層 = 立繪表['衣']
            self.顏圖層 = 立繪表['顏']
            self.固有縮放 = 立繪表.get('縮放', 1)
            self.現顏 = None
            self.現衣 = None
            self.現特效 = None

        assert self.名字 not in 角色表
        角色表[self.名字] = self

    @property
    def 現衣圖層(self):
        try:
            return self.衣圖層[self.現衣 or '_默認']
        except Exception:
            logging.warning(f'衣「{self.現衣}」沒有配置。')
            return []

    @property
    def 現顏圖層(self):
        try:
            return self.顏圖層[self.現顏 or '_默認']
        except Exception:
            logging.warning(f'顏「{self.現顏}」沒有配置。')
            return []

    def __repr__(self):
        return f'角色{"|"+self.顯示名字 if self.顯示名字 else ""}({self.名字}->[衣:{self.衣圖層}],[顏:{self.顏圖層}])'
