import os
import re
import argparse
import logging

from weasyprint import HTML, CSS

import opencc

import 編譯

此處 = os.path.dirname(os.path.abspath(__file__))

cc = opencc.OpenCC('t2s')
簡化字 = False

參數 = argparse.ArgumentParser(description='劇本文件生成pdf')
參數.add_argument('--play', type=str, required=True)
參數.add_argument('--css', type=str, action='append')
參數.add_argument('--out', type=str)
參數=參數.parse_args()

if not 參數.css:
    參數.css = [os.path.join(此處, './資源/導出pdf用/紙樣式.css')]

def 化(s):
    if 簡化字:
        return cc.convert(s)
    return s


def 打標點(句):
    句=re.sub('([，。？！…——])', '<span class="標點">\\1</span>', 句)
    句=re.sub('(「.*?」)', '<span class="引用">\\1</span>', 句)
    return 句


def 導出(f):
    head=f'''
    <head>
        <meta charset="utf8"/>
        {" ".join([f"<link rel='stylesheet' href='file:///{css}'/>" for css in 參數.css])}
    </head>
    '''
    logging.debug(head)
    body=''
    a=編譯.編譯(f)
    for s in a:
        類型=s['類型']
        if 類型 == '插入圖':
            body += f'<div class="插入">{s["插入圖"]}</div>'
        if 類型 == '旁白':
            旁白=打標點(化(s["旁白"]))
            body += f'<p class="旁白">{旁白}</p>\n'
        if 類型 == '人物對話':
            代=化(s['代'] or s["名"])
            顏=化(s['顏'] or '')
            語=化(s.get('語', ''))

            body += f'<p><span class="代 {s["名"]}">{代}</span>'
            if 顏:
                body += f'<span class="顏">{顏}</span>'
            if 語:
                body += f'<span class="語">{語}</span>'
            body += f'</p>'
        if 類型 == '註釋':
            body += f'<span class="註釋">{s["註釋"]}</span><br/>\n'
        if 類型 == '函數調用':
            body += f'<span class="函數調用">{s["原文"]}</span><br/>\n'
        if '之後的空白' in s:
            body += '<br/>\n' * s['之後的空白']

    return head + f'<body>{body}</body>'


if __name__ == '__main__':
    if 參數.play:
        pdf=html=False
        if 參數.out is None:
            參數.out=參數.play[:-5] + '.pdf'
            pdf=True
        elif 參數.out.endswith('pdf'):
            pdf=True
        elif 參數.out.endswith('pdf'):
            html=True

        with open(參數.play, encoding='utf8') as f:
            t=導出(f)
            if html:
                with open(參數.out, 'w', encoding='utf8') as f2:
                    f2.write(導出(f))
            if pdf:
                HTML(string=t).write_pdf(參數.out)
            else:
                raise Exception('操你媽')
