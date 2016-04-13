//*********************************
//**Идентификатор / ФИО
//*********************************
//выбор tag_id, меняем фио
$('body').delegate('#identificator', 'change', function(e){
	parameters = {}
	var optionSelected = $('option:selected', this);
	parameters['tag_id'] = this.value;
	parameters['method'] = 'tagchange';
	identificator(parameters);
});
//выбор фио, меняем tag_id
$('body').delegate('#tagname', 'change', function(e){
	parameters = {}
	var optionSelected = $('option:selected', this);
	parameters['tag_id'] = this.value;
	parameters['method'] = 'namechange';
	identificator(parameters);
});

function identificator(parameters){
	$.ajax({
		type: "POST",
		url: "/reportparameters/"+report_id,
		data: JSON.stringify(parameters),
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		async: true,
		success: function(data, textStatus, jqXHR){
			$('#identselect').html(data['string']);
		}
	});
}

//выбор периода с и периода
$(function(){
	$('#from').fdatepicker({
		format: 'dd-mm-yyyy hh:ii',
		disableDblClickSelection: true,
		language: 'ru',
		pickTime: true
	});
	$('#to').fdatepicker({
		format: 'dd-mm-yyyy hh:ii',
		disableDblClickSelection: true,
		language: 'ru',
		pickTime: true
	});
});

//структурное подразделение
//если выбрана структурное подразделение structure radio
$('#instructure').delegate('input[type=radio][id=structure]', 'change', function(){
	parameters = {};
	parameters['method'] = 'structure';
	instructure(parameters);
});

//selected scene_id
$('body').delegate('#scene_id', 'change', function(e){
	parameters = {}
	var optionSelected = $('option:selected', this);
	parameters['landscape_id'] = this.value;
	parameters['method'] = 'scene_idchange';
	instructure(parameters);
});

//selected scenename
$('body').delegate('#scenename', 'change', function(e){
	parameters = {}
	var optionSelected = $('option:selected', this);
	parameters['landscape_id'] = this.value;
	parameters['method'] = 'scenenamechange';
	instructure(parameters);
});

function instructure(parameters){
	$.ajax({
		type: "POST",
		url: "/reportparameters/"+report_id,
		data: JSON.stringify(parameters),
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		async: true,
		success: function(data, textStatus, jqXHR){
			$('#instructure').html(data['string']);
		}
	})
}

//checkbox указать строение
$('body').delegate('#checkbuilding', 'change', function(){
	if (this.checked){
		parameters = {}
		parameters['landscape_id'] = $('#scene_id option:selected')[0].value;
		parameters['method'] = 'choosebuilding';
		chooseElem(parameters, 'building');
	} else {
		$('#buildingselect').html('');
	}
});

//building option selected
$('body').delegate('#building', 'change', function(e){
	$('#floorselect').html('');
	$('#checkfloor')[0].checked = false;
});

//checkbox указать этаж
$('body').delegate('#checkfloor', 'change', function(){
	if (this.checked){
		parameters = {}
		parameters['building_id'] = $('#building option:selected')[0].value;
		parameters['method'] = 'choosefloor';
		chooseElem(parameters, 'floor');
	} else {
		$('#floorselect').html('');
	}
})

$('body').delegate('#floor', 'change', function(e){
	$('#kabinetselect').html('');
	$('#checkkabinet')[0].checked = false;
});

//checkbox указать кабинет
$('body').delegate('#checkkabinet', 'change', function(){
	if(this.checked){
		parameters = {}
		parameters['floor_id'] = $('#floor option:selected')[0].value;
		parameters['method'] = 'choosekabinet';
		chooseElem(parameters, 'kabinet');
	} else {
		$('#kabinetselect').html('')
	}
})

function chooseElem(parameters, elemType){
	$.ajax({
		type: "POST",
		url: "/reportparameters/"+report_id,
		data: JSON.stringify(parameters),
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		async: true,
		success: function(data, textStatus, jqXHR){
			if(elemType=='building'){
				$('#buildingselect').html(data['string']);
			} else if (elemType=='floor'){
				$('#floorselect').html(data['string']);
			} else if (elemType=='kabinet'){
				$('#kabinetselect').html(data['string'])
			}
		}
	});
}

//зона пользователя/ группа зон пользователя
//если выбрана зона пользователя / группа зон пользоватея uzone radio
$('#instructure').delegate('input[type=radio][id=uzone]', 'change', function(){
	$('div#structure').html('');
	parameters = {}
	parameters['user_id'] = user_id;
	parameters['method'] = 'inuzone';
	instructure(parameters);
});

//radio uzerzone
$('#instructure').delegate('input#userzone', 'change', function(){
	//снимаем отметку "указать группу зон пользователя"
	$('#uzonegroupselect')[0].checked = false;
	//очищаем uzonegrouplist
	$('#uzonegrouplist').html('');
})

$('#instructure').delegate('input#groupuserzone', 'change', function(){
	//снимаем отметку "указать зону пользователя"
	$('#uzoneselect')[0].checked = false;
	//очищаем uzonelist
	$('#uzonelist').html('');
});

//checkbox указать зону пользователя uzoneselect
$('#instructure').delegate('#uzoneselect', 'change', function(){
	if (this.checked){
		parameters = {}
		parameters['user_id'] = user_id;
		parameters['method'] = 'uzoneselect';
		uzone(parameters, parameters['method']);
		//снимаем отметку "указать группу зон пользователя"
		$('#uzonegroupselect')[0].checked = false;
		//ставим radiobutton "Все зоны пользователей"
		$('input#userzone')[0].checked = true;
	} else {
		$('#uzonelist').html('');
	}
});

//checkbox указать группу зон пользователя uzonegroupselect
$('#instructure').delegate('#uzonegroupselect', 'change', function(){
	if (this.checked){
		parameters = {}
		parameters['user_id'] = user_id;
		parameters['method'] = 'uzonegroupselect';
		uzone(parameters, parameters['method']);
		//снимаем отметку "указать зону пользователя"
		$('#uzoneselect')[0].checked = false;
		//ставим radiobutton "Все группы зон пользователей"
		$('input#groupuserzone')[0].checked = true;
	} else {
		$('#uzonegrouplist').html('');
	}
});

function uzone(parameters, method){
	$.ajax({
		type: "POST",
		url: "/reportparameters/"+report_id,
		data: JSON.stringify(parameters),
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		async: true,
		success: function(data, textStatus, jqXHR){
			if(method=='uzoneselect'){
				$('#uzonelist').html(data['string']);
				$('#uzonegrouplist').html('');
			} else if (method=='uzonegroupselect'){
				$('#uzonegrouplist').html(data['string']);
				$('#uzonelist').html('');
			}
		}
	});	
}
//checkbox all
$('#instructure').delegate('input#all', 'change', function(){
	$('div#structure').html('');
	$('div#uzone').html('');
});
//******************************
//кнопка "сформировать" proccess
//******************************
$('body').delegate('#proccess', 'click', function(){
	var parameters = [];
	no = 0;
	$.each($('.reportparameter'), function(index){
		parameters.push({'id': parseInt($(this).attr('data-id')), 'parameters': {}});
		//наполняем параметры идентификатора
		if ($(this).attr('data-id') == 1){
			parameters[no]['parameters']['tag_id'] = $('#identificator option:selected')[0].value;
			parameters[no]['parameters']['name'] = $('#tagname option:selected')[0].text; 
		} else if ($(this).attr('data-id') == 2) {
		//наполняем параметры интервала даты
			parameters[no]['parameters']['from'] = $('input#from').val();
			parameters[no]['parameters']['to'] = $('input#to').val();
		} else if ($(this).attr('data-id') == 3) {
			//если заполнено структурное подразделение
			//*******************
			if ($('div#structure #scene_id')[0]){
				var landscape_id = $('div#structure #scene_id option:selected')[0].value;
				parameters[no]['parameters']['structure'] = {'landscape_id': 0};
				parameters[no]['parameters']['structure']['landscape_id'] = landscape_id;
			}
			//если указано строение
			if ($('div#structure #building')[0]){
				var building_id = $('div#structure #building option:selected')[0].value;
				parameters[no]['parameters']['structure']['building_id'] = building_id;
			}
			//если указан этаж
			if ($('div#structure #floor')[0]){
				var floor_id = $('div#structure #floor option:selected')[0].value;
				parameters[no]['parameters']['structure']['floor_id'] = floor_id;
			}
			//если указан кабинет
			if ($('div#structure #kabinet')[0]){
				var kabinet_id = $('div#structure #kabinet option:selected')[0].value;
				parameters[no]['parameters']['structure']['kabinet_id'] = kabinet_id;
			}
			//если заполнена зона пользователя
			//****************************

			//если зона пользователя берем всех
			if ($('div#uzone #userzone')[0]){
				if ($('div#uzone #userzone')[0].checked == true){
					parameters[no]['parameters']['uzone'] = {'userzone': 'all'};					
				}
			}
			//если указана конектретная зона пользователя
			if ($('div#uzone select#uzoneslist')[0]){
				var uzone_id = $('div#uzone select#uzoneslist option:selected')[0].value;
				parameters[no]['parameters']['uzone'] = {'userzone': {'id': uzone_id}};
			}

			//если группа зон пользователя берем всех
			if ($('div#uzone #groupuserzone')[0]){
				if ($('div#uzone #groupuserzone')[0].checked == true){
					parameters[no]['parameters']['uzone'] = {'groupuzone': 'all'};	
				}
			}
			// если указана конкретная группа зон пользователя
			if ($('div#uzone select#groupuzoneslist')[0]){
				var groupuzone_id = $('div#uzone select#groupuzoneslist option:selected')[0].value;
				parameters[no]['parameters']['uzone']['groupuzone'] = {'id': groupuzone_id};
			}

			if ($('div#instructure input#all')[0]){
				if ($('div#instructure input#all')[0].checked == true){
					parameters[no]['parameters']['uzone'] = {'str_n_uzone': 'all'} ;
				}
			}
		}
		no += 1;
	});
	//проверка parameters на ошибки
	var errors = [];
	$.each(parameters, function(index){
		if (parameters[index]['id'] == 2){
			if(parameters[index]['parameters']['from'].length == 0){
				errors.push({'text':'Отсутствует параметр "Период с"'})
			}
			if (parameters[index]['parameters']['to'].length == 0){
				errors.push({'text':'Отсутствует параметр "Период по"'})
			}
		}
		if (parameters[index]['id'] == 3){
			if (($('input#structure')[0].checked == false) && ($('input#uzone')[0].checked == false) && ($('input#all')[0].checked == false)) {
				errors.push({'text':'Необходимо отметить параметр "Структурное подразделение / зона пользователя"'});
			}
		}
	});
	//высветить ошибки
	if (errors.length > 0){
		parameters = {};
		parameters['method'] = 'showerrors';
		parameters['errors'] = errors;
		$.ajax({
			type: "POST",
			url: "/reportparameters/"+report_id,
			data: JSON.stringify(parameters),
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			async: true,
			success: function(data, textStatus, jqXHR){
				$('#showerrors').html(data['string']);
			}		
		});
	} else {
		$('#showerrors').html('');
		//производим отправку параметров для формирования отчета
		params = {}
		params['parameters'] = parameters;
		params['report_id'] = report_id;
		params['method'] = 'getreport';
		$.ajax({
			type: "POST",
			url: "/reportparameters/"+report_id,
			data: JSON.stringify(params),
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			async: true,
			success: function(data, textStatus, jqXHR){
				/*console.log(data);*/
				$('#result').html(data['string']);
			}
		})
	}
});