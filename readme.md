# Librian: 簡明強大的 Galgame | Visual Novel 引擎

[![](https://img.shields.io/github/stars/RimoChan/Librian.svg)](https://github.com/RimoChan/Librian/stargazers)
[![](https://img.shields.io/badge/platform-windows%20%7C%20linux-%23989898)](https://en.wikipedia.org/wiki/Microsoft_Windows)
[![](https://img.shields.io/github/release/RimoChan/librian.svg)](https://github.com/RimoChan/Librian/releases)
[![](https://img.shields.io/github/downloads/RimoChan/librian/total.svg)](https://github.com/RimoChan/Librian/releases)
[![](https://img.shields.io/codacy/grade/cc567bfd3e374eb494825aae3ce3e7cf)](https://www.codacy.com/manual/s60481235/Librian?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=RimoChan/Librian&amp;utm_campaign=Badge_Grade)
[![](https://img.shields.io/github/license/RimoChan/Librian.svg)](https://github.com/RimoChan/Librian/blob/master/LICENSE)
![Librian2.jpg](./文檔/Librian2.jpg)    
[简体中文](readme-chs.md)

——來像Markdown一樣寫Galgame劇本吧！

Librian是容易上手的Galgame引擎，Librian由Python和JavaScript編寫而成，基於CEFPython前端。  

Librian適用於快速高效的ADV實現，能將你的奇思妙想迅速轉換爲成果——你只需提供素材文件和简单的劇本就能做出Galgame！

Librian是面向劇本的引擎，賣點是: 

-   輕快便捷的原型開發。
-   用戶友好。
-   高度可擴展性。

## 一分鐘的演示視頻

[![視頻佔位](./文檔/視頻佔位.jpg)](https://librian.it/視頻/轉.webm)

## 劇本格式

```liber
> BG 中庭.jpg
+ [舟舟, 潘大爺]
中庭。潘大爺在散步。
舟舟 (微笑)「啊！校長！終於找到你了！」
潘大爺 「舟舟！來得正是時候！」
潘大爺 (微笑)「來看看我新發明的催眠調教裝置！」
舟舟 (驚)「真有這種發明！？」
```

不需要任何其他標記或代碼，一小段劇本就完成了。  

準備好立繪和背景後，運行Librian主程序並啓動工程——演出是這樣的效果。  
![圖1](文檔/樣例_潘大爺.jpg)

## 中文文檔

如果你想瞭解詳細的使用方法，可以直接閱讀Librian的中文文檔——[https://doc.librian.it](https://doc.librian.it/site/主頁.html)。

你可以輕鬆定製你的遊戲，包括特效、畫面樣式、甚至聯網，快來探索吧！

## 快速上手

方便起見的話，Windows用戶可以直接下載打包的[release版本](https://github.com/RimoChan/Librian/releases)使用。

如果你持「不讀說明書主義」，可以: 

1.  安裝python3.6
2.  pip install -r requirements.txt
3.  python3 librian_panel.py

此外，你也可以根據[中文文檔](https://doc.librian.it/site/主頁.html)的指示來安裝。

## Liber分析器

Liber分析器是Librian用來分析劇本語言Liber的工具。  
如果你想要開發自己的Galgame引擎或者做一些很酷的事情，它會有所助益。

你可以直接用 `pip install liber` 來安裝它。

## 援交～

試着建了QQ群: 618775838。

如果你需要使用幫助，或者對Librian和galgame製作有興趣，<sub>或者想觀看蘿莉圖片</sub>，都可以來這裏討論。  
總之，一起玩就行啦。

## 贊助

如果你覺得Librian對你的工作或學習有幫助，歡迎給作者介紹一些可愛的女朋友。

最好是蘿莉，要那種會坐在腿上蹭蹭，喊「歐尼醬」的。
