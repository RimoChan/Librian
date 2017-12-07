
//滚轮功能
$(function () {
	$('#tot').mousewheel(function (event, delta) {
		if (delta > 0)
			log();
		if (delta < 0)
			left_click();
	});
});

//右键功能
function right_click() {
	window.event.returnValue = false;
	$('#dialog').toggle(250);
	$('.scroll').hide(200);
}

//左键功能
left_disable = false;
function left_click() {
	if ((left_disable)||(choice_state))
		return;
	if ($('#dialog').is(':hidden')) {
		$('.scroll').hide(200);
		$('#dialog').show(250)
	} else {
		if(待打印文字){
			e=$('#word')
			e.attr('f',e.attr('f')+待打印文字)
			e.html(e.attr('f'))
			待打印文字=''
		}
		else
			go_update();
	}
}

//滚动条美化
$(function () {
	$('.scroll').mCustomScrollbar();
});

//显示log，参考资料在http://www.wufangbo.com/mcustomscrollbar/
function log() {
	if ($('.scroll').is(':hidden')) {
		$('#dialog').hide(200);
		$('.scroll').show(0);
		$('.scroll').mCustomScrollbar('scrollTo', 9999999);
	}
}

//skip功能
var skip_mode = 'off';
function skip() {
	if (skip_mode == 'off') {
		skip_mode = 'on';
		skip_cycle();
	} else
		skip_mode = 'off';
}
function skip_cycle() {
	if (skip_mode == 'off')
		return;
	else {
		left_click();
		setTimeout(skip_cycle, 65);
	}
}

//键盘功能
function key_press(evt){
	k=evt.keyCode
	//ctrl键的skip
	if(k==17)
		skip()
	//空格和回车和z相当于鼠标点击
	if((k==32)||(k==13)||(k==90))
		left_click()
}
function key_free(evt){
	if(evt.keyCode==17)
		skip()
}
window.document.onkeydown = key_press;
window.document.onkeyup = key_free;

// $(document).keypress(function(e) {
// 	if (e.altKey && e.which == 13) 
// 		send('换全屏')
// })

//切换到config界面
function config() {
	$('#config').fadeIn(300);
}
function exit_config() {
	$('#config').fadeOut(300);
}
