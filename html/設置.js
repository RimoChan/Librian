設置=new Object();
設置.內容=new Object();
設置.內容.文字速度=25;
設置.內容.對話框背景透明度=0.8;
設置.內容.總體音量=1;
設置.內容.自動收起控制面板=false;
設置.初始化 = function(){
    $('#文字速度').attr('value',設置.內容.文字速度);
    $('#對話框背景透明度').attr('value',設置.內容.對話框背景透明度);
    $('#總體音量').attr('value',設置.內容.總體音量);
    $('#自動收起控制面板').attr("checked", 設置.內容.自動收起控制面板); 
    設置.同調適用()
}
設置.應用用戶設置 = function (s){
    設置.內容=JSON.parse(s); 
    設置.初始化();
}
設置.同調 = function (element){
    var e = $(element)
    if(e.attr('type')=='checkbox')
        設置.內容[e.attr('id')]=e.is(':checked')
    else
        設置.內容[e.attr('id')]=e.val()
    設置.同調適用(); 
};
設置.同調適用 = function 同調適用(){
    $('#dialog_bg').css('opacity',設置.內容.對話框背景透明度);
    if(設置.內容.自動收起控制面板)
        $('#tool').attr('class', '自動收起');
    else
        $('#tool').attr('class', '');
    send('設置',JSON.stringify(設置.內容))
}

$(function(){
    設置.初始化(); 
})