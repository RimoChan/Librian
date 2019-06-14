# ![](資源/Librian小.png)Librian: 簡明強大的 Galgame | Visual Novel 引擎

![Librian2.jpg](./資源/Librian2.jpg)

![](https://img.shields.io/github/stars/RimoChan/Librian.svg)
![](https://img.shields.io/badge/platform-windows-blueviolet.svg)
![](https://img.shields.io/github/release/RimoChan/librian.svg)
![](https://img.shields.io/github/downloads/RimoChan/librian/total.svg)
![](https://img.shields.io/github/license/RimoChan/Librian.svg)

[读简化字版本](readme_chs.md)

Librian是一个非常容易上手的 Galgame | Visual Novel 引擎。   

Librian適用於快速高效的adv實現，能將你的奇思妙想迅速轉換爲成果——你只需提供素材文件和简单的劇本就能觀賞adv演出！

Librian是面向劇本的引擎，賣點是: 

-   清晰自然的劇本，提升你的寫作速度。
-   自動分配立繪，無需手工操作且兼容性強。
-   可以嵌入python，具有無限大的擴展性。
-   導出美觀的PDF，與原畫老師輕鬆交流。
-   附帶語義文件，讓現代字編輯器如虎添翼。

Librian由python和HTML編寫而成，基於CEFPython和wxPython前端。

## 演示視頻

[![視頻佔位](./資源/視頻佔位.png)](https://www.zhihu.com/video/1075418256290131968)  

## 劇本格式

    > BG 機房.png
    排成列的高過人的金屬箱子的微光，讓黑暗的空間浸染上了青色。
    Librian 6，似乎是被這樣稱呼的。
    儘管嗡嗡的機械噪聲從耳膜的左邊穿到右邊，又從右邊穿到左邊，像是劣質的鐘錶一樣描述着時間的流逝。但時間就像是反反覆覆地停止了一樣。
    潘大爺 (嘆)「美妙，真是美妙。」
    不如說，時間不停止的話就是極大的失禮。
    潘大爺 (笑)「把我的理論獻給你吧………不，到現在爲止還剩什麼理論呢……」
    潘大爺 (笑)「來吧，和我一起，去到地上！」
    沒有回應，因爲自始至終這個狹長的空間裏只有一個人。如果他不回應自己的話，就一定沒有誰會回應他了。
    青色的光像是風中的火，頻繁而隨機地稍稍淡下又變得更強，也許有人會不禁懷疑電路是不是出了故障…………
    …………又像是裝可愛的女兒眨着俏皮的眼睛。
    # 這是隨便編的www，本來想隨便寫幾句程序的哲理體現一下潘大爺的厲害，結果就變成了小說23333

不需要任何其他標記或代碼，一小段劇本就完成了。  
準備好立繪和背景後，運行Librian主程序並選擇剛纔的工程啓動——演出是這樣的效果。  
![圖1](文檔/樣例_潘大爺.jpg)

## 擴展功能

你可以輕鬆客製化你的遊戲，包括遊標，界面，標題畫面等。

不只是adv，你甚至可以嵌入線上交互等功能！

## 中文文檔

如果你想瞭解詳細的使用方法，可以直接閱讀Librian的中文文檔——<https://rimochan.github.io/Librian_doc>。

## 快速上手

方便起見的話，Windows用戶可以直接下載打包的[release版本](https://github.com/RimoChan/Librian/releases)使用。

如果你持「不讀說明書主義」，也可以: 

1.  安裝python3.6
2.  pip install wxpython cefpython3 pillow psd-tools pyyaml chardet
3.  python3 librian_panel.py

此外，你也可以根據[中文文檔](https://rimochan.github.io/Librian_doc)的指示來安裝。

## 援交～

試着建了QQ討論組: 618775838。

如果你需要一些使用幫助，或者有什麼不滿，或者不常用GitHub的話，可以來這裏討論。  
總之，一起玩就行啦。

## 贊助

如果你覺得Librian對你的工作或學習有幫助，歡迎給作者介紹一些可愛的女朋友。

最好是蘿莉，要那種會坐在腿上蹭蹭，喊「歐尼醬」的。
