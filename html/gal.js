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
	setTimeout(function(){send('同步路徑')},300)
});


function 準備工作(){
	$("<link>")
		.attr({ rel: "stylesheet",
		type: "text/css",
		href: path+自定css
	}).appendTo("head");
	change_img('cover','url(static/None.png)',0);
	change_img('bg','url(static/None.png)',0);
	change_img('ch','url(static/.png)',0);
	update()
}


//步進並更新頁面
function go_update(){
	send('步進更新');
}

//更新頁面
function update(){
	send('更新')
}

//信息預處理
function predeal(data){
	if(data.bg=='')
		data.bg='url(static/None.png)';
	else
		data.bg='url('+path+'img/'+data.bg+')';
	if(data.bgm!='None')
		data.bgm=path+'bgm/'+data.bgm;
	if(data.ch)
		data.ch='url('+path+'ch/'+data.ch+'.png)';
	else
		data.ch='url(static/no_ch.png)'
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
		deal_info(data.info);
	change_ch(data.ch);
	change_bg(data.bg);
	change_bgm(data.bgm);
	change_name(data.name);
	change_word(data.word)
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

//處理特殊信息
function deal_info(info){
	if(info[0]=='cut'){
		left_disable=true;
		setTimeout( (function(){ $('#cover').css('display','block');         })            , 1500);
		setTimeout( (function(){ change_img('cover','url('+path+'img/'+info[1]+')',3);  }) , 1500);
		setTimeout( (function(){ change_img('cover','url(static/None.png)',1); })          , 6000);
		setTimeout( (function(){ $('#cover').css('display','none');            })          , 7000);
		setTimeout( (function(){ go_update();                                  })          , 7500);
		setTimeout( (function(){ left_disable=false;    })                                 , 8000);
	}
	if(info[0]=='video'){
		left_disable=true;
		var v=$('video');
		v.css('display','block');
		v.attr('src',path+'video/'+info[1]);
		v[0].addEventListener('ended', function () {  
			go_update();
			setTimeout( (function(){ v[0].style.display = 'none'; left_disable=false; }) , 500);
		}, false);
		v[0].play();
	}
}

//改變立繪
function change_ch(text){
	change_img('ch',text,0.4);
}	
//改變背景
function change_bg(text){
	if(text===$('#bg').css('background-image')) return;
	change_img('bg',text,2.4);
}
//改變名字
function change_name(text) {
	$('#name').html(text);
	$('#history').append(text+'<br/>');
}
//改變文本
function change_word(text) {
	// $('#word').lbyl( { content:text, speed:22, type:'fade', fadeSpeed:85 } );
	$('#word').逐字打印(text);
	$('#history').append(text+'<br/><br/>');
}
//改變背景音樂
function change_bgm(text){
	var au=$('audio');
	if(text===au.attr('src')) return;
	if(text=='None'){
		au.animate({volume: 0}, 1000);
		setTimeout( (function(){ au.attr('src',text); }) , 1000);
		return
	}
	au.animate({volume: 1}, 0);
	au.attr('src',text);
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
