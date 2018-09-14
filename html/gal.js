//與後端的通信器
link_on=true;	//保證同時只有一個通信
var a=new QWebChannel(qt.webChannelTransport, function (channel) {
	window.handler = channel.objects.handler;;
	send=function(str){
		if(link_on){
			link_on=false;
			window.handler.rec(str);
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

function 準備工作(){
	$("<link>")
		.attr({ rel: "stylesheet",
		type: "text/css",
		href: path+自定css
	}).appendTo("head");
	$('#总画面').css('width',解析度[0])
	$('#总画面').css('height',解析度[1])
	if(邊界) $('div').css('border','1px solid #22f');
	change_img('cover','url(static/None.png)',0);
	change_img('bg','url(static/None.png)',0);
	change_img('cg','url(static/None.png)',0);
	change_img('ch','url(static/.png)',0);
	更新()
}


function 步進更新(){
	send('步進更新');
}

function 更新(){
	send('更新')
}

function 信息預處理(data){
	if(!data.bg)
		data.bg='url(static/None.png)';
	else
		data.bg='url('+path+'img/'+data.bg+')';
	if(!data.cg)
		data.cg='url(static/None.png)';
	else
		data.cg='url('+path+'img/'+data.cg+')';

	if(data.bgm[0]!='None')
		data.bgm[0]=path+'bgm/'+data.bgm[0];
	if(data.name!='') {
		data.name='【'+data.name+'】';
		$('#name_bg').fadeIn(200);
	}else{
		data.word='　　'+data.word;
		$('#name_bg').fadeOut(200);
	}
}

//得到信息全部改變頁面
function state_Change(data) {
	信息預處理(data)
	if(data.choice.length>0){
		處理選項(data.choice);
		return
	}
	if(data.info){
		if(data.info[0]=='cut'){
			data.name=''
			data.word=''
			data.bgm=['None',0]
			插入圖(data.info[1])
		}
		if(data.info[0]=='video')
			放視頻(data.info[1])
		if(data.info[0]=='load')
			load特效()
	}
	換cg(data.cg);
	換bg(data.bg);
	換立繪(data.ch);
	換bgm(data.bgm);
	換人名(data.name);
	換對話(data.word,data.name);
}

choice_state=false;
function 處理選項(choice){
	var tot='';
	for(var i in choice)
		tot+='<button onclick="choose('+i+');">'+choice[i]+'</botton>';
	$('#choice').html(tot);
	$('#choice').show(250);
	choice_state=true
}
function choose(x){
	$('#choice').hide(250);
	send(x);
	choice_state=false
}

function 插入圖(圖){
	left_disable=true;
	$('#cover').css('display','block');
	
    $('#总画面').fadeOut(400);
	setTimeout( (function(){ change_img('cover','url('+path+'img/'+圖+')',1);})          , 400);
    $('#总画面').fadeIn(1100);
	setTimeout( (function(){ change_img('cover','url(static/None.png)',1);})          , 4500);
	setTimeout( (function(){ $('#cover').css('display','none');            })          , 5500);
	setTimeout( (function(){ 步進更新();                                  })            ,6000);
	setTimeout( (function(){ left_disable=false;    })                                 , 6500);
}

function 放視頻(視頻){
	left_disable=true;
	var v=$('video');
	v.css('display','block');
	v.attr('src',path+'video/'+視頻);
	v[0].addEventListener('ended', function () {  
		步進更新();
		setTimeout( (function(){ v[0].style.display = 'none'; left_disable=false; }) , 500);
	}, false);
	v[0].play();
}

function load特效(){
    left_disable=true;
    $('#总画面').fadeOut(0);
    $('#总画面').fadeIn(1200);
    setTimeout( (function(){ left_disable=false;    }) , 1000);
}

function 提示(x){
    $('#提示').html(x);
    $('#提示').fadeIn(300);
    $('#提示').hide(1000);
}

現在cg='None'
function 換cg(cg){
	if(cg===現在cg)
		return;
	現在cg=cg
	change_img('cg',cg,1);
}

//改變立繪
function 換立繪(text){
	$('#ch').html(text)
}	

現在bg='None'
function 換bg(bg){
	if(bg===現在bg)
		return;
	現在bg=bg
	if(bg==='None')
		bg='url(static/None.png)'
	change_img('bg',bg,1.4);
}

function 換人名(text) {
	$('#name').html(text);
	$('#history').append(text+'<br/>');
}

function 換對話(text,name) {
    if (name)
        $('#word').逐字打印(text,true);
    else
        $('#word').逐字打印(text);
    $('#history').append(text+'<br/><br/>');
}

當前曲名='None'
function 換bgm(bgm){
	var 曲名=bgm[0],音量=bgm[1];
	var au=$('#bgm');
	if(當前曲名==曲名) return;
	當前曲名=曲名
	if(當前曲名=='None'){
		au.stop()
		au.animate({volume: 0}, 2000);
		setTimeout( (function(){ au.attr('src',當前曲名); }) , 2000);
	}else{
		au.stop()
        au.attr('src',當前曲名);
        au.animate({volume: 0}, 0);
		au.animate({volume: 音量}, 2000);
	}
}
//改變圖像，通用，bg和ch都會用到
function change_img(dst,img_b,time){
	var frame='A'+Math.ceil(Math.random()*999999).toString();
	var img_a;
	dst='#'+dst;
	img_a=$(dst).attr('my_img');
	
	$(dst).css('animation','');
	$('#style').append('@keyframes '+frame+'{ 0%{background-image:'+img_a+';}100%{background-image:'+img_b+';} }\n');
	$(dst).css('animation',frame+' '+time.toString()+'s');	
	$(dst).css('background-image',img_b);
	
	$(dst).attr('my_img',img_b);
}
