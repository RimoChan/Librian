import logging

from . import 立繪
from . import 虛擬機環境

語者 = ''

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
            t[人] = {
                '位置': 位置,
                '語': 人 == 語者
            }
        上次位置 = {}
        for 人 in self.所有位置:
            上次位置[人] = self.所有位置[人]
        return t

    def 拆解(self):
        立繪組 = [立繪.人物拆解(人, 參數) for 人, 參數 in self.統合().items()]
        return [立繪 for 立繪 in 立繪組 if 立繪 is not None]

    def __repr__(self):
        return str(self.所有位置)

    def __bool__(self):
        return bool(self.所有位置)


空鏡頭 = 鏡頭({})


def 查詢(人):
    if 人 not in 鏡頭對應:
        鏡頭({人: 虛擬機環境.默認立繪位置[1][0]})
    return 鏡頭對應[人]

# ['潘大爺'] -> {'潘大爺':[0,0]}


def 生成鏡頭(x):
    if type(x) == dict:
        return 鏡頭(x)
    if type(x) == list:
        m = 虛擬機環境.默認立繪位置[len(x)]
        a = dict(zip(x, m))
        return 鏡頭(a)


def 解除鏡頭(人):
    鏡頭對應[人] = 空鏡頭


if __name__ == '__main__':
    print(查詢('潘大爺'))
    print(空鏡頭)
