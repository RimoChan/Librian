import os
import json

import 環境
from 環境 import 工程路徑, 配置

import 劇本

讀者 = 劇本.讀者(f'{工程路徑}/{配置["劇本入口"]}')

圖片文件夾 = os.path.join(f'../{工程路徑}', 配置['圖片文件夾']).replace('\\', '/')
音樂文件夾 = os.path.join(f'../{工程路徑}', 配置['音樂文件夾']).replace('\\', '/')
自定css = os.path.join(f'../{工程路徑}', 配置['自定css']).replace('\\', '/')
主題css = os.path.join(f'主題', 配置['主題css'] + '.css').replace('\\', '/')

演出步 = json.dumps(list(讀者.迭代器()), ensure_ascii=False)

with open('./html/虛擬核心.js', 'w', encoding='utf-8') as f:
    f.write(f'作品名 = {配置["標題"].__repr__()};\n')
    f.write(f'邊界 = {int(配置["顯示繪圖邊界"])};\n')
    f.write(f'解析度 = {配置["主解析度"].__repr__()};\n')
    f.write(f'圖片文件夾 = {圖片文件夾.__repr__()};\n')
    f.write(f'音樂文件夾 = {音樂文件夾.__repr__()};\n')
    f.write(f'自定css = {自定css.__repr__()};\n')
    f.write(f'主題css = {主題css.__repr__()};\n')
    f.write(f'演出步 = {演出步};\n')
    f.write(f'虛擬核心已加載 = true;\n')
