import sys
import os
import logging
import yaml
import shutil

import 環境
if __name__ == '__main__':
    環境.設定工程路徑('./project/極夜所在的星之海')

from 環境 import 配置, 工程路徑
import 劇本

臨時立繪文件夾 = 工程路徑 + '/_臨時立繪/'
輕文立繪文件夾 = 工程路徑 + '/_輕文立繪/'

輕文縮放 = 1280 / 配置['主解析度'][0]


def 立繪壓平():
    try:
        os.mkdir(輕文立繪文件夾)
    except:
        None
    for root, dirs, files in os.walk(臨時立繪文件夾):
        r = os.path.relpath(root, 臨時立繪文件夾)
        for i in files:
            if i.endswith('.png'):
                舊名 = os.path.join(r, i)
                新名 = r.replace('\\', '_') + '_' + i
                shutil.copy(臨時立繪文件夾 + 舊名, 輕文立繪文件夾 + 新名)


def 路徑變換(p):
    s = os.path.relpath(p, '../' + 臨時立繪文件夾)
    s = s.replace('\\', '_')[:-4]
    return s


def 輕立繪(ch):
    t = ''
    if not ch:
        return t
    層數 = 1
    for 人 in ch:
        if not 人:
            continue
        動作 = 人['動作']
        縮放 = 人['位置'][2]
        for 圖 in 人['圖層']:
            圖["文件"] = 路徑變換(圖["文件"])
            x = (人['位置'][0] + 圖['子位置'][0] * 縮放) * 輕文縮放
            y = (人['位置'][1] + 圖['子位置'][1] * 縮放) * 輕文縮放
            t += f'@in CHR{層數} url={圖["文件"]} x={x} y={y} zoom={縮放*輕文縮放*100} \n@action CHR{層數} zoomcenter=(0,0)\n'
            if 動作:
                if 動作[0] == '淡入':
                    t += f'@action CHR{層數} alpha=0 time=0\n'
                    t += f'@action CHR{層數} alpha=1 time=300\n'
                if 動作[0] == '移動':
                    原位置 = 動作[1]
                    新位置 = 動作[2]
                    原縮放 = 原位置[2]
                    原x = (原位置[0] + 圖['子位置'][0] * 原縮放) * 輕文縮放
                    原y = (原位置[1] + 圖['子位置'][1] * 原縮放) * 輕文縮放
                    新縮放 = 新位置[2]
                    新x = (新位置[0] + 圖['子位置'][0] * 新縮放) * 輕文縮放
                    新y = (新位置[1] + 圖['子位置'][1] * 新縮放) * 輕文縮放
                    t += f'@action CHR{層數} x={原x}\n'
                    t += f'@action CHR{層數} y={原y}\n'
                    t += f'@action CHR{層數} zoom={原縮放*輕文縮放*100}\n'
                    t += f'@action CHR{層數} x={新x} time=400\n'
                    t += f'@action CHR{層數} y={新y} time=400\n'
                    t += f'@action CHR{層數} zoom={新縮放*輕文縮放*100} time=400\n'

            層數 += 1
    return t


def 輕立繪解除(ch):
    t = ''
    if not ch:
        return t
    層數 = 1
    for 人 in ch:
        if not 人:
            continue
        for 圖 in 人['圖層']:
            t += f'@in CHR{層數} url=None\n'
            層數 += 1
    return t


當前bgm = ''


def 輕句(q):
    t = ''
    if q['info'] and q['info'][0] == 'cut':
        圖 = q['info'][1][:-4]
        t += f'@in EFX1 url={圖} alpha=0\n'
        t += f'@action EFX1 url={圖} alpha=1 time=1000\n'
        t += '[l]\n'
        t += f'@action EFX1 url={圖} alpha=0 time=2000\n'
        return f'\n{t}\n'

    bgm = q['bgm'][0]
    global 當前bgm
    if bgm != 當前bgm:
        當前bgm = bgm
        if bgm == 'None':
            t += '@stop BGM1 time=1000\n'
        else:
            t += f'@play BGM1 url="{bgm[:-4]}" time=1000\n'

    if q["bg"]:
        t += f'@in BG1 url={q["bg"][:-4]}\n'

    t += f'@dianame {q["name"]}\n'
    t += 輕立繪(q['ch'])
    if q['name']:
        t += f'「{q["word"]}」[p]\n'
    else:
        t += f'　　{q["word"]}[p]\n'
    t += 輕立繪解除(q['ch'])

    return f'\n{t}\n'


if __name__ == '__main__':
    t = ''
    t += '@msgdia\n'
    初讀者 = 劇本.讀者(f'{工程路徑}/{配置["劇本入口"]}')
    for i in range(99999):
        初讀者.步進()
        q = 初讀者.狀態.導出(html=False)
        t += 輕句(q)
        if '終焉' in q['info']:
            break
    立繪壓平()
    with open('輕.txt', 'w', encoding='utf8') as f:
        f.write(t)
