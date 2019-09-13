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
            山彥.建立工程()
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
            山彥.生成html()
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