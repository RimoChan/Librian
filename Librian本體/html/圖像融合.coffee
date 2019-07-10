window.圖像融合 =
    緩存: {} ,
    圖像融合: (圖片名組, f) ->
        緩存 = this.緩存
        if 緩存[圖片名組.toString()]
            console.log '用緩存'
            t = this.緩存[圖片名組.toString()]
            f(t[0], t[1])
        m = 0
        圖片組 = []
        for i in 圖片名組
            t = new Image()
            t.src = i[0]
            t.setAttribute("crossOrigin", 'Anonymous')
            t.偏移x = i[1]
            t.偏移y = i[2]
            圖片組.push(t)
            t.onload = ->
                m += 1
                if m == 圖片名組.length
                    go(緩存)
        go = (緩存)->
            極x = Math.max.apply(Math, (圖片.width + 圖片.偏移x for 圖片 in 圖片組))
            極y = Math.max.apply(Math, (圖片.height + 圖片.偏移y for 圖片 in 圖片組))

            canvas = document.createElement("canvas")
            canvas.width = 極x
            canvas.height = 極y

            context = canvas.getContext("2d")
            for 圖片 in 圖片組
                context.drawImage(圖片, 圖片.偏移x , 圖片.偏移y , 圖片.width , 圖片.height)

            base64 = canvas.toDataURL("image/png")
            緩存[圖片名組.toString()] = [[極x, 極y], base64]

            f([極x, 極y], base64)

    融合到div: (圖片名組, 時間, dv) ->
        this.圖像融合(圖片名組, (尺寸, base64) ->
            dv = document.getElementById(dv)
            if 時間 > 0
                dv.style.transition = "background #{時間}s, width #{時間}s, height #{時間}s, top #{時間}s, left #{時間}s, transform #{時間}s"
            else
                dv.style.transition = ""
            dv.style.width = 尺寸[0]
            dv.style.height = 尺寸[1]
            dv.style.backgroundImage = "url(#{base64})"
        )


# window.onload = ->
#     融合到div([
#         ['體.png', 2, 156],
#         ['0.png', 423, 338],
#     ], 1)
#
#     document.getElementById('avatar').onclick=->
#         融合到div([
#             ['體.png', 2, 156],
#             ['1.png', 425, 336]
#         ], 0.5)
