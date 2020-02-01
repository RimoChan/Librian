import Vue from 'vue/dist/vue.esm.js'
import $ from 'jquery'

import 演出 from './演出.coffee'
import 控制 from './控制.coffee'
import 存檔讀檔 from './存檔讀檔.coffee'

import './_統合.sass'


window._py演出 = 演出

window.onload = ->
    if window.山彥
        window.本地 = 
        console.log '在本地演出'
        本地運行()
    else
        console.log '在瀏覽器上演出'
        在線運行()
    控制.控制初始化()

本地運行 = ->
    window.v = new Vue
        el: '#總畫面'
        data:
            本地運行: true
            圖片文件夾: ''
            音樂文件夾: ''
            視頻文件夾: ''
            臨時立繪文件夾: ''
            自定css: ''
            主題css: ''
            解析度: ''
            邊界: ''
            翻譯: false
            存檔讀檔:
                啓動功能: '？？？'
                檔表: []
            用戶設置: 
                文字速度: 
                    類型: 'number'
                    值: 35
                    範圍: [0, 100]
                    提示: ['須臾', '永恆']
                對話框背景透明度:
                    類型: 'number'
                    值: 0.8
                    範圍: [0, 1]
                    提示: ['通透', '固實']
                總體音量:
                    類型: 'number'
                    值: 1
                    範圍: [0, 1]
                    提示: ['小聲', '大聲(沒用)']
                自動收起控制面板: 
                    類型: 'boolean'
                    值: false
                
        watch:
            $data:
                handler: (val, oldVal) ->
                    山彥.vue更新(val)
                deep: true
    山彥.vue連接初始化((x)-> 
        for a,b of x
            v[a]=b
    )
    山彥.初始化()


從虛擬核心提取資源 = (心)->
    集合 = {}
    步 = JSON.parse(JSON.stringify(心.演出步))
    for data in 步
        if data.背景
            集合["#{v.圖片文件夾}/#{data.背景[0]}"] = true
        if data.cg
            集合["#{v.圖片文件夾}/#{data.cg[0]}"] = true
        if data.插入圖
            集合["#{v.圖片文件夾}/#{data.插入圖}"] = true
        for 人 in data.立繪
            for 圖層 in 人.圖層
                集合["#{v.臨時立繪文件夾}/#{圖層.文件}"] = true
    return (i for i of 集合)

window.加載完成的初始化 = ->
    $('#加載畫面').fadeOut()
    山彥.初始化()

在線運行 = ->
    if typeof(虛擬核心) == "undefined"
        alert '無法加載虛擬核心。'
        return
        
    ua = window.navigator.userAgent
    isChrome = ua.indexOf("Chrome") && window.chrome
    if not isChrome
        alert '只有chrome能用。'
        return
        
    $('#加載畫面').css('display', 'flex')
        
    window.山彥 =
        n: 0
        步進: ->
            this.n += 1
        更新: ->
            演出.改變演出狀態(虛擬核心.演出步[this.n])
        狀態回調: (步進, callback)->
            if 步進
                this.步進()
            callback(虛擬核心.演出步[this.n])
        初始化: ->
            演出.準備工作()
        切換全屏: ->
            doc = window.document
            docEl = doc.documentElement

            requestFullScreen = docEl.requestFullscreen || docEl.mozRequestFullScreen || docEl.webkitRequestFullScreen || docEl.msRequestFullscreen
            cancelFullScreen = doc.exitFullscreen || doc.mozCancelFullScreen || doc.webkitExitFullscreen || doc.msExitFullscreen

            if(!doc.fullscreenElement && !doc.mozFullScreenElement && !doc.webkitFullscreenElement && !doc.msFullscreenElement) 
                requestFullScreen.call(docEl)
            else 
                cancelFullScreen.call(doc)
    
    window.v = new Vue
        el: '#總畫面'
        data:
            本地運行: false
            圖片文件夾: 虛擬核心.圖片文件夾
            音樂文件夾: 虛擬核心.音樂文件夾
            視頻文件夾: 虛擬核心.視頻文件夾
            臨時立繪文件夾: 虛擬核心.臨時立繪文件夾
            自定css: 虛擬核心.自定css
            主題css: 虛擬核心.主題css
            解析度: 虛擬核心.解析度
            邊界: 虛擬核心.邊界
            翻譯: false
            用戶設置: 
                文字速度: 
                    類型: 'number'
                    值: 35
                    範圍: [0, 100]
                    提示: ['須臾', '永恆']
                對話框背景透明度:
                    類型: 'number'
                    值: 0.8
                    範圍: [0, 1]
                    提示: ['通透', '固實']
                總體音量:
                    類型: 'number'
                    值: 1
                    範圍: [0, 1]
                    提示: ['小聲', '大聲(沒用)']
                自動收起控制面板: 
                    類型: 'boolean'
                    值: false
    
    資源組 = 從虛擬核心提取資源(虛擬核心)
    window.v加載 = new Vue
        el: '#加載畫面'
        data:
            最大值: 資源組.length
            計數: 0
    for 資源 in 資源組
        $.get(資源, ->
            v加載.計數+=1
        )
    $('title').html 虛擬核心.作品名
