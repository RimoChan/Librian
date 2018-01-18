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


//步進並更新頁面
function 步進更新(){
	send('步進更新');
}

//更新頁面
function 更新(){
	send('更新')
}

//信息預處理
function predeal(data){
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
function state_Change( data ) {
	predeal(data)
	if(data.choice.length>0){
		deal_choice(data.choice);
		return
	}
	if(data.info)
		處理額外信息(data.info);
	換cg(data.cg);
	換bg(data.bg);
	換立繪(data.ch);
	換bgm(data.bgm);
	換人名(data.name);
	換對話(data.word);
}

//處理選項
choice_state=false;
function deal_choice(choice){
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

function 處理額外信息(info){
	if(info[0]=='cut'){
		left_disable=true;
		setTimeout( (function(){ $('#cover').css('display','block');         })            , 1500);
		setTimeout( (function(){ change_img('cover','url('+path+'img/'+info[1]+')',3);  }) , 1500);
		setTimeout( (function(){ change_img('cover','url(static/None.png)',1); })          , 6000);
		setTimeout( (function(){ $('#cover').css('display','none');            })          , 7000);
		setTimeout( (function(){ 步進更新();                                  })          , 7500);
		setTimeout( (function(){ left_disable=false;    })                                 , 8000);
	}
	if(info[0]=='video'){
		left_disable=true;
		var v=$('video');
		v.css('display','block');
		v.attr('src',path+'video/'+info[1]);
		v[0].addEventListener('ended', function () {  
			步進更新();
			setTimeout( (function(){ v[0].style.display = 'none'; left_disable=false; }) , 500);
		}, false);
		v[0].play();
	}
    if(info[0]=='load'){
        left_disable=true;
        $('#总画面').fadeOut(0);
        $('#总画面').fadeIn(1200);
        setTimeout( (function(){ left_disable=false;    }) , 1000);
    }
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
	change_img('bg',bg,1.4);
}

//改變名字
function 換人名(text) {
	$('#name').html(text);
	$('#history').append(text+'<br/>');
}
//改變文本
function 換對話(text) {
	// $('#word').lbyl( { content:text, speed:22, type:'fade', fadeSpeed:85 } );
	$('#word').逐字打印(text);
	$('#history').append(text+'<br/><br/>');
}
//改變背景音樂
function 換bgm(bgm){
	var 曲名=bgm[0],音量=bgm[1];
	var au=$('audio');
	if(曲名===au.attr('src')) return;
	if(曲名=='None'){
		au.animate({volume: 0}, 1000);
		setTimeout( (function(){ au.attr('src','None'); }) , 1000);
	}else{
		au.animate({volume: 音量}, 0);
		au.attr('src',曲名);
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
