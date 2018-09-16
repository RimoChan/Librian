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
$(function() {
	初始化()
});
function 初始化(){
	try{
        send('初始化');
    }
    catch(err){
        setTimeout(初始化,35)
    }
}