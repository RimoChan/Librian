//与后端的通信器
link_on=true;	//保证同时只有一个通信
var a=new QWebChannel(qt.webChannelTransport, function (channel) {
	window.handler = channel.objects.handler;;
	send=function(str){
		if(link_on){
			link_on=false;
			window.handler.rec(str);
		}
	};
});

function game_continue(){
	send('从title继续')
}

function extra(){
	
}

function setting(){
	
}