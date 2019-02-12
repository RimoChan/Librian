$ ->
    if typeof(虛擬核心已加載) == "undefined"
        alert '無法加載虛擬核心。'

    $('title').html 作品名
    演出.主題css = 主題css
    演出.自定css = 自定css
    演出.圖片文件夾 = 圖片文件夾
    演出.音樂文件夾 = 音樂文件夾
    演出.準備工作()
    縮放調整=->
        a = document.body.clientWidth / 解析度[0]
        b = document.body.clientHeight / 解析度[1]
        t = Math.min(a, b)
        $('#總畫面 , #墊底').css({
            "transform-origin": "0% 0%"
            "transform": "scale("+t+")"
        } )
        setTimeout(縮放調整, 200)
    縮放調整()

虛擬中樞 =
    n: 0
    更新: ->
        演出.改變演出狀態(演出步[this.n])
    步進: ->
        this.n += 1
    步進更新: ->
        this.步進()
        this.更新()
    設置: ->
        0

window.send = (a, b) ->
    虛擬中樞[a](b)
    console.log ['send', a, b]



