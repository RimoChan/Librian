import $ from 'jquery'
import opencc from 'node-opencc'

import 控制 from './控制.coffee'
import psd處理 from './psd處理.coffee'


export default 演出 = 
    準備工作: ->
        $ '<link>'
            .attr
                rel: 'stylesheet'
                type: 'text/css'
                href: v.主題css
            .appendTo("head")
        for i in v.自定css
            $ '<link>'
                .attr
                    rel: 'stylesheet'
                    type: 'text/css'
                    href: i
                .appendTo('head')

        $('#總畫面').css 'width', v.解析度[0]
        $('#總畫面').css 'height', v.解析度[1]

        if v.邊界
            $ 'div'
                .css 'border','1px solid #22f'

        this.縮放調整()

    縮放調整: ->
        a = document.body.clientWidth / v.解析度[0]
        b = document.body.clientHeight / v.解析度[1]
        t = Math.min(a, b)
        $('#總畫面').css(
            "transform-origin": "0% 0%"
            "transform": "scale("+t+")"
        )
        setTimeout(演出.縮放調整, 200)

    更新: (瞬間化=false)->
        山彥.狀態回調 false, (狀態, 步進=false)->
            演出.改變演出狀態(狀態, 瞬間化)
            
    步進更新: (瞬間化=false)->
        山彥.狀態回調 true, (狀態)->
            演出.改變演出狀態(狀態, 瞬間化)
            
    翻譯: (s)->
        if not v.翻譯
            return s
        return opencc[v.翻譯](s)
            
    信息預處理: (data) ->
        if data.背景
            data.背景[0] = "url('#{v.圖片文件夾}/#{data.背景[0]}')".replace(/(\\)/g, '/')
        if data.cg
            data.cg[0] = "url('#{v.圖片文件夾}/#{data.cg[0]}')".replace(/\\/g, '/')
        if data.背景音樂
            data.背景音樂[0] = v.音樂文件夾 + '/' + data.背景音樂[0]
        if data.效果音
            data.效果音[0] = v.音樂文件夾 + '/' + data.效果音[0]
        if data.插入圖
            data.插入圖 = "url('#{v.圖片文件夾}/#{data.插入圖}')".replace(/\\/g, '/')
    
    當前狀態: {}
    改變演出狀態: (data, 瞬間化=false) ->
        console.log data
        this.信息預處理 data
        this.當前狀態 = data
        {特效表, 插入圖, 立繪, 名字, 話語, 額外信息, 語者, 背景, 背景音樂, 效果音, cg, 選項, js, html, 視頻} = data
        this.特效處理 特效表
        if 選項.length > 0
            this.處理選項 選項
            return
            
        if 插入圖
            this.換背景音樂(null)
            this.換圖('覆蓋', 插入圖, 0)
            $('#覆蓋').attr('顯現', 'true') 
            return
        else
            if $('#覆蓋').attr('顯現') == 'true'
                瞬間化 = true
            $('#覆蓋').attr('顯現', 'false') 
            
        if 額外信息
            if 額外信息[0] == 'load'
                this.load特效()
        try
            eval(js)
        catch e
            console.log e
        
        $('#html疊加').html(html)
        this.放視頻(視頻)
        this.換cg(cg)
        this.換背景(背景, 瞬間化)
        this.換立繪(立繪, 瞬間化)
        this.換背景音樂(背景音樂)
        this.放效果音(效果音)
        this.換人名(語者, 名字)
        this.換對話(話語, 名字, 瞬間化)

    特效處理: (特效表) ->
        可特效块 = [
            '總畫面','adv畫面','主畫面','覆蓋','選項','cg','bg','立繪','對話歷史',
            '對話框','名字框','名字','名字框背景','話語框','話語','話語框背景',
            '對話框背景'
        ]
        for i in 可特效块
            if $('#' + i).attr('特效')
                $('#' + i).attr('特效', '')
        for i of 特效表
            $('#' + i).attr('特效', 特效表[i])

    選擇之刻: false,
    處理選項: (選項) ->
        $('#選項').html('')
        for i, p in 選項
            t = $("<a 選項號='#{p}'>#{i}</a>")
            $('#選項').append(t)
            t.click () -> 
                演出.點選項(parseInt($(this).attr('選項號')))
        $('#選項').fadeIn(200)
        this.選擇之刻 = true
    點選項: (x) ->
        $('#選項').fadeOut(50)
        山彥.選(x)
        this.選擇之刻 = false

    放視頻: (視頻) ->
        if ! 視頻
            return
        [視頻文件, 可以跳過] = 視頻
        video = $('#視頻')
        video.css('display', 'block')
        video.attr('src', v.視頻文件夾+'/' + 視頻文件)
        video.click if 可以跳過
            ->
                video.css('animation', '_黑出 0.5s')
                video.css('animation-fill-mode', 'forwards')
                setTimeout ->
                    video.css('animation', '')
                    video.attr('src', '')
                    video[0].style.display = 'none'
                , 600
        else
            -> null

        video[0].addEventListener 'ended', ->
            video[0].style.display = 'none'
        , false
        video[0].play()

    load特效: ->
        控制.左鍵屏蔽 = true
        $('#adv畫面').fadeOut(0)
        $('#adv畫面').fadeIn(400)
        setTimeout ->
            控制.左鍵屏蔽 = false
        , 300
    提示: (x) ->
        $('#提示').html(x)
        $('#提示').fadeIn(300)
        $('#提示').hide(1000)

    現在cg: null,
    換cg: (cg) ->
        if cg
            [cg圖片, 淡入時間, 漸變方法] = cg
        else
            [cg圖片, 淡入時間, 漸變方法] = ['', 0, '']
        if cg圖片 == this.現在cg
            return
        this.現在cg = cg圖片
        this.換圖('cg', cg圖片, 淡入時間, 漸變方法)

    當前人物組: []
    換立繪: (立繪組, 瞬=false) ->
        名字組 = (立繪.名字 for 立繪 in 立繪組)
        
        # 垃圾回收
        for 名字 in this.當前人物組
            if 名字組.indexOf(名字) == - 1
                $("#立繪--#{名字}").remove()
                console.log "去除 #{名字}"
            else
                $("#立繪--#{名字}").attr('特效', '')

        # 新建        
        for 名字 in 名字組
            if this.當前人物組.indexOf(名字) == - 1
                $('#立繪').append($("<div id='立繪--#{名字}'><div id='立繪--#{名字}--圖像'></div></div>"))
                console.log "加入 #{名字}"
                $("#立繪--#{名字}").attr('特效','淡入')
                
        # 設定位置          
        for 立繪 in 立繪組
            t = $("#立繪--#{立繪.名字}")
            if 瞬
                t.css('transition', '')
            else
                移動時間 = 0.5
                t.css('transition', "top #{移動時間}s, left #{移動時間}s, transform #{移動時間}s")
            t.css('left', "#{立繪.位置[0]}px")
            t.css('top', "#{立繪.位置[1]}px")
            t.css('transform', "scale(#{立繪.位置[2]})")
            $("#立繪--#{立繪.名字}--圖像").attr('特效', 立繪.特效.join(' '))
            
        # 貼圖
        for 立繪 in 立繪組
            if 立繪.使用png
                png名 = "#{v.psd立繪路徑}/#{立繪.名字}.png"
                psd處理.渲染png到div(png名, "立繪--#{立繪.名字}--圖像")
            else
                psd名 = "#{v.psd立繪路徑}/#{立繪.名字}.psd"
                psd處理.渲染圖層組到div(psd名, 立繪.圖層, "立繪--#{立繪.名字}--圖像")

        this.當前人物組 = 名字組

    現在背景: [null, "0% 0%"],
    換背景: (背景, 瞬) ->
        if 背景
            [背景圖片, 淡入時間, 位置, 漸變方法] = 背景
        else
            [背景圖片, 淡入時間, 位置, 漸變方法] = ['', 0, '']
        if 瞬
            淡入時間 = 0
        if 背景圖片 != this.現在背景[0]
            $('#bg').css('background-position', 位置)
            this.換圖('bg', 背景圖片, 淡入時間, 漸變方法)
        else if 位置 != this.現在背景[1]
            $('#bg').css('background-position', 位置)
        this.現在背景 = [背景圖片, 位置]

    換人名: (語者, 名字) ->
        名字 = this.翻譯(名字)
        if 名字
            $('#名字').html(名字)
            $('#名字框').css('opacity', 1)
        else
            $('#名字框').css('opacity', 0)
        $('#對話歷史').append(名字+'<br/>')
        $('#對話框').attr('名字', 語者)

    淡入過期時間: 0,
    換對話: (話語, 名字, 瞬間化) ->
        話語 = this.翻譯(話語)
        名字 = this.翻譯(名字)
        $('#對話歷史').append(話語+'<br/><br/>')
        
        if 名字 != ''
            $('#對話框').attr('對話類型','對話')
        else
            $('#對話框').attr('對話類型','旁白')
        
        if $("#話語").css("--幹你娘老子就是要每行都縮進")
            縮進 = '　'.repeat(parseInt($("#話語").css("--幹你娘老子就是要每行都縮進")))
            話語 = 話語.replace(/(^|\n)/g, "$1#{縮進}")
        
        if 瞬間化
            $('#話語').html(話語 + '<span></span>') 
        else
            淡入字 = 演出.文字淡入(話語)
            $('#話語').html(淡入字.內容)
            演出.淡入過期時間 = Date.now() + 淡入字.文字時間 * 1000
    早泄: ->
        $('#話語 *').css('animation','None')
        $('#話語 *').css('opacity','1')

    當前曲名: null,
    換背景音樂: (背景音樂) ->
        if 背景音樂
            [曲名, 音量] = 背景音樂
        else
            [曲名, 音量] = [null, 0]
            
        if this.當前曲名 == 曲名
            return
        this.當前曲名 = 曲名
        
        for i in $('#總畫面 > audio.背景音樂')
            if i.volume==0
                i.remove()
        $('#總畫面 > audio.背景音樂').animate({volume: 0}, 500)
        
        音樂 = $("<audio src='#{曲名}' class='背景音樂' autoplay loop></audio>")
        音樂.volume = 音量
        $('#總畫面').append(音樂)
        
    放效果音: (效果音) ->
        if ! 效果音
            return
        [曲名, 音量] = 效果音
        音樂 = $("<audio src='#{曲名}' class='效果音' autoplay></audio>")
        音樂.volume = 音量
        音樂[0].addEventListener('ended', ->
            音樂.remove()
        , false)
        $('#總畫面').append(音樂)
        
    換圖: (目標, 新圖, 漸變時間, 漸變方法 = '_淡出') ->
        目標 = $('#'+目標)
        原背景 = 目標.css('background-image')
        目標.css('background-image', 新圖)

        目標.html('<div class="舊淡出"></div>')
        舊淡出 = 目標.children()

        if 漸變時間 > 0
            舊淡出.css('background-image', 原背景)
            舊淡出.css('animation', "#{漸變方法} #{漸變時間}s")
            舊淡出.css('animation-fill-mode', 'forwards')
            舊淡出.css('animation-play-state', 'running')

    文字淡入: (s, 動畫名 = '_淡入') ->
        時間間隔 = v.用戶設置.文字速度.值 / 800
        group = s.replace(/(\s*((<.*?>)|(.)))/g, "$1\0").split('\0')
        動畫時間 = 時間間隔 * 8
        時間 = 0
        內容 = (for i in group
            if i[0] == '<'
                i
            else
                時間 += 時間間隔
                "<span style='animation:#{動畫名} #{動畫時間}s;animation-fill-mode:forwards;animation-delay:#{時間}s;opacity:0;'>#{i}</span>"
        ).join('')
        {內容, 文字時間: 時間, 總時間: 時間 + 動畫時間}
