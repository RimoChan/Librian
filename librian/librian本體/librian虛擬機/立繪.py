import copy

from . import 角色


def 人物拆解(人名: str, 镜头參數):
    人 = 角色.取角色(人名)

    if not 人.有立繪:
        return None

    位置 = copy.deepcopy(镜头參數['位置'])
    語 = 镜头參數['語']

    if 人.使用png:
        return {
            '使用png': True,
            '位置': 位置,
            '特效': 人.現特效,
            '名字': 人名,
        }

    位置[2] *= 人.固有縮放

    衣配件 = 人.現衣圖層[::-1]
    顏 = 人.現顏圖層
    if isinstance(顏, dict):
        if 語:
            顏 = 顏['_語']
        else:
            顏 = 顏['_默認']
    顏配件 = 顏[::-1]

    return {
        '圖層': 衣配件 + 顏配件,
        '位置': 位置,
        '特效': 人.現特效,
        '名字': 人名,
    }
