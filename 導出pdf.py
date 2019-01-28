import os
import re
import argparse

import pdfkit
import opencc

import 編譯

此處 = os.path.dirname(os.path.abspath(__file__))

cc = opencc.OpenCC('t2s')
簡化字 = True

參數 = argparse.ArgumentParser(description='劇本文件生成pdf')
參數.add_argument('--css', type=str, default='./導出組件/樣式.html')
參數.add_argument('--play', type=str, required=True)
參數.add_argument('--out', type=str)
參數 = 參數.parse_args()

with open(os.path.join(此處, 參數.css), encoding='utf8') as f:
    頭 = f.read()


def 化(s):
    if 簡化字:
        return cc.convert(s)
    return s


def 打標點(句):
    句 = re.sub('([，。？！…——])', '<span class="標點">\\1</span>', 句)
    句 = re.sub('(「.*?」)', '<span class="引用">\\1</span>', 句)
    return 句


def 導出(f):
    html = 頭
    a = 編譯.編譯(f)
    for s in a:
        if '插入圖' in s:
            html += f'<hr/>{s["插入圖"]}<hr/>'
        if '旁白' in s:
            旁白 = 打標點(化(s["旁白"]))
            html += f'<span class="旁白">　　{旁白}</span><br/>\n'
        if '名' in s:
            代 = 化(s['代'] or s["名"])
            顏 = 化(s['顏'] or '')
            語 = 化(s.get('語', ''))
            html += f'<span class="代 {s["名"]}">　　{代}</span>'
            if 顏:
                html += f'<span class="顏">({顏})</span>'
            if 語:
                html += f'「<span class="語">{語}</span>」'
            html += f'<br/>'

        if '註釋' in s:
            html += f'<span class="註釋">{s["註釋"]}</span><br/>\n'
        if '空行' in s:
            html += '<br/>\n'

    return html


if __name__ == '__main__':
    if 參數.play:
        pdf = html = False
        if 參數.out is None:
            參數.out = 參數.play[:-5] + '.pdf'
            pdf = True
        elif 參數.out.endswith('pdf'):
            pdf = True
        elif 參數.out.endswith('pdf'):
            html = True

        with open(參數.play, encoding='utf8') as f:
            t = 導出(f)
            if html:
                with open(參數.out, 'w', encoding='utf8') as f2:
                    f2.write(導出(f))
            if pdf:
                pdfkit.from_string(t, 參數.out, options={
                    'margin-top': '0in',
                    'margin-right': '0in',
                    'margin-bottom': '0in',
                    'margin-left': '0in',
                    'encoding': 'UTF-8',
                })
            else:
                raise Exception('操你媽')
