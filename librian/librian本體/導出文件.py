import os
import re
import logging
import argparse

import opencc

from Librian虛擬機 import 讀者
from Librian虛擬機 import 角色

cc = opencc.OpenCC('t2s')

此處 = os.path.dirname(os.path.abspath(__file__))


class 虛狀態:
    def __init__(self):
        self.額外信息 = ()
        self.內容 = {}

    def 導出(self):
        return {'內容': self.內容, '額外信息': self.額外信息}


class 虛讀者(讀者.讀者):
    def __init__(self, 初始劇本, 簡化字=False):
        super().__init__(初始劇本)
        self.簡化字 = 簡化字

    def 步進(self):
        self.狀態 = 虛狀態()
        s = self.下一句()
        類型 = s['類型']
        if 類型 == '終焉':
            self.狀態.額外信息 = ('終焉',)
        if 類型 in ('註釋', '躍點'):
            self.狀態.內容 = f'<span class="{類型}">{s[類型]}</span>\n'
        if 類型 == '函數調用':
            self.狀態.內容 = f'<span class="函數調用">{s["原文"]}</span>\n'
        if 類型 == '插入圖':
            self.狀態.內容 = f'<div class="插入">{s["插入圖"]}</div>'
        if 類型 == '旁白':
            旁白 = self.打標點(self.化(s["旁白"]))
            self.狀態.內容 = f'<p class="旁白">{旁白}</p>\n'
        if 類型 == '人物操作':
            人物名 = s['人物名']
            目標 = s['目標']
            if s['操作符'] == '+':
                self.狀態.內容 = f'<p class="人物操作">{self.化(人物名)} + {self.化(目標)}</p>\n'
            if s['操作符'] == '|':
                角色.取角色(人物名).顯示名字 = s['目標']
                self.狀態.內容 = ''
        if 類型 in ('人物對話', '人物表情'):
            替代顯示名字 = 角色.取角色(s['名']).顯示名字
            名字 = s['代'] or 替代顯示名字 or s['名']
            self.狀態.內容 = f'<p><span class="代 {s["名"]}">{self.化(名字)}</span>'
            if s['顏']:
                self.狀態.內容 += f'<span class="顏">{s["顏"]}</span>'
            if 類型 == '人物對話':
                self.狀態.內容 += f'<span class="語">{self.化(s["語"])}</span>'
            self.狀態.內容 += f'</p>'

        if '之後的空白' in s:
            self.狀態.內容 += '<br/>\n' * s['之後的空白']

    def 化(self, s):
        if self.簡化字:
            return cc.convert(s)
        return s

    def 打標點(self, 句):
        句 = re.sub('([，。？！…——])', '<span class="標點">\\1</span>', 句)
        句 = re.sub('(「.*?」)', '<span class="引用">\\1</span>', 句)
        return 句

    def 導出html(self, 帶css=False):
        head = f'<meta charset="utf8"/>\n'
        if 帶css:
            for css in 參數.css:
                head += f'<link rel="stylesheet" href="{css}"/>\n'

        return head + self.body內容()

    def body內容(self):
        t = list(self.迭代器())
        return '\n'.join([i['內容'] for i in t])


if __name__ == '__main__':
    參數 = argparse.ArgumentParser(description='劇本文件生成pdf')
    參數.add_argument('--play', type=str, required=True)
    參數.add_argument('--css', type=str, action='append')
    參數.add_argument('--out', type=str)
    參數.add_argument('--chs', action='store_true')
    參數.add_argument('--html', action='store_true')
    參數 = 參數.parse_args()

    if not 參數.css:
        參數.css = [os.path.join(此處, './資源/導出pdf用/紙樣式.css')]

    讀 = 虛讀者(參數.play, 參數.chs)
    if 參數.html:
        with open(參數.out, 'w', encoding='utf8') as f2:
            f2.write(讀.導出html(帶css=True))
    else:
        from weasyprint import HTML, CSS
        HTML(string=讀.導出html()).write_pdf(參數.out, stylesheets=參數.css)
