import os
import logging
import random
from 環境 import 配置, 工程路徑


def 位置轉html(位置):
    return f'left:{位置[0]}; top:{位置[1]}; transform:scale({位置[2]});'


def 生成html(參數):
    動作 = 參數['動作']
    位置 = 參數['位置']
    特效 = 參數['特效']
    類 = []
    css = ''
    if 特效:
        類.append(特效)
    if 動作:
        類.append(動作[0])
        if 動作[0] == '移動':
            原位置 = 動作[1]
            新位置 = 動作[2]
            臨時名 = '移動' + str(random.randint(0, 999999))
            動畫名 = '_' + 臨時名
            css += '@keyframes %s { 0%% { %s;}100%% { %s;} }' % (動畫名, 位置轉html(原位置), 位置轉html(新位置))
            css += '.%s { animation: %s 0.4s;animation-fill-mode:forwards; }' % (臨時名, 動畫名)
            類.append(臨時名)

    頭html = '<style>%s</style>' % css
    人物html = ''
    人物html += f"<div class='{' '.join(類)}' style='position:relative;{位置轉html(位置)}'>\n"
    try:
        for 層 in 參數['圖層']:
            人物html += " <img src='%s' style='position:absolute; left:%d; top:%d;'/>\n" % (層['文件'], *層['子位置'])

    except Exception as e:
        if 配置['嚴格模式']:
            raise e
        else:
            logging.warning('生成立繪時出錯了。' + e.__repr__())
    人物html += '</div>\n'
    return 頭html + 人物html
