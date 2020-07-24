import logging

from librian.librian_util import 文件

from . import 虛擬機環境


def 別名適用(x):
    for i, f in list(x.__dict__.items()):
        if '別名' in dir(f):
            for 各別名 in f.別名:
                x.__class__.__setattr__(x, 各別名, f)
    return x


def 別名(*li):
    def f2(x):
        x.別名 = li
        return x
    return f2


@別名適用
class 命令:
    def __init__(self, 函數, 參數表, 原文):
        self.函數 = 函數
        self.參數 = [i['a'] for i in 參數表]
        self.原文 = 原文

    def 執行(self, 讀者):
        try:
            t = eval(self.原文, {
                i: (lambda *li, f=f: f(self, 讀者, *li))
                for i, f in self.__class__.__dict__.items()
                if i not in ('py', 'js') and i[0] != '_'
            })
            if t is not None:
                raise Exception('不太對勁……')
        except:
            try:
                函數 = eval('self.' + self.函數)
                函數(*([讀者] + self.參數))
            except AttributeError as e:
                raise AttributeError('沒有可用的函數「%s」。' % self.函數)
            except Exception as e:
                s = '%s(%s)' % (self.函數, ', '.join(self.參數))
                logging.warning(f'在劇本中執行方法「{s}」時遇到了意外。')
                logging.exception(e)

    # ——————————————————————————————

    @別名('背景')
    def BG(self, 讀者, bg, 淡入時間=1, 位置='0% 0%', 漸變方法='_淡出'):
        bg = 文件.補充擴展名(bg, ['webp', 'png', 'jpg'], 虛擬機環境.工程路徑 / 虛擬機環境.圖片文件夾)
        讀者.狀態.背景 = bg, 淡入時間, 位置, 漸變方法

    @別名('特效')
    def EF(self, 讀者, 標識, 類名=None):
        if 類名 is None and 標識 in 讀者.狀態.特效表:
            del 讀者.狀態.特效表[標識]
        else:
            讀者.狀態.特效表[標識] = 類名

    @別名('背景音樂', '背景音乐')
    def BGM(self, 讀者, 文件名, 音量=1):
        if 文件名 is None or 文件名 == 'None':
            讀者.狀態.背景音樂 = None
        else:
            文件名 = 文件.補充擴展名(文件名, ['opus', 'mp3', 'ogg'], 虛擬機環境.工程路徑 / 虛擬機環境.音樂文件夾)
            讀者.狀態.背景音樂 = 文件名, 音量

    def CG(self, 讀者, cg, 淡入時間=1, 漸變方法='_淡出'):
        if cg is None or cg == 'None':
            讀者.狀態.cg = None
        else:
            cg = 文件.補充擴展名(cg, ['webp', 'png', 'jpg'], 虛擬機環境.工程路徑 / 虛擬機環境.圖片文件夾)
            讀者.狀態.cg = cg, 淡入時間, 漸變方法

    @別名('效果音')
    def SE(self, 讀者, 文件名, 音量=1):
        文件名 = 文件.補充擴展名(文件名, ['opus', 'mp3', 'ogg'], 虛擬機環境.工程路徑 / 虛擬機環境.音樂文件夾)
        讀者.狀態.效果音 = 文件名, 音量

    @別名('視頻', '视频')
    def VIDEO(self, 讀者, 文件名, 可以跳過=False):
        讀者.狀態.重置()
        讀者.狀態.視頻 = 文件名, 可以跳過
