待打印文字=''
!function (e) {
	function 循环(e){
		if(待打印文字){
			while((待打印文字[0]=='<')||(待打印文字[0]=='/')){	//屏蔽html字符……
				e.attr('f',e.attr('f')+待打印文字[0])
				待打印文字=待打印文字.slice(1)
			}
			e.attr('f',e.attr('f')+待打印文字[0])
			待打印文字=待打印文字.slice(1)
			e.html(e.attr('f'))
			setTimeout(function () {
				循环(e)
			}, 25)
		}
		else{
			$('#嘀').attr('src','');
		}
	}
	e.fn.逐字打印 = function (n,嘀=false) { 
		if(嘀)
			$('#嘀').attr('src','./static/嘀.mp3');
		待打印文字=n
		d = e(this)
		d.empty()
		d.attr('f','')
		循环(d)
	}
}
(jQuery);
