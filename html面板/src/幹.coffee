import Vue from 'vue/dist/vue.esm.js'
import Swal from 'sweetalert2'
import $ from 'jquery'

import './樣式.sass'

window.Swal = Swal

$ ->
    window.v = new Vue
        el: '#all'
        data:
            標題: ''
            主解析度: ''
            工程路徑: ''
            圖標路徑: ''
            存檔資料: []
        watch:
            $data:
                handler: (val, oldVal) ->
                    山彥.vue更新(val)
                deep: true
    山彥.vue連接初始化((x) ->
        for a, b of x
            v[a] = b
    )
    
    響應表 = 
        開啓工程: ->
            山彥.開啓工程()
        建立工程: ->
            Swal.fire
                title: '工程名'
                input: 'text'
                showCancelButton: true,
                confirmButtonText: '确定'
                cancelButtonText: '取消'
            .then (result) ->
                if result.value
                    山彥.建立工程(result.value)
        清除記錄: ->
            v.存檔資料 = []
        運行: ->
            山彥.運行()
        運行同時編寫: ->
            山彥.運行同時編寫()
        打開文件夾: ->
            山彥.打開文件夾()
        生成exe: ->
            山彥.生成exe()
        生成html: ->
            Swal.fire
                title: '目标文件夹路径'
                input: 'text'
                showCancelButton: true,
                confirmButtonText: '确定'
                cancelButtonText: '取消'
            .then (result) ->
                if result.value
                    山彥.生成html(result.value)
        讀文檔: ->
            Swal.fire
                title: '在外部瀏覽器打開Librian文檔？'
                showCancelButton: true,
                confirmButtonText: '确定'
                cancelButtonText: '取消'
            .then (result) ->
                if result.value
                    山彥.瀏覽器打開("https://gate.librian.it/?a=Librian&b=https://doc.librian.it")
        自我更新: ->
            Swal.fire
                icon: 'warning'
                title: '真的要更新嗎'
                text: 'Librian更新是激進的，\n可能會使你的電腦爆炸！'
                showCancelButton: true,
                confirmButtonText: '确定'
                cancelButtonText: '取消'
            .then (result) ->
                if result.value
                    山彥.自我更新()
        返回: ->
            window.返回()
    
    $('body').on 'click','a', (event)->
        id = $(this).attr('id')
        if id
            響應表[id]()
        else
            console.log '沒有可響應的id'

    window.進入工程 = ->
        $('.頁').hide()
        $('#工程編輯').show()
    window.返回 = ->
        $('.頁').hide()
        $('#入口').show()

    window.返回()