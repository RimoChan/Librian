$ ->
    window.v = new Vue
        el: '#工程信息'
        data:
            標題: ''
            主解析度: ''
            工程路徑: '' 
            
    $("#開啓工程").click ->
        send("開啓工程")
    $("#建立工程").click ->
        send("建立工程")
        
    $("#運行").click ->
        send("運行")
    $("#運行同時編寫").click ->
        send("運行同時編寫")
    $("#打開文件夾").click ->
        send("打開文件夾")
    $("#生成exe").click ->
        send("生成exe")
    $("#生成html").click ->
        send("生成html")
    
    
    window.進入工程 = ->
        $("#入口").slideUp()
