import PSD from 'psd.js'


psd緩存 = {}
圖層緩存 = {}
圖緩存 = {}

export default psd拆包 = 

    獲取圖層: (psd路徑, 圖層名) ->
        if not psd緩存[psd路徑]
            psd緩存[psd路徑] = await PSD.fromURL(psd路徑)
        psd = psd緩存[psd路徑]

        key = [psd路徑, 圖層名].toString()
        if not 圖層緩存[key]
            現層 = psd.tree().childrenAtPath(圖層名)[0]
            圖層緩存[key] = {
                '位置': 現層.coords
                'img': 現層.layer.image.toPng()
            }
        return 圖層緩存[key]

    獲取圖層組: (psd路徑, 圖層名組) ->
        return (
            for i, 圖層名 of 圖層名組
                await this.獲取圖層(psd路徑, 圖層名)
        )

    圖層融合: (圖層組) ->
        m = 0
        
        極x = Math.max.apply(Math, (圖層.位置.right for 圖層 in 圖層組))
        極y = Math.max.apply(Math, (圖層.位置.bottom for 圖層 in 圖層組))

        canvas = document.createElement('canvas')
        canvas.width = 極x
        canvas.height = 極y

        context = canvas.getContext('2d')
        for 圖層 in 圖層組
            {left, top, bottom, right} = 圖層.位置
            context.drawImage(圖層.img, left, top)

        base64 = canvas.toDataURL('image/png')

        return [極x, 極y, base64]

    融合到div: (base64, width, height, 過渡時間, div名) ->
        dv = document.getElementById(div名)
        dv.style.transition = "background #{過渡時間}s, width #{過渡時間}s, height #{過渡時間}s"
        dv.style.width = width
        dv.style.height = height
        dv.style.backgroundImage = "url(#{base64})"

    渲染圖層組到div: (psd路徑, 圖層名組, div名) ->
        key = [psd路徑, 圖層名組].toString()
        if not 圖緩存[key]
            圖層組 = await this.獲取圖層組(psd路徑, 圖層名組)
            圖緩存[key] = this.圖層融合(圖層組)
        [width, height, base64] = 圖緩存[key]
        this.融合到div(base64, width, height, 0.5, div名)

    渲染png到div: (png路徑, div名) ->
        t = new Image()
        t.setAttribute("crossOrigin", 'Anonymous')
        t.src = png路徑
        t.onload = () =>
            [width, height, base64] = this.圖層融合([{
                '位置': 
                    'top': 0,
                    'left': 0,
                    'bottom': t.height,
                    'right': t.width,
                'img': t,
            }])
            this.融合到div(base64, width, height, 0.5, div名)
