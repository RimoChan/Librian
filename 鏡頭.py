from psd生成html import 生成html
import 立繪
from 環境 import 配置
import logging

語者 = ''

默認位置 = 配置['默認立繪位置']

鏡頭對應 = {}

上次位置 = {}


class 鏡頭:
    def __init__(self, 所有位置):
        self.所有位置 = 所有位置
        for 人, 位置 in 所有位置.items():
            鏡頭對應[人] = self
            if len(位置) == 2:
                位置.append(1)

    def 統合(self):
        global 上次位置
        t = {}
        for 人 in self.所有位置:
            位置 = self.所有位置[人]
            t[人] = {'位置': 位置, '動作': None, '語': False}
            if 人 not in 上次位置:
                t[人]['動作'] = ('淡入',)
            elif 上次位置[人] != 位置:
                原位置 = 上次位置[人]
                t[人]['動作'] = ('移動', 原位置, 位置)
            if 人 == 語者:
                t[人]['語'] = True
        上次位置 = {}
        for 人 in self.所有位置:
            上次位置[人] = self.所有位置[人]
        return t

    def 拆解(self):
        return [立繪.人物拆解(人, 參數) for 人, 參數 in self.統合().items()]

    def 轉html(self):
        tot = ''
        try:
            for 人 in self.拆解():
                if 人:
                    tot += 生成html(人)
        except Exception as e:
            if 配置['嚴格模式']:
                raise e
            logging.warning('立繪立即被停用，因爲立繪生成出現問題了「%s」。' % e.__repr__())
            self.轉html = lambda: None
        return tot

    def __repr__(self):
        return str(self.所有位置)

    def __bool__(self):
        return bool(self.所有位置)


空鏡頭 = 鏡頭({})


def 查詢(人):
    if 人 not in 鏡頭對應:
        鏡頭({人: 默認位置[1][0]})
    return 鏡頭對應[人]

# ['潘大爺'] -> {'潘大爺':[0,0]}


def 生成鏡頭(x):
    if type(x) == dict:
        return 鏡頭(x)
    if type(x) == list:
        m = 默認位置[len(x)]
        a = dict(zip(x, m))
        return 鏡頭(a)


def 解除鏡頭(人):
    鏡頭對應[人] = 空鏡頭


if __name__ == '__main__':
    print(查詢('潘大爺'))
    print(空鏡頭)
