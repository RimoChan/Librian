import re

正則組={
    '^> *(?P<函數>\S*)(?P<參數表>(.*))$':{
        '參數表':{
            '(?P<a>(((?<=").*?(?="))|(((?<= )|(?<=^))([^" ]+?)(?=( |$)))))':None
            }
        }
    ,
    '^={3,} *(?P<插入圖>.*)$':
        None
    ,
    '^(?P<名>.+?)(\|(?P<代>.+?))? *(\((?P<顏>.+?)\))? *「(?P<語>.*?)」$':
        None
    ,
    '^(?P<鏡頭>[\\+\\-])(?P<內容>.*)$':
        None
    ,
    '^(?P<名>.+?)(\|(?P<代>.+?))? (\((?P<顏>.+?)\))$':
        None
    ,
    '^(?P<名>.+?)(\|(?P<代>.+?))? (\((?P<顏>.+?)\))?(?P<多行起始>「)$':
        None
    ,
    '^(?P<多行終焉>」)$':
        None
    ,
    '^#(?P<註釋>.*)$':
        None
    ,
    '^\\*(?P<躍點>.*)$':
        None
    ,
    '^(?!(.+?)(\|(.+?))? (\((.+?)\))?)(?P<旁白>[^>#\\*\\+\\-\\=」].*)$':
        None    
}

def 遞歸re(s, start=正則組):
    d=[]
    for i in start:
        單位 = re.finditer(i, s) 
        for j in 單位:
            gd=j.groupdict()
            d.append(gd)
            if start[i]:
                for k in gd:
                    if k in start[i]:
                        gd[k]=遞歸re(gd[k],start[i][k])
    return d
    
def py狀態(g,自):
            code=''
            while True:
                q=next(g)
                l=遞歸re(q)
                if l and l[0].get('函數', '')=='endpy':
                    break
                code+=q
            自['代碼']=code

def 多行文本狀態(g,自):
        txt=''
        while True:
            q=next(g).lstrip().rstrip()
            if q=='」':
                break
            txt+=q+'\n'
        txt=txt.rstrip('\n')
        自['語']=txt

class j棧(list):
    def __init__(self):
        self.append([])
    
    @property
    def 尾(self):
        return self[-1]
    
    @property
    def 尾句(self):
        return self[-1][-1]

def 編譯(f):
    棧=j棧()
    g=iter(f.readlines())
    for s in g:
        if not re.search('\\S',s):
            棧.尾句['之後的空白']=棧.尾句.get('之後的空白',0)+1
            continue

        自={}
        自['縮進數']=len(s)-len(s.lstrip(' '))
        if 自['縮進數']>0 and 自['縮進數']>棧.尾句['縮進數']:
            棧.尾句['子']=[]
            棧.append(棧.尾句['子'])

        if 棧.尾:
            while 自['縮進數']<棧.尾句['縮進數']:
                棧.pop()
            if 棧.尾句['縮進數']!=自['縮進數']:
                raise Exception('層次錯誤')

        s=s.lstrip(' ')
        s=s.rstrip('\r').rstrip('\n')
        

        d=遞歸re(s)
        if len(d)==0:
            raise Exception('『%s 』無法匹配'%s)
        if len(d)>1:
            print(d)
            raise Exception('『%s 』匹配過多'%s)
        自.update(d[0])

        if 自.get('函數', '')=='py':
            py狀態(g,自)
        if '多行起始' in 自:
            多行文本狀態(g,自)

        棧.尾.append(自)
    return 棧[0]

def 印(q):
    for i in q:
        if '子' in i:
            t=i['子']
            del i['子']
            print(' '*i['縮進數'],end='')
            del i['縮進數']
            print(i)
            印(t)
        else:
            print(' '*i['縮進數'],end='')
            del i['縮進數']
            print(i)
    
if __name__=='__main__':
    with open('1.play',encoding='utf8') as f:
        印(編譯(f))
        # print(編譯(f))
