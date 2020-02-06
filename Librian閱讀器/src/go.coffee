import Vue from 'vue/dist/vue.esm.js'
import $ from 'jquery'

import transverter from './transverter.js'

import './網頁樣式.sass'
import './劇本樣式.sass'


$ ->
    window.v = new Vue
        el: '#all'
        data:
            鎖: false
            配置: null
            文件列表: []
            文件號: null
            當前內容: null
        methods:
            簡化字: (s) ->
                if s and this.配置.簡化字
                    return transverter()({str: s} )
                else
                    return s

    window.load = (文件號) ->
        v.文件號 = null
        v.當前內容 = null
        $('title').html(v.文件列表[文件號]['名字'])
        $.ajax
            dataType: "json",
            url: v.文件列表[文件號]['文件'],
            success: (j) ->
                v.文件號 = 文件號
                v.當前內容 = j

    $.ajax
        dataType: "json",
        url: '配置.json',
        success: (配置) ->
            console.log 配置
            v.配置 = 配置
            for i in 配置.自定css
                $ '<link>'
                    .attr
                        rel: 'stylesheet'
                        type: 'text/css'
                        href: i
                    .appendTo('head')
            v.文件列表 = 配置.文件列表
            load(0)
