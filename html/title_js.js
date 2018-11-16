//與後端的通信器
link_on=true;	//保證同時只有一個通信
var a=new QWebChannel(qt.webChannelTransport, function (channel) {
	window.handler = channel.objects.handler;;
	send=function(s1,s2){
		if(link_on){
			link_on=false;
			if(!s2)
				window.handler.rec1(s1)
			else
				window.handler.rec2(s1,s2)
		}
	};
});

function 開始(){
	send('步進'); 
	window.location.href='/html/adv.html';
}

function 從title讀檔(){
	send('從title讀檔')
}

function 從劇本開始(劇本){
	send('從劇本開始',劇本); 
}

function setting(){
	
}