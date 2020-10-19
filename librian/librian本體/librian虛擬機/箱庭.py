import os
import logging

import liber

from . import 讀者


class 箱庭:
    def __init__(self, 關聯讀者):
        self.關聯讀者 = 關聯讀者
        self.箱庭內容 = {
            'goto': self.跳轉,
            'call': self.棧跳轉,
            'choice': self.產生選項,
            'fusion': self.同化,
            'adv_end': self.演出終了,
            
            '跳轉': self.跳轉,
            '調用': self.棧跳轉,
            '產生選項': self.產生選項,
            '同化': self.同化,
            '演出終了': self.演出終了,
            
            '跳转': self.跳轉,
            '调用': self.棧跳轉,
            '产生选项': self.產生選項,
            '同化': self.同化,
            '演出终了': self.演出終了,
        }

    def 跳轉(self, path=None, lable=None, 彈=True):
        現名 = self.關聯讀者.劇本文件.名
        if not path:
            path = 現名
        else:
            path = '%s/%s' % (os.path.dirname(現名), path)

        if 彈:
            self.關聯讀者.劇本棧.pop()
        self.關聯讀者.劇本棧.append(self.關聯讀者.編譯(path))
        if lable:
            while True:
                t = self.關聯讀者.劇本文件.下一句()
                if t is None:
                    raise Exception(f'沒有找到躍點「{lable}」')
                if '躍點' in t and t['躍點'] == lable:
                    break

    def 棧跳轉(self, path=None, lable=None):
        self.跳轉(path, lable, 彈=False)

    def 產生選項(self, *li):
        li = [(i[0], i[1]) for i in li]
        self.關聯讀者.狀態.選項 = li

    def 同化(self, s):
        self.關聯讀者.劇本棧.append(讀者.劇本(liber.load(s), '_字串'))

    def 演出終了(self):
        self.關聯讀者.劇本棧 = []
