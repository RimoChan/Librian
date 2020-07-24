import Vue from 'vue/dist/vue.esm.js'
import $ from 'jquery'

import 演出 from './演出.coffee'


export default 存檔讀檔 = 
    存檔準備: ->
        山彥.取檔 (檔表) ->
            v.存檔讀檔.檔表 = 檔表
            v.存檔讀檔.啓動功能 = '存檔'
            $('#總畫面').attr('存檔讀檔面板', 'on')
    讀檔準備: ->
        山彥.取檔 (檔表) ->
            v.存檔讀檔.檔表 = 檔表
            v.存檔讀檔.啓動功能 = '讀檔'
            $('#總畫面').attr('存檔讀檔面板', 'on')
    存檔: (名字, 描述)->
        this.截圖轉換 160, 90, (截圖)->
            山彥.存檔(名字, 描述, 截圖)
            山彥.取檔 (檔表) ->
                v.存檔讀檔.檔表 = 檔表
    讀檔: (名字)->
        山彥.讀檔(名字)
        $('#總畫面').attr('存檔讀檔面板', 'off')
    快速存檔: ->
        山彥.快速存檔()
    快速讀檔: ->
        山彥.快速讀檔()
    截圖轉換: (x, y, 回調)->
        bg = 演出.當前狀態.背景[0].slice(5,-2)
        t = new Image()
        t.src = bg
        t.setAttribute("crossOrigin", 'Anonymous')
        t.onload = ->
            canvas = document.createElement("canvas")
            canvas.width = x
            canvas.height = y
            context = canvas.getContext("2d")
            context.drawImage(t, 0, 0, 160, 90)
            base64 = canvas.toDataURL("image/webp")
            回調(base64)