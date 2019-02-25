window.演出 =
    準備工作: ->
        $ '<link>'
            .attr
                rel: 'stylesheet'
                type: 'text/css'
                href: this.自定css
            .appendTo('head')
        $ '<link>'
            .attr
                rel: 'stylesheet'
                type: 'text/css'
                href: this.主題css
            .appendTo("head")

        $('#總畫面').css 'width', 解析度[0]
        $('#總畫面').css 'height', 解析度[1]

        if 邊界
            $ 'div'
                .css 'border','1px solid #22f'

        this.換圖('覆蓋','url(static/None.png)', 0)
        this.換圖('bg','url(static/None.png)', 0)
        this.換圖('cg','url(static/None.png)', 0)
        this.更新()

    步進更新: ->
        send('步進更新')
    更新: ->
        send('更新')

    信息預處理: (data) ->
        if ! data.bg
            data.bg = 'url(static/None.png)'
        else
            data.bg = "url(#{this.圖片文件夾}/#{data.bg})"
        if ! data.cg
            data.cg = 'url(static/None.png)'
        else
            data.bg = "url(#{this.圖片文件夾}/#{data.cg})"

        if data.bgm[0]!='None'
            data.bgm[0] = this.音樂文件夾 + '/' + data.bgm[0]

        if data.名字!=''
            data.話語 = "「#{data.話語}」"
            $('#名字框').fadeIn(200)
        else
            data.話語 = '　　' + data.話語
            $('#名字框').fadeOut(200)

    改變演出狀態: (data) ->
        this.信息預處理 data
        {特效表, 立繪, 名字, 話語, 額外信息, 語者, bg, bgm, cg, choice} = data
        this.特效處理 特效表
        if choice.length > 0
            this.處理選項 choice
            return
        if 額外信息
            if 額外信息[0] == 'cut'
                名字 = ''
                話語 = ''
                bgm = ['None', 0]
                this.插入圖(額外信息[1])
            if 額外信息[0] == 'video'
                this.放視頻(額外信息[1])
            if 額外信息[0] == 'load'
                this.load特效()
        this.換cg(cg)
        this.換bg(bg)
        this.換立繪(立繪)
        this.換bgm(bgm)
        this.換人名(語者, 名字)
        this.換對話(話語, 名字)

    特效處理: (特效表) ->
        可特效块 = [
            '總畫面','adv畫面','覆蓋','選項','cg','bg','立繪','對話歷史',
            '對話框','名字框','名字','名字框背景','話語框','話語','話語框背景',
            '對話框背景'
        ]
        for i in 可特效块
            if $('#'+i).attr('class')
                $('#'+i).attr('class','')
        for i in 特效表
            $('#' + i).addClass(特效表[i])

    選擇之刻: false,
    處理選項: (choice) ->
        tot = ''
        for i in choice
            tot += "<button onclick='this.點選項(#{i});'>#{choice[i]}</botton>\n"
        $('#選項').html(tot)
        $('#選項').show(250)
        this.選擇之刻 = true
    點選項: (x) ->
        $('#選項').hide(250)
        send('選',x+'')
        this.選擇之刻 = false

    插入圖: (圖) ->
        控制.左鍵屏蔽 = true
        $('#覆蓋').css('display','block')
        $('#總畫面').fadeOut(1400)
        setTimeout ->
            演出.換圖('覆蓋','url('+演出.圖片文件夾+'/'+圖+')', 0)
        , 1500
        setTimeout ->
            演出.步進更新()
        , 1500
        setTimeout ->
            $('#總畫面').fadeIn(1100)
        , 1500
        setTimeout ->
            演出.換圖('覆蓋','url(static/None.png)', 1)
        , 4500
        setTimeout ->
            $('#覆蓋').css('animation','')
        , 5550
        setTimeout ->
            $('#覆蓋').css('display','none')
        , 5600
        setTimeout ->
            控制.左鍵屏蔽 = false
        , 5600
    放視頻: (視頻) ->
        控制.左鍵屏蔽 = true
        v = $('video')
        v.css('display','block')
        v.attr('src',this.視頻文件夾+'/' + 視頻)
        v[0].addEventListener 'ended', ->
            this.步進更新()
            setTimeout ->
                v[0].style.display = 'none'
                控制.左鍵屏蔽 = false
            , 500
        , false
        v[0].play()

    load特效: ->
        控制.左鍵屏蔽 = true
        $('#總畫面').fadeOut(0)
        $('#總畫面').fadeIn(1200)
        setTimeout ->
            控制.左鍵屏蔽 = false
        , 1000
    提示: (x) ->
        $('#提示').html(x)
        $('#提示').fadeIn(300)
        $('#提示').hide(1000)

    現在cg: 'None',
    換cg: (cg) ->
        if cg == this.現在cg
            return
        this.現在cg = cg
        this.換圖('cg', cg, 1)

    換立繪: (text) ->
        $('#立繪').html(text)

    現在bg: 'None',
    換bg: (bg) ->
        if bg == this.現在bg
            return
        現在bg = bg
        if bg == 'None'
            bg = 'url(static/None.png)'
        this.換圖('bg', bg, 1.4)

    換人名: (語者, 名字) ->
        $('#名字').html(名字)
        $('#對話歷史').append(名字+'<br/>')
        $('#對話框').attr('class','人物--'+語者)
        # alert $('#對話框').attr('class')
        
    換對話: (text, 名字) ->
        if 名字
            $('#話語').逐字打印(text, true)
        else
            $('#話語').逐字打印(text)
        $('#對話歷史').append(text+'<br/><br/>')

    當前曲名: 'None',
    換bgm: (bgm) ->
        曲名 = bgm[0]
        音量 = bgm[1]
        au = $('#bgm')
        if this.當前曲名 == 曲名
            return
        this.當前曲名 = 曲名
        if this.當前曲名 == 'None'
            au.stop()
            au.animate({volume: 0} , 2000)
            setTimeout ->
                au.attr('src', 演出.當前曲名)
            , 2000
        else
            au.stop()
            au.attr('src', this.當前曲名)
            au.animate({volume: 0} , 0)
            au.animate({volume: 音量} , 2000)

    換圖: (dst, img_b, time) ->
        frame = 'A' + Math.ceil(Math.random() * 999999).toString()
        dst = '#' + dst
        img_a = $(dst).attr('my_img')

        if time > 0
            $(dst).css('animation','')
            $('#style').append('@keyframes '+frame+'{ 0%{background-image:'+img_a+';}100%{background-image:'+img_b+';} }\n')
            $(dst).css('animation',frame+' '+time.toString()+'s')
        $(dst).css('background-image', img_b)
        $(dst).attr('my_img', img_b)
