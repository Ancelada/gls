//**********************************************
// панель сессий
//**********************************************
$('body').delegate('.show_hide_session_button', 'click', function(){
	$('.session_block').css('right', 0);
});

$('body').delegate('.close_session_panel', 'click', function(){
	$('.session_block').css('right', '-100%');
});

//************************************************
//** Получить список сессий
$('.session_block').delegate('#getsessionlist', 'click', function(){
	$('#notification').html('');
	parameters = {};
	parameters['method'] = 'getsessionlist';
	serverRequest(parameters);
});
//**Отправить сессию
$('body').delegate('#sendsession', 'click', function(){
	//параметры сессии
    session['session']['name'] = $('#sessionname').val();
    session['session']['password'] = $('#sessionpassword').val();
    session['session']['idLayer'] = parseInt($('#layerid').val());
    // параметры layer
    session['layer']['id'] = parseInt($('#layerid').val());
    session['layer']['name'] = $('#layername').val();

	$('#notification').html('');
	parameters = {};
	parameters['data'] = session;
	parameters['method'] = 'sendsession';
	parameters['landscape_id'] = landscape_id;
	serverRequest(parameters);
});

function serverRequest(parameters){
	$.ajax({
		type: "POST",
		url: "/landscapetreeload/"+landscape_id,
		data: JSON.stringify(parameters),
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		async: true,
		success: function(data, textStatus, jqXHR){
			$('#notification').html(data['string']);
			console.log(data['string']);
		}
	});
}
//**********************************************
// панель инструментов
//**********************************************

$('body').delegate('.show_hide_button', 'click', function(){
	$('.instrument_block').css('right', 0);
});

$('body').delegate('.close_panel', 'click', function(){
	$('.instrument_block').css('right', '-100%');
});