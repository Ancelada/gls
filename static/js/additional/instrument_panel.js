//**********************************************
// панель инструментов
//**********************************************

$('.show_hide_button').on('click', function(){
	$('.instrument_block').css('right', 0);
});

$('.close_panel').on('click', function(){
	$('.instrument_block').css('right', '-100%');
});