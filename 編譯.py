import re

正則組={
    '^> *(?P<原文>(?P<函數>\S*)(?P<參數表>(.*)))$':{
        '類型':'函數調用',
        '子樹':{
            '參數表':{
                '(?P<a>(((?<=").*?(?="))|(((?<= )|(?<=^))([^" ]+?)(?=( |$)))))':None
            }
        }
    },
    '^={3,} *(?P<插入圖>.*) *$':{
        '類型':'插入圖',
    },
    '^(?P<名>.+?)(\|(?P<代>.+?))?  *(\[(?P<特效>.+?)\])? *(\((?P<顏>.+?)\))? *「(?P<語>.*?)」 *$':{
        '類型':'人物對話',
    },
    '^(?P<名>.+?)(\|(?P<代>.+?))?  *(\[(?P<特效>.+?)\])? *(\((?P<顏>.+?)\)) *$':{
        '類型':'人物表情',
    },
    '^(?P<鏡頭>[\\+\\-]) *(?P<內容>.*)$':{
        '類型':'鏡頭',
    },
    '^(?P<名>.+?)(\|(?P<代>.+?))? (\((?P<顏>.+?)\))?(?P<多行起始>「)$':{
        '類型':'多行人物對話開始',
    },
    '^(?P<多行終焉>」)$':{
        '類型':'多行人物對話終焉',
    },
    '^#(?P<註釋>.*)$':{
        '類型':'註釋',
    },
    '^\\*(?P<躍點>.*)$':{
        '類型':'躍點'
    },
    '^(?!(.+?)(\|(.+?))?  *(\[(.+?)\])? *(\((.+?)\))? *「.*?」)(?!(.+?)(\|(.+?))?  *(\[(.+?)\])? *(\((.+?)\)))(?P<旁白>[^>#\\*\\+\\-\\=」].*)$':{
        '類型':'旁白'
    }#寫出來就看不懂了23333
}

def 遞歸re(s, start=正則組):
    d=[]
    for i in start:
        單位 = re.finditer(i, s)
        for j in 單位:
            gd=j.groupdict()
            d.append(gd)
            if isinstance(start[i],dict):
                gd['類型']=start[i]['類型']
            if start[i] is not None and '子樹' in start[i]:
                for k in start[i]['子樹']:
                    gd[k]=遞歸re(gd[k],start[i]['子樹'][k])
    return d
    
def 多行檢查(g,自,結束函數):
    內容=''
    while True:
        q=next(g)
        l=遞歸re(q)
        if l and 結束函數(l):
            break
        內容+=q
    return 內容

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
    return 生編譯(f.readlines())

def 生編譯(s):
    棧=j棧()
    g=iter(s)
    for s in g:
        if not re.search('\\S',s):
            if 棧.尾:
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
            自['代碼']=多行檢查(g,自,lambda x:x[0].get('函數', '')=='endpy')
        if 自.get('函數', '')=='js':
            自['代碼']=多行檢查(g,自,lambda x:x[0].get('函數', '')=='endjs')
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
