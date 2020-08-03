import logging
import copy

import cloudpickle as pickle
import yaml
import sass
import liber

from librian.librian_util import 讀txt

from . import 鏡頭
from . import 角色
from . import 命令
from . import 箱庭



class 狀態:
    def __init__(self):
        self.話語 = None      # str
        self.名字 = None      # str
        self.語者 = None      # str
        self.人物 = None      # str
        self.背景 = None      # [圖名, 淡入時間, 位置, 漸變方法]
        self.背景音樂 = None   # [音樂名, 音量]
        self.效果音 = None    # [音樂名, 音量]
        self.插入圖 = None     # str
        self.cg = None        # [圖名, 淡入時間, 漸變方法]
        self.視頻 = None      # [視頻名, 可以跳過]
        self.js = None        # str
        self.html = None      # str
        self.選項 = []
        self.特效表 = {}
        self.額外信息 = ()
        self.源 = []

    def 導出(self):
        鏡頭.語者 = self.語者
        if self.人物:
            立繪 = 鏡頭.查詢(self.人物).拆解()
        else:
            立繪 = []
        if self.語者:
            表情 = 角色.取角色(self.語者).現顏
        else:
            表情 = ''
        快照 = {
            '話語': self.話語,
            '名字': self.名字,
            '立繪': 立繪,
            '表情': 表情,
            '語者': self.語者,
            '背景': self.背景,
            '背景音樂': self.背景音樂,
            '效果音': self.效果音,
            '插入圖': self.插入圖,
            'cg': self.cg,
            '視頻': self.視頻,
            'js': self.js,
            'html': self.html,
            '選項': [i[0] for i in self.選項],
            '特效表': copy.deepcopy(self.特效表),
            '額外信息': self.額外信息,
            '源': self.源,
        }
        self.清除臨時狀態()
        return 快照

    def 重置(self):
        self.__init__()

    def 清除臨時狀態(self):
        self.js = None
        self.插入圖 = None
        self.效果音 = None
        self.視頻 = None
        self.額外信息 = ()
        self.源 = []


class 劇本:
    def __init__(self, 內容, 名):
        self.內容 = 內容
        self.指針 = 0
        self.名 = 名

    def 下一句(self):
        if self.指針 >= len(self.內容):
            return None
        r = self.內容[self.指針]
        self.指針 += 1
        return r


class 讀者:
    def __init__(self, 初始劇本):
        self.劇本棧 = [self.編譯(初始劇本)]
        self.狀態 = 狀態()
        self.狀態.重置()
        self.箱庭 = 箱庭.箱庭(self)
        鏡頭.鏡頭對應 = {}

    @property
    def 劇本文件(self):
        return self.劇本棧[-1]

    def 下一句(self):
        if not self.劇本棧:
            return {'旁白': '<small>【演出結束了】</small>', '類型': '終焉'}
        s = self.劇本文件.下一句()
        if s:
            return s
        else:
            self.劇本棧.pop()
            return self.下一句()

    def 編譯(self, s):
        with 讀txt.讀(s) as f:
            return 劇本(liber.load(f), s)

    def 步進(self, 防止終焉=False):
        s = self.下一句()
        if s['類型'] == '終焉' and 防止終焉:
            return True
        self.狀態.源.append(copy.copy(s))
        讀者句控制(self, s['類型'], s)

    def 迭代器(self):
        while True:
            self.步進()
            s = self.狀態.導出()
            if s['額外信息'] and s['額外信息'][0] == '終焉':
                break
            else:
                yield s

    def 從一而終(self, 劇本):
        self.__init__(劇本)
        logging.debug(self.劇本文件.內容)
        while True:
            if self.步進(防止終焉=True):
                break

    def 存檔(self, 路徑, 存檔信息=None):
        虛擬機狀態 = {
            '讀者狀態': self.狀態,
            '角色表': 角色.角色表,
            '鏡頭對應': 鏡頭.鏡頭對應,
            '劇本棧': self.劇本棧,
            '箱庭': self.箱庭,
        }
        with open(路徑, 'wb') as f:
            pickle.dump({
                '虛擬機狀態': 虛擬機狀態,
                '存檔信息': 存檔信息
            }, f)

    def 讀檔(self, 路徑):
        try:
            with open(路徑, 'rb') as f:
                data = pickle.load(f)['虛擬機狀態']
                角色.角色表 = data['角色表']
                鏡頭.鏡頭對應 = data['鏡頭對應']
                self.狀態 = data['讀者狀態']
                self.狀態.額外信息 = ('load',)
                self.劇本棧 = data['劇本棧']
                self.箱庭 = data['箱庭']
        except Exception as e:
            logging.warning('讀檔失敗……')
            logging.exception(e)


class 讀者句控制:
    def __init__(self, 讀者, 類型, 參數表):
        del 參數表['類型']
        if '縮進數' in 參數表:
            del 參數表['縮進數']
        if '之後的空白' in 參數表:
            del 參數表['之後的空白']
        logging.debug(類型)
        logging.debug(參數表)
        讀者句控制.__getattribute__(self, 類型)(讀者, **參數表)

    @staticmethod
    def 註釋(讀者, 註釋):
        讀者.步進()

    @staticmethod
    def 躍點(讀者, 躍點):
        讀者.步進()

    @staticmethod
    def 函數調用(讀者, 函數, 參數表, 原文):
        命令.命令(函數, 參數表, 原文).執行(讀者)
        if not 讀者.狀態.選項:
            讀者.步進()

    @staticmethod
    def 插入代碼(讀者, 代碼類型, 代碼內容):
        if 代碼類型 in ['', 'py', 'python']:
            exec(代碼內容, 讀者.箱庭.箱庭內容)
        elif 代碼類型 in ['js', 'javascript']:
            讀者.狀態.js = 代碼內容
        elif 代碼類型 in ['html']:
            讀者.狀態.html = 代碼內容
        elif 代碼類型 in ['css']:
            讀者.狀態.html = f'<style>{代碼內容}</style>'
        elif 代碼類型 in ['sass']:
            讀者.狀態.html = f'<style>{sass.compile(string=代碼內容, indented=True)}</style>'
        elif 代碼類型 in ['scss']:
            讀者.狀態.html = f'<style>{sass.compile(string=代碼內容)}</style>'
        else:
            raise Exception(f'『{代碼類型}』代碼類型不明白。')
        if not 讀者.狀態.選項:
            讀者.步進()

    @staticmethod
    def 插入圖(讀者, 插入圖):
        logging.debug('插入圖: %s' % 插入圖)
        讀者.狀態.插入圖 = 插入圖

    @staticmethod
    def 終焉(讀者, 旁白):
        讀者.狀態.額外信息 = ('終焉',)
        讀者.狀態.話語 = 旁白
        讀者.狀態.名字 = ''
        讀者.狀態.語者 = ''

    @staticmethod
    def 鏡頭(讀者, 鏡頭符號, 內容):
        if 鏡頭符號 == '+':
            try:
                d = yaml.load(內容)
                鏡頭.生成鏡頭(d)
            except Exception as e:
                logging.exception(e)
                logging.warning(f'鏡頭「{內容}」的內容不正確。')
            讀者.步進()
        elif 鏡頭符號 == '-':
            try:
                鏡頭.解除鏡頭(yaml.load(內容))
            except Exception as e:
                logging.exception(e)
                logging.warning(f'鏡頭「{內容}」的內容不正確。')
            讀者.步進()

    @staticmethod
    def 旁白(讀者, 旁白):
        讀者.狀態.話語 = 旁白
        讀者.狀態.名字 = ''
        讀者.狀態.語者 = ''

    @staticmethod
    def 人物操作(讀者, 人物名, 目標, 操作符):
        if 操作符 == '+':
            角色.取角色(人物名).現衣 = 目標
        if 操作符 == '|':
            角色.取角色(人物名).顯示名字 = 目標
        讀者.步進()

    @staticmethod
    def 人物對話(讀者, 名, 顏, 語, 代, 特效):
        人物 = 讀者句控制._表情變化(讀者, 名, 顏, 代, 特效)
        讀者.狀態.話語 = 語
        讀者.狀態.名字 = 代 or 人物.顯示名字 or 名
        讀者.狀態.語者 = 名
        logging.debug([名, 代, 顏, 語].__str__())

    @staticmethod
    def 人物表情(讀者, 名, 顏, 代, 特效):
        人物 = 讀者句控制._表情變化(讀者, 名, 顏, 代, 特效)
        logging.debug([名, 代, 顏].__str__())
        讀者.步進()

    @staticmethod
    def 選項(讀者, 選項名, 文件, 位置):
        讀者.狀態.選項.append([選項名, lambda: 讀者.箱庭.棧跳轉(文件, 位置)])
        if 讀者.劇本文件.指針 < len(讀者.劇本文件.內容):
            if 讀者.劇本文件.內容[讀者.劇本文件.指針]['類型'] == '選項':
                讀者.步進()

    @staticmethod
    def _表情變化(讀者, 名, 顏, 代, 特效):
        人物 = 角色.取角色(名)
        人物.現顏 = 顏
        if 特效:
            人物.現特效 = [特效]
        else:
            人物.現特效 = []
        if 鏡頭.查詢(名) and 讀者.狀態.人物 != 名:
            讀者.狀態.人物 = 名
        return 人物
