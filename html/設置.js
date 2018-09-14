設置=new Object();
設置.文字速度=25
設置.對話框背景透明度=0.8
設置.總體音量=1
設置.自動收起控制面板=false
$(function(){
    初始化()
})
function 初化(){
    $('#文字速度').attr('value',設置.文字速度);
    $('#對話框背景透明度').attr('value',設置.對話框背景透明度);
    $('#總體音量').attr('value',設置.總體音量);
    $('#自動收起控制面板').attr("checked", 設置.自動收起控制面板); 
    同調適用()
}
function 應用用戶設置(s){
    設置=JSON.parse(s)
    初化()
}
function 同調(element){
    var e = $(element)
    if(e.attr('type')=='checkbox')
        設置[e.attr('id')]=e.is(':checked')
    else
        設置[e.attr('id')]=e.val()
    同調適用()
};
function 同調適用(){
    $('#dialog_bg').css('opacity',設置.對話框背景透明度);
    if(設置.自動收起控制面板)
        $('#tool').attr('class', '自動收起');
    else
        $('#tool').attr('class', '');
    send('設置',JSON.stringify(設置))
}