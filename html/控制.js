控制=new Object();

控制.右鍵功能 = function() {
	window.event.returnValue = false;
	$('#dialog').fadeToggle(250);
	$('.scroll').fadeOut(200);
	$('#dialog_bg').fadeToggle(250);
}

控制.左鍵屏蔽 = false;
控制.左鍵功能 = function() {
	if ((控制.左鍵屏蔽)||(演出.選擇之刻))
		return;
	if ($('#dialog').is(':hidden')) {
		$('.scroll').fadeOut(200);
		$('#dialog').fadeIn(250);
		$('#dialog_bg').fadeIn(250);
	} else {
		if(待打印文字){
			e=$('#word')
			e.attr('f',e.attr('f')+待打印文字)
			e.html(e.attr('f'))
			待打印文字=''
		}
		else
			演出.步進更新();
	}
}

控制.顯示履歷 = function() {
	if (!($('.scroll').is(':hidden'))) 
		return;
	$('#dialog').fadeOut(200);
	$('#dialog_bg').fadeOut(200);
	$('.scroll').show(0);
	$('.scroll').animate({scrollTop:99999999},0);
}

//skip功能
控制.正在快進 = false;
控制.快進 = function() {
	if (控制.正在快進 == false) {
		控制.正在快進 = true;
		控制.快進輪迴();
	} else
		控制.正在快進 = false;
}
控制.快進輪迴 = function() {
	if (控制.正在快進 == false)
		return;
	else {
		控制.左鍵功能();
		setTimeout(控制.快進輪迴, 65);
	}
}

控制.進入設置 = function() {
	$('#config').fadeIn(300);
}
控制.退出設置 = function() {
	$('#config').fadeOut(300);
}


window.document.onkeydown = function(evt){
	k=evt.keyCode

	//[ctrl] skip
	if(k==17)
		控制.快進()
	//[空格 回車 z] 左鍵
	if((k==32)||(k==13)||(k==90))
		控制.左鍵功能()
	//[esc] 右鍵
	if(k==27)
		控制.右鍵功能()
	//[Page_up] 歷史
	if(k==33)
		控制.顯示履歷()
}
window.document.onkeyup = function(evt){
	//[ctrl] skip
	if(evt.keyCode==17)
		控制.快進()
}



//滚轮功能
$(function () {
	$('#tot').mousewheel(function (event, delta) {
		if (delta > 0)
			控制.顯示履歷();
		if (delta < 0){
			if($('.scroll').is(':hidden'))
				控制.左鍵功能();
		}
	});
	$("#tot").mousedown(function(e) {
    if (3 == e.which) {
    	控制.右鍵功能();
    } else if (1 == e.which) {
    	控制.左鍵功能();
    }
})
});