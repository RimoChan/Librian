window.link_on=true;    
new QWebChannel qt.webChannelTransport,(channel)->
    window.handler = channel.objects.handler
    window.send=(s1,s2)->
        if window.link_on
            window.link_on=false
            if !s2
                window.handler.rec1(s1)
            else
                window.handler.rec2(s1,s2)

$ ->
    try
        send('初始化');
    catch
        setTimeout(初始化,35)