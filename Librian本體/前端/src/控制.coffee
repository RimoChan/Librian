import 演出 from './演出.coffee'

export default 控制 =
    右鍵功能: ->
        window.event.returnValue = false
        $('#總畫面').attr('歷史', 'off')
        if $('#總畫面').attr('對話框') == 'off'
            $('#總畫面').attr('對話框', 'on')
        else
            $('#總畫面').attr('對話框', 'off')

    左鍵屏蔽: false
    左鍵功能: ->
        if this.左鍵屏蔽 or 演出.選擇之刻
            return

        if $('#總畫面').attr('歷史') == 'on'
            $('#總畫面').attr('歷史', 'off')

        if $('#總畫面').attr('對話框') == 'off'
            $('#總畫面').attr('對話框', 'on')
        else
            if Date.now() < 演出.淡入過期時間
                演出.淡入過期時間 = 0
                演出.早泄()
            else
                演出.步進更新()

    顯示履歷: ->
        $('#總畫面').attr('歷史', 'on')
        $('#總畫面').attr('對話框', 'off')
        $('#對話歷史').scrollTop($('#對話歷史')[0].scrollHeight)

    正在快進: false,

    開始快進: ->
        if this.正在快進 == false
            this.正在快進 = true
            this.快進輪迴()
    結束快進: ->
        this.正在快進 = false

    切換快進: ->
        if this.正在快進 == false
            this.正在快進 = true
            this.快進輪迴()
        else
            this.正在快進 = false

    快進輪迴: ->
        if 控制.正在快進 == false
            return
        else
            控制.左鍵功能()
            setTimeout(控制.快進輪迴, 50)

    進入設置: ->
        $('#總畫面').attr('配置面板', 'on')

    退出設置: ->
        $('#總畫面').attr('配置面板', 'off')

    控制初始化: ->
        window.document.onkeydown = (evt) ->
            k = evt.keyCode
            # [ctrl] skip
            if k == 17
                console.log 'ctrl按下'
                控制.開始快進()
            # [空格 回車 z] 左鍵
            if k == 32 || k == 13 || k == 90
                控制.左鍵功能()
            # [esc] 右鍵
            if k == 27
                控制.右鍵功能()
            # [Page_up] 歷史
            if k == 33
                控制.顯示履歷()
        window.document.onkeyup = (evt) ->
            # [ctrl] skip
            if evt.keyCode == 17
                console.log 'ctrl放開'
                控制.結束快進()
                
        # 滚轮功能
        $('#主畫面').mousewheel (event, delta)->
            if delta > 0
                控制.顯示履歷()
            if delta < 0
                控制.左鍵功能()
        
        $("#主畫面").mousedown (e)->
            if e.which == 3
                控制.右鍵功能()
            else if e.which == 1 
                控制.左鍵功能()
        
        $('#存檔').click ->
            山彥.存檔()
        $('#讀檔').click ->
            山彥.讀檔()
        $('#快速存檔').click ->
            山彥.快速存檔()
        $('#快速讀檔').click ->
            山彥.快速讀檔()
        $('#自動模式').click ->
            alert("沒做這個功能")
        $('#切換快進').click ->
            控制.切換快進()
        $('#進入設置').click ->
            控制.進入設置()
        $('#回標題').click ->
            山彥.回標題()
            
        $('#退出設置').click ->
            控制.退出設置()

                