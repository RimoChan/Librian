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

        $('#總畫面').css 'width', this.解析度[0]
        $('#總畫面').css 'height', this.解析度[1]

        if this.邊界
            $ 'div'
                .css 'border','1px solid #22f'

        this.換圖('覆蓋','url(static/None.png)', 0)
        this.換圖('bg','url(static/None.png)', 0)
        this.換圖('cg','url(static/None.png)', 0)
        this.縮放調整()
        this.更新()

    縮放調整: ->
        a = document.body.clientWidth / 演出.解析度[0]
        b = document.body.clientHeight / 演出.解析度[1]
        t = Math.min(a, b)
        $('#總畫面 , #墊底').css({
            "transform-origin": "0% 0%"
            "transform": "scale("+t+")"
        } )
        setTimeout(演出.縮放調整, 200)


    配置: (d) ->
        for i, j of d
            this[i] = j

    步進更新: ->
        山彥.步進更新()
    更新: ->
        山彥.更新()

    信息預處理: (data) ->
        if ! data.背景
            data.背景 = 'url(static/None.png)'
        else
            data.背景 = "url(#{this.圖片文件夾}/#{data.背景})"
        if ! data.cg
            data.cg = 'url(static/None.png)'
        else
            data.背景 = "url(#{this.圖片文件夾}/#{data.cg})"

        if data.背景音樂[0]!='None'
            data.背景音樂[0] = this.音樂文件夾 + '/' + data.背景音樂[0]

        if data.名字!=''
            data.話語 = "「#{data.話語}」"
            $('#名字框').fadeIn(200)
        else
            data.話語 = '　　' + data.話語
            $('#名字框').fadeOut(200)

    改變演出狀態: (data) ->
        this.信息預處理 data
        console.log data
        {特效表, 立繪, 名字, 話語, 額外信息, 語者, 背景, 背景音樂, cg, 選項, js, 視頻} = data
        this.特效處理 特效表
        if 選項.length > 0
            this.處理選項 選項
            return
        if 額外信息
            if 額外信息[0] == 'cut'
                名字 = ''
                話語 = ''
                背景音樂 = ['None', 0]
                this.插入圖(額外信息[1])
            if 額外信息[0] == 'load'
                this.load特效()
        eval(js)
        this.放視頻(視頻)
        this.換cg(cg)
        this.換背景(背景)
        this.換立繪(立繪)
        this.換背景音樂(背景音樂)
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
    處理選項: (選項) ->
        console.log '處理選項',選項
        tot = ''
        for i,p in 選項
            tot += "<button onclick='演出.點選項(#{p});'>#{i}</botton>\n"
        $('#選項').html(tot)
        console.log '選項show'
        $('#選項').show(250)
        this.選擇之刻 = true
    點選項: (x) ->
        console.log '點選項hide'
        $('#選項').hide(250)
        山彥.選(x)
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
        if ! 視頻
            return
        控制.左鍵屏蔽 = true
        v = $('video')
        v.css('display','block')
        v.attr('src',this.視頻文件夾+'/' + 視頻)
        v[0].addEventListener 'ended', ->
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

    現在背景: 'None',
    換背景: (背景) ->
        if 背景 == this.現在背景
            return
        現在背景 = 背景
        if 背景 == 'None'
            背景 = 'url(static/None.png)'
        this.換圖('bg', 背景, 1.4)

    換人名: (語者, 名字) ->
        $('#名字').html(名字)
        $('#對話歷史').append(名字+'<br/>')
        $('#對話框').attr('class','人物--' + 語者)
        # alert $('#對話框').attr('class')

    淡入過期時間: 0,
    換對話: (text, 名字) ->
        淡入字 = 演出.文字淡入(text)
        $('#話語').html(淡入字.內容)
        演出.淡入過期時間 = Date.now() + 淡入字.總時間 * 1000
        $('#對話歷史').append(text+'<br/><br/>')
    早泄: ->
        $('#話語 *').css('animation','None')
        $('#話語 *').css('opacity','1')

    當前曲名: 'None',
    換背景音樂: (背景音樂) ->
        曲名 = 背景音樂[0]
        音量 = 背景音樂[1]
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

    文字淡入: (s, 動畫名 = '_淡入') ->
        時間間隔 = 設置.內容.文字速度/800
        group = s.replace(/((<.*?>)|(.))/g, "$2$3\0").split('\0')
        動畫時間 = 時間間隔 * 8
        時間 = 0
        內容 = (for i in group
            if i[0] == '<'
                i
            else
                時間 += 時間間隔
                "<span style='animation:#{動畫名} #{動畫時間}s;animation-fill-mode:forwards;animation-delay:#{時間}s;opacity:0;'>#{i}</span>"
        ).join('')
        {內容, 總時間: 時間 + 動畫時間}
