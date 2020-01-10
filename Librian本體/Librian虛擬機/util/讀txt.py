import logging

import chardet


def 讀(txt):
    with open(txt, 'rb') as f:
        a = chardet.detect(f.read())
        # 我也很絕望啊！
        if a['encoding'] == 'GB2312':
            a['encoding'] = 'GBK'
    if a['confidence'] < 0.5:
        try:
            logging.warning(f'沒能自動識別「{txt}」的編碼，嘗試用默認編碼打開。')
            open(txt).read()
            return open(txt)
        except:
            logging.warning(f'沒能自動識別「{txt}」的編碼，嘗試用utf8打開。')
            return open(txt, encoding='utf8')
    else:
        return open(txt, encoding=a['encoding'])
