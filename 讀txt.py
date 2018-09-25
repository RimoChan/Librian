import chardet

def 讀(txt):
    with open(txt,'rb') as f:
        a=chardet.detect(f.read())
    print(a)
    if a['confidence']<0.5:
        return open(txt)
    else: 
        return open(txt,encoding=a['encoding'])
