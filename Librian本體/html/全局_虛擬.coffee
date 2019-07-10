$ ->
    if typeof(虛擬核心已加載) == "undefined"
        alert '無法加載虛擬核心。'

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
    
    $('title').html 作品名
    山彥.初始化()

window.山彥 =
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
    初始化: ->
        演出.配置({
            解析度
            邊界
            主題css
            自定css
            圖片文件夾
            音樂文件夾
            視頻文件夾
        })
        演出.準備工作()