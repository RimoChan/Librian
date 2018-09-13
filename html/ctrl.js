//滚轮功能
$(function () {
	$('#tot').mousewheel(function (event, delta) {
		if (delta > 0)
			顯示履歷();
		if (delta < 0){
			if($('.scroll').is(':hidden'))
				左鍵功能();
		}
	});
	$("#tot").mousedown(function(e) {
    if (3 == e.which) {
    	右鍵功能();
    } else if (1 == e.which) {
    	左鍵功能();
    }
})
});

function 右鍵功能() {
	window.event.returnValue = false;
	$('#dialog').fadeToggle(250);
	$('.scroll').fadeOut(200);
	$('#dialog_bg').fadeToggle(250);
}

left_disable = false;
function 左鍵功能() {
	if ((left_disable)||(choice_state))
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
			步進更新();
	}
}

function 顯示履歷() {
	if (!($('.scroll').is(':hidden'))) 
		return;
	$('#dialog').fadeOut(200);
	$('#dialog_bg').fadeOut(200);
	$('.scroll').show(0);
	$('.scroll').animate({scrollTop:99999999},0);
}

//skip功能
var skip_mode = false;
function skip() {
	if (skip_mode == false) {
		skip_mode = true;
		skip_cycle();
	} else
		skip_mode = false;
}
function skip_cycle() {
	if (skip_mode == false)
		return;
	else {
		左鍵功能();
		setTimeout(skip_cycle, 65);
	}
}


window.document.onkeydown = function(evt){
	k=evt.keyCode

	//[ctrl] skip
	if(k==17)
		skip()
	//[空格 回車 z] 左鍵
	if((k==32)||(k==13)||(k==90))
		左鍵功能()
	//[esc] 右鍵
	if(k==27)
		右鍵功能()
	//[Page_up] 歷史
	if(k==33)
		顯示履歷()
}
window.document.onkeyup = function(evt){
	//[ctrl] skip
	if(evt.keyCode==17)
		skip()
}

//切换到config界面
function config() {
	$('#config').fadeIn(300);
}
function exit_config() {
	$('#config').fadeOut(300);
}

