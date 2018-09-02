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
    '^(?P<名>.+?)(\|(?P<代>.+?))? (\((?P<顏>.+?)\))?(?P<語>「.*?」)$':
        None
    ,
    '^(?P<鏡頭>[\\+\\-])(?P<內容>.*)$':
        None
    ,
    '^(?P<名>.+?)(\|(?P<代>.+?))? (\((?P<顏>.+?)\))$':
        None
    ,
    '^#(?P<註釋>.*)$':
        None
    ,
    '^\\*(?P<躍點>.*)$':
        None
    ,
    '^(?!(.+?)(\|(.+?))? (\((.+?)\))?)(?P<旁白>[^>#\\*\\+\\-\\=].*)$':
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
    
def 編譯(f):
    a=[]
    g=iter(f.readlines())
    for s in g:
        s=s.rstrip('\r').rstrip('\n')
        if not re.search('\\S',s):
            a.append({'空行':None})
            continue
        d=遞歸re(s)
        if len(d)==0:
            raise Exception('『%s 』無法匹配'%s)
        if len(d)>1:
            print(d)
            raise Exception('『%s 』匹配過多'%s)
        d=d[0]
        if d.get('函數', '')=='py':
            code=''
            while True:
                q=next(g)
                l=遞歸re(q)
                if l and l[0].get('函數', '')=='endpy':
                    break
                code+=q
            d['代碼']=code
        a.append(d)
    return a
    
if __name__=='__main__':
    with open('1.play',encoding='utf8') as f:
        for i in 編譯(f):
            print(i)