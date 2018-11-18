控制={
	右鍵功能() {
		window.event.returnValue = false;
		$('#對話框').fadeToggle(250);
		$('.scroll').fadeOut(200);
	},
	
	左鍵屏蔽:false,
	左鍵功能() {
		if (this.左鍵屏蔽||this.選擇之刻)
			return;
		if ($('#對話框').is(':hidden')) {
			$('.scroll').fadeOut(200);
			$('#對話框').fadeIn(250);
		} else {
			if(待打印文字){
				e=$('#話語')
				e.attr('f',e.attr('f')+待打印文字)
				e.html(e.attr('f'))
				待打印文字=''
			}
			else
				演出.步進更新();
		}
	},
	
	顯示履歷() {
		if (!($('.scroll').is(':hidden'))) 
			return;
		$('#對話框').fadeOut(200);
		$('.scroll').show(0);
		$('.scroll').animate({scrollTop:99999999},0);
	},
	
	//skip功能
	正在快進:false,
	快進() {
		if (this.正在快進 == false) {
			this.正在快進 = true;
			this.快進輪迴();
		} else
			this.正在快進 = false;
	},
	快進輪迴() {
		if (控制.正在快進 == false)
			return;
		else {
			控制.左鍵功能();
			setTimeout(控制.快進輪迴, 65);
		}
	},
	
	進入設置() {
		$('#配置面板').fadeIn(300);
	},
	退出設置() {
		$('#配置面板').fadeOut(300);
	},
};

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
	$('#adv畫面').mousewheel(function (event, delta) {
		if (delta > 0)
			控制.顯示履歷();
		if (delta < 0){
			if($('.scroll').is(':hidden'))
				控制.左鍵功能();
		}
	});
	$("#adv畫面").mousedown(function(e) {
    	if (3 == e.which) {
    		控制.右鍵功能();
    	} else if (1 == e.which) {
    		控制.左鍵功能();
    	}
	})
});