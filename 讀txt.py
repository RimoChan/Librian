import chardet


def 讀(txt):
    with open(txt, 'rb') as f:
        a = chardet.detect(f.read())
    if a['confidence'] < 0.5:
        try:
            open(txt).read()
            return open(txt)
        except:
            return open(txt, encoding='utf8')
    else:
        return open(txt, encoding=a['encoding'])
