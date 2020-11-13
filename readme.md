# Librian: 簡明強大的 Galgame | Visual Novel 引擎

[![](https://img.shields.io/github/stars/RimoChan/Librian.svg)](https://github.com/RimoChan/Librian/stargazers)
[![](https://img.shields.io/badge/platform-windows%20%7C%20linux-%23989898)](https://en.wikipedia.org/wiki/Microsoft_Windows)
[![](https://img.shields.io/github/release/RimoChan/librian.svg)](https://github.com/RimoChan/Librian/releases)
[![](https://img.shields.io/codacy/grade/cc567bfd3e374eb494825aae3ce3e7cf)](https://www.codacy.com/manual/s60481235/Librian?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=RimoChan/Librian&amp;utm_campaign=Badge_Grade)
[![](https://img.shields.io/github/license/RimoChan/Librian.svg)](https://github.com/RimoChan/Librian/blob/master/LICENSE)
![Librian2.jpg](https://cdn.jsdelivr.net/gh/RimoChan/librian/文檔/Librian2.jpg)    

——來像 Markdown 一樣寫 Galgame 劇本吧！

Librian 是容易上手的 Galgame 引擎，Librian 由 Python 和 JavaScript 編寫而成，基於 CEFPython 前端。  

Librian 適用於快速高效的 ADV 實現，能將你的奇思妙想迅速轉換爲成果——你只需提供素材文件和简单的劇本就能做出 Galgame！

Librian 是面向劇本的引擎，賣點是: 

-   輕快便捷的原型開發。
-   用戶友好。
-   高度可擴展性。

## 一分鐘的演示視頻

[![視頻佔位](https://cdn.jsdelivr.net/gh/RimoChan/librian/文檔/視頻佔位.jpg)](https://librian.net/視頻/轉.webm)

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

準備好立繪和背景後，運行 Librian 主程序並啓動工程——演出是這樣的效果。  
![圖1](https://cdn.jsdelivr.net/gh/RimoChan/librian/文檔/樣例_潘大爺.jpg)

## 中文文檔

如果你想瞭解詳細的使用方法，可以直接閱讀 Librian 的中文文檔——[https://doc.librian.net](https://doc.librian.net/site/主頁.html)。

你可以輕鬆客製化你的遊戲，包括特效、畫面樣式、甚至聯網，快來探索吧！

## 快速上手

+ 直接下載打包的 [release 版本](https://github.com/RimoChan/Librian/releases) <sub>(推薦)</sub>。
    - release 版本也附帶了 [librian 面板](https://github.com/RimoChan/Librian)。

+ 或者使用 `pip install librian` 來安裝 librian。
    - 這需要本地 Python 爲 3.6 或 3.7 版本
    - 它不太穩定，所以最好先更新一下 pip 和 setuptools，要是裝不上我也沒辦法……

## Liber 分析器

Liber 分析器是 Librian 用來分析劇本語言 Liber 的工具。  
如果你想要開發自己的 Galgame 引擎或者做一些很酷的事情，它會有所助益。

它的倉庫在 <https://github.com/librian-center/liber-language>

你可以直接用 `pip install liber` 來安裝它。

## 援交～

QQ 群「Librian蘿莉會所」: 618775838。

如果你需要使用幫助，或者對 Librian 和 Galgame 製作有興趣，或者想觀看蘿莉色圖，都可以來這裏討論。  
總之，一起玩就行啦。

## 贊助

如果你覺得 Librian 對你的工作或學習有幫助，歡迎給作者介紹一些可愛的女朋友。

最好是蘿莉，要那種會坐在腿上蹭蹭，喊「歐尼醬」的。
