//与后端的通信器
link_on=true;	//保证同时只有一个通信
var a=new QWebChannel(qt.webChannelTransport, function (channel) {
	window.handler = channel.objects.handler;;
	send=function(str){
		if(link_on){
			link_on=false;
			window.handler.rec1(str);
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

function extra(){
	
}

function setting(){
	
}