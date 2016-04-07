//**********************************************
// панель инструментов
//**********************************************

$('body').delegate('.show_hide_button', 'click', function(){
	$('.instrument_block').css('right', 0);
});

$('body').delegate('.close_panel', 'click', function(){
	$('.instrument_block').css('right', '-100%');
});
//*******************************************
// панель интструментов динамики
//*******************************************

//показвать принадлежность зоне пользователя userzone
$('body').delegate('.static_instrument_block #belongtouzone', 'click', function(){
	tag_id = $(this).attr('data-id');
	txt = $(this).text();
	if (txt == 'Показывать принадлежность зоне пользователя'){
		$(this).text('Остановить');
		belongToUsone('start', tag_id, username);
	} else {
		scene.remove(lightedUpUzonePlane);
		$(this).text('Показывать принадлежность зоне пользователя');
		belongToUsone('stop', tag_id, username);
	}
});

function belongToUsone(type, tag_id, uname){
	$.ajax({
		type: "POST",
		url: "/getbelonguzone",
		data: JSON.stringify({'tag_id': tag_id, 'user_id': uname, 'type': type}),
		contentType: "application/json; charset=utf-8",
		dataType: "html",
		async: true,
		success: function(data, textStatus, jqXHR){
			console.log(data);
		}
	})
}

//показывать принадлежность
$('body').delegate('.static_instrument_block #belong', 'click', function(){
	tag_id = $(this).attr('data-id');
	txt = $(this).text();
	if (txt == 'Показывать принадлежность'){
		$(this).text('Остановить');
		belong('start', tag_id, username);
	} else {
		scene.remove(lightedUpPlane);
		$(this).text('Показывать принадлежность');
		belong('stop', tag_id, username);
	}
});

function belong(type, tag_id, uname){
	$.ajax({
		type: "POST",
		url: "/getbelong",
		data: JSON.stringify({'tag_id': tag_id, 'user_id': uname, 'type': type}),
		contentType: "application/json; charset=utf-8",
    	dataType: "html",
    	async: true,
    	success: function(data, textStatus, jqXHR){
    		console.log(data);
    	}	
	});
}

//*******************************************
// панель инструментов статики
//*******************************************
$('body').delegate('.show_hide_static_button', 'click', function(){
	$('.static_instrument_block').css('right', 0);
});

$('body').delegate('.close_static_panel', 'click', function(){
	$('.static_instrument_block').css('right', '-100%');
});
//панель зоны пользователя
//**********************************************
$('.user_zone_button').on('click', function(){
	$('.userzone_panel').css('right', 0);
});

$('.close_userzone_panel').on('click', function(){
	$('.userzone_panel').css('right', '-100%');
});
//панель зоны входа
//**********************************************
$('.income_zone_button').on('click', function(){
	$('.incomezone_panel').css('right', 0);
});

$('.close_incomezone_panel').on('click', function(){
	$('.incomezone_panel').css('right', '-100%');
});
//панель зоны исключения
//**********************************************
$('.exclude_zone_button').on('click', function(){
	$('.excludezone_panel').css('right', 0);
});

$('.close_excludezone_panel').on('click', function(){
	$('.excludezone_panel').css('right', '-100%');
});

//переименовать userzone
$('body').delegate('#rename_userzone', 'click', function(){
	zoneid = $(this).attr('data-id');
	name = $(this).next().children('li').children('input').val();
	$.ajax({
		type: "POST",
		url: "/incomezonedefine/"+landscape_id,
		data: JSON.stringify({'method': 'rename_userzone', 'zoneid': zoneid, 'name': name, 'landscape_id': landscape_id}),
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		async: true,
		success: function(data, textStatus, jqXHR){
			$('#userzonetable').html(data['userzonetable']);
			$('#uzonegrouptable').html(data['uzonegrouptable']);
			$('#zonetable').html(data['zonetable']);
			$('#excludezonetable').html(data['excludezonetable']);
		}
	});
});

//переименовать uzonegrouptable
$('body').delegate('#renamezonegroup', 'click', function(){
	parameters = {}
	parameters['groupname'] = $(this).next().children().children().val();
	parameters['groupid'] = parseInt($(this).attr('data-id'));
	parameters['landscape_id'] = landscape_id;
	parameters['method'] = 'renamezonegroup'
	$.ajax({
		type: "POST",
		url: "/incomezonedefine/"+landscape_id,
		data: JSON.stringify(parameters),
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		async: true,
		success: function(data, textStatus, jqXHR){
			$('#uzonegrouptable').html(data['uzonegrouptable']);
		}
	});
});

//записать вершины income
$('body').delegate('#new', 'click', function(){
    if($(this).text() == 'Новая'){
        $(this).text('Остановить');
        $(this).addClass('secondary')
    } else{
    	if (vertices.length > 2){
    		$('.lessvert').hide();
	    	$(this).removeClass('secondary');
	        $(this).text('Новая');
	        $.ajax({
	        	type: "POST",
	        	url: "/incomezonedefine/"+landscape_id,
	        	data: JSON.stringify({'method': 'add', 'vertices': vertices, 'landscape_id': landscape_id}),
	        	contentType: "application/json; charset=utf-8",
	        	dataType: "html",
	        	async: true,
	        	success: function(data, textStatus, jqXHR){
	        		$('#zonetable').html(data);
	        	}
	        })
	        vertices = [];	
    	} else {
    		$('.lessvert').show()
    	}
    }
});
//записать вершины exclude
$('body').delegate('#new_exclude', 'click', function(){
    if($(this).text() == 'Новая'){
        $(this).text('Остановить');
        $(this).addClass('secondary');
    } else{
    	if (vertices.length > 2){
    		$('.exclude_lessvert').hide();
	    	$(this).removeClass('secondary');
	        $(this).text('Новая');
	        $.ajax({
	        	type: "POST",
	        	url: "/incomezonedefine/"+landscape_id,
	        	data: JSON.stringify({'method': 'addexclude', 'vertices': vertices, 'landscape_id': landscape_id}),
	        	contentType: "application/json; charset=utf-8",
	        	dataType: "html",
	        	async: true,
	        	success: function(data, textStatus, jqXHR){
	        		$('#excludezonetable').html(data);
	        	}
	        })
	        vertices = [];	
    	} else {
    		$('.exclude_lessvert').show()
    	}
    }
});
//записать вершины userzone
$('body').delegate('#new_user', 'click', function(){
	if($(this).text() == 'Новая'){
		$(this).text('Остановить');
		$(this).addClass('secondary');
	} else {
		if (vertices.length > 2){
			$('.user_lessvert').hide();
			$(this).removeClass('secondary');
			$(this).text('Новая');
			$.ajax({
				type: "POST",
				url: "/incomezonedefine/"+landscape_id,
				data: JSON.stringify({'method': 'adduzone', 'vertices': vertices, 'user_id': user_id, 'landscape_id': landscape_id}),
				contentType: "application/json: charset=utf-8",
				dataType: "json",
				async: true,
				success: function(data, textStatus, jqXHR){
					$('#userzonetable').html(data['userzonetable']);
					$('#uzonegrouptable').html(data['uzonegrouptable']);
					$('#zonetable').html(data['zonetable']);
					$('#excludezonetable').html(data['excludezonetable']);
				}
			});
			vertices = [];
		} else {
			$('.user_lessvert').show();
		}
	}
});

//удалить зону income
$('body').delegate('#delete', 'click', function(){
	zoneid = $(this).attr('data-id');
	$.ajax({
		type: "POST",
		url: "/incomezonedefine/"+landscape_id,
		data: JSON.stringify({'method': 'delete', 'landscape_id':landscape_id, 'zoneid': parseInt(zoneid)}),
		contentType: "application/json; charset=utf-8",
		dataType: "html",
		async: true,
		success: function(data, textStatus, jqXHR){
			$('#zonetable').html(data);
		}
	});
});
//удалить зону exclude
$('body').delegate('#delete_exclude', 'click', function(){
	zoneid = $(this).attr('data-id');
	$.ajax({
		type: "POST",
		url: "/incomezonedefine/"+landscape_id,
		data: JSON.stringify({'method': 'delete_exclude', 'landscape_id':landscape_id, 'zoneid': parseInt(zoneid)}),
		contentType: "application/json; charset=utf-8",
		dataType: "html",
		async: true,
		success: function(data, textStatus, jqXHR){
			$('#excludezonetable').html(data);
		}
	});
});
//удалить зону userzone
$('body').delegate('#delete_userzone', 'click', function(){
	zoneid = $(this).attr('data-id');
	$.ajax({
		type: "POST",
		url: "/incomezonedefine/"+landscape_id,
		data: JSON.stringify({'method': 'delete_userzone', 'landscape_id': landscape_id, 'zoneid': parseInt(zoneid)}),
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		async: true,
		success: function(data, textStatus, jqXHR){
			$('#userzonetable').html(data['userzonetable']);
			$('#uzonegrouptable').html(data['uzonegrouptable']);
			$('#zonetable').html(data['zonetable']);
			$('#excludezonetable').html(data['excludezonetable']);
		}
	});
});

//прицепить к объекту incomezone
$('body').delegate('#link', 'click', function(){
	zoneid = $(this).attr('data-zoneid');
	id = $(this).attr('data-id');
	type = $(this).attr('data-type');
	$.ajax({
		type: "POST",
		url: "/incomezonedefine/"+landscape_id,
		data: JSON.stringify({'method': 'link', 'landscape_id': landscape_id, 'zoneid': zoneid, 'type': type, 'id': parseInt(id)}),
		contentType: "application/json; charset=utf-8",
		dataType: "html",
		async: true,
		success: function(data, textStatus, jqXHR){
			$('#zonetable').html(data);
		}
	});
});

//прицепить userzone к incomezone
$('body').delegate('#linkIncomeZoneToUserZone', 'click', function(){
	parameters = {};
	parameters['izone'] = $(this).attr('data-izone');
	parameters['uzone'] = $(this).attr('data-uzone');
	parameters['landscape_id'] = landscape_id;
	parameters['method'] = 'linkincomezonetouserzone';
	$.ajax({
		type: "POST",
		url: "/incomezonedefine/"+landscape_id,
		data:JSON.stringify(parameters),
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		async: true,
		success: function(data, textStatus, jqXHR){
			$("#zonetable").html(data['zonetable']);
		}
	});
});

//отцепить userzone от incomezone
$('body').delegate('#unlinkIncomeZoneToUserZone', 'click', function(){
	parameters = {};
	parameters['izuz'] = parseInt($(this).attr('data-izuz'));
	parameters['landscape_id'] = landscape_id;
	parameters['method'] = 'unlinkincomezonetouserzone';
	$.ajax({
		type: "POST",
		url: "/incomezonedefine/"+landscape_id,
		data:JSON.stringify(parameters),
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		async: true,
		success: function(data, textStatus, jqXHR){
			$("#zonetable").html(data['zonetable']);
		}
	});
});

//прицепить userzone к excludezone
$('body').delegate('#linkExcludeZoneToUserZone', 'click', function(){
	parameters = {};
	parameters['ezone'] = $(this).attr('data-ezone');
	parameters['uzone'] = $(this).attr('data-uzone');
	parameters['landscape_id'] = landscape_id;
	parameters['method'] = 'linkexcludezonetouserzone';
	$.ajax({
		type: "POST",
		url: "/incomezonedefine/"+landscape_id,
		data: JSON.stringify(parameters),
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		async: true,
		success: function(data, textStatus, jqXHR){
			$('#excludezonetable').html(data['excludezonetable']);
		}
	});
});

//отцепить userzone от excludezone
$('body').delegate('#unlinkExcludeZoneToUserZone', 'click', function(){
	parameters = {};
	parameters['ezuz'] = parseInt($(this).attr('data-ezuz'));
	parameters['landscape_id'] = landscape_id;
	parameters['method'] = 'unlinkexcludezonetouserzone';
	$.ajax({
		type: "POST",
		url: "/incomezonedefine/"+landscape_id,
		data:JSON.stringify(parameters),
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		async: true,
		success: function(data, textStatus, jqXHR){
			$("#excludezonetable").html(data['excludezonetable']);
		}
	});
});
//прицепить к объекту excludezone
$('body').delegate('#link_exclude', 'click', function(){
	zoneid = $(this).attr('data-zoneid');
	id = $(this).attr('data-id');
	type = $(this).attr('data-type');
	$.ajax({
		type: "POST",
		url: "/incomezonedefine/"+landscape_id,
		data: JSON.stringify({'method': 'link_exclude', 'landscape_id': landscape_id, 'zoneid': zoneid, 'type': type, 'id': parseInt(id)}),
		contentType: "application/json; charset=utf-8",
		dataType: "html",
		async: true,
		success: function(data, textStatus, jqXHR){
			$('#excludezonetable').html(data);
		}
	});
});
//прицепить к объекту userzone
$('body').delegate('#link_uzone', 'click', function(){
	zoneid = $(this).attr('data-zoneid');
	id = $(this).attr('data-id');
	type = $(this).attr('data-type');
	$.ajax({
		type: "POST",
		url: "/incomezonedefine/"+landscape_id,
		data: JSON.stringify({'method': 'link_uzone', 'zoneid': zoneid, 'landscape_id': landscape_id, 'type': type, 'id': parseInt(id)}),
		contentType: "application/json; charset=utf-8",
		dataType: "html",
		async: true,
		success: function(data, textStatus, jqXHR){
			$('#userzonetable').html(data);
		}
	});
});

//отцепить от объекта incomezone
$('body').delegate('#unlink', 'click', function(){
	zoneid = $(this).attr('data-id');
	$.ajax({
		type: "POST",
		url: "/incomezonedefine/"+landscape_id,
		data: JSON.stringify({'method': 'unlink', 'landscape_id': landscape_id, 'zoneid': zoneid}),
		contentType: "application/json; charset=utf-8",
		dataType: "html",
		async: true,
		success: function(data, textStatus, jqXHR){
			$('#zonetable').html(data);
		}
	})
});
//отцепить от объекта excludezone
$('body').delegate('#unlink_exclude', 'click', function(){
	zoneid = $(this).attr('data-id');
	$.ajax({
		type: "POST",
		url: "/incomezonedefine/"+landscape_id,
		data: JSON.stringify({'method': 'unlink_exclude', 'landscape_id': landscape_id, 'zoneid': zoneid}),
		contentType: "application/json; charset=utf-8",
		dataType: "html",
		async: true,
		success: function(data, textStatus, jqXHR){
			$('#excludezonetable').html(data);
		}
	})
});
//отцепить об объекта uzerzone
$('body').delegate('#unlink_uzone', 'click', function(){
	zoneid = $(this).attr('data-id');
	$.ajax({
		type: "POST",
		url: "/incomezonedefine/"+landscape_id,
		data: JSON.stringify({'method': 'unlink_uzone', 'landscape_id': landscape_id, 'zoneid': zoneid}),
		contentType: "application/json; charset=utf-8",
		dataType: "html",
		async: true,
		success: function(data, textStatus, jqXHR){
			$('#userzonetable').html(data);
		}
	});
});

//отметка привязанных зон в таблице incomezone
function colored(dae_elem){
	parameters = {}
	parameters['method'] = 'colored';
	parameters['landscape_id'] = landscape_id;
	if (dae_elem.indexOf('building') != -1){
		parameters['type'] = 'building';
		parameters['dae_name'] = dae_elem;
	} else if (dae_elem.indexOf('floor') != -1){
		parameters['type'] = 'floor';
		parameters['dae_name'] = dae_elem;
	} else if (dae_elem.indexOf('kabinet') != -1){
		parameters['type'] = 'kabinet';
		parameters['dae_name'] = dae_elem;
	}
	$.ajax({
		type: "POST",
		url: "/incomezonedefine/"+landscape_id,
		data: JSON.stringify(parameters),
		contentType: "application/json; charset=utf-8",
		dataType: "html",
		async: true,
		success: function(data, textStatus, jqXHR){
			$('#zonetable').html(data);
		}
	});
}

//отметка привязанных зон в таблице excludezone
function coloredexclude(dae_elem){
	parameters = {}
	parameters = {}
	parameters['method'] = 'colored_exclude';
	parameters['landscape_id'] = landscape_id;
	if (dae_elem.indexOf('building') != -1){
		parameters['type'] = 'building';
		parameters['dae_name'] = dae_elem;
	} else if (dae_elem.indexOf('floor') != -1){
		parameters['type'] = 'floor';
		parameters['dae_name'] = dae_elem;
	} else if (dae_elem.indexOf('kabinet') != -1){
		parameters['type'] = 'kabinet';
		parameters['dae_name'] = dae_elem;
	}
	$.ajax({
		type: "POST",
		url: "/incomezonedefine/"+landscape_id,
		data: JSON.stringify(parameters),
		contentType: "application/json; charset=utf-8",
		dataType: "html",
		async: true,
		success: function(data, textStatus, jqXHR){
			$('#excludezonetable').html(data);
		}
	});
}

//показать зоны, принадлежащие группе userzone
$('body').delegate('#showzonegroup', 'click', function(){
	parameters = {}
	parameters['method'] = 'colored_uzone';
	parameters['landscape_id'] = landscape_id;
	parameters['ugrzoneid'] = parseInt($(this).attr('data-id'));
	$.ajax({
		type: "POST",
		url: "/incomezonedefine/"+landscape_id,
		data: JSON.stringify(parameters),
		contentType: "application/json: charset=utf-8",
		dataType: "json",
		async: true,
		success: function(data, textStatus, jqXHR){
			$('#userzonetable').html(data['userzonetable']);
			//показываем зону пользователя
			showZonesOfGroup(data['mesh']);
			izones = []
			ezones = []
			$.each(data['mesh'], function(index){
				$.each(data['mesh'][index]['izones'], function(ind){
					izones.push(data['mesh'][index]['izones'][ind]);
				});
			})
			$.each(data['mesh'], function(index){
				$.each(data['mesh'][index]['ezones'], function(ind){
					ezones.push(data['mesh'][index]['ezones'][ind]);
				})
			})
			showIncomeZones(izones);
			showExcludeZones(ezones);
		}
	});
});

function showZonesOfGroup(arr){
	$.each(Obj_I_uZone, function(index){
		scene.remove(Obj_I_uZone[index]['mesh']);
	});
	$.each(Obj_I_uZoneUp, function(index){
		scene.remove(Obj_I_uZoneUp[index]['mesh']);
	});
	Obj_I_uZone = [];
	Obj_I_uZoneUp = [];
	$.each(arr, function(index){
		var uZoneVert = [];
		var uZoneVertUp = [];
		var uZoneFaces = [];
		uzone = arr[index];
		$.each(uzone['vertices'], function(index){
			value = uzone['vertices'][index];
			uZoneVert.push({'x': value['x'], 'y': value['y'], 'z': value['zmin']});
			uZoneVertUp.push({'x': value['x'], 'y': value['y'], 'z': value['zmax']});
		});
		$.each(uzone['faces'], function(index){
			value = uzone['faces'][index];
			uZoneFaces.push({'a': value['a'], 'b': value['b'], 'c': value['c']});
		});
		//строим плоскость
		var uzoneGeometry = new THREE.Geometry();
		$.each(uZoneVert, function(index){
			x = uZoneVert[index]['x'];
			y = uZoneVert[index]['y'];
			z = uZoneVert[index]['z'];
			uzoneGeometry.vertices.push(
				new THREE.Vector3(x, y, z + 0.12)
			)
		});
		$.each(uZoneFaces, function(index){
			a = uZoneFaces[index]['a'];
			b = uZoneFaces[index]['b'];
			c = uZoneFaces[index]['c'];
			uzoneGeometry.faces.push(
				new THREE.Face3(a, b, c)
			)
		});
		
		var uzoneGeometryUp = new THREE.Geometry();
		$.each(uZoneVertUp, function(index){
			x = uZoneVertUp[index]['x'];
			y = uZoneVertUp[index]['y'];
			z = uZoneVertUp[index]['z'];
			uzoneGeometryUp.vertices.push(
				new THREE.Vector3(x, y, z + 0.06)
			)
		});
		$.each(uZoneFaces, function(index){
			a = uZoneFaces[index]['a'];
			b = uZoneFaces[index]['b'];
			c = uZoneFaces[index]['c'];
			uzoneGeometryUp.faces.push(
				new THREE.Face3(a, b, c)
			)
		});
		uzoneGeometry.computeBoundingSphere();
		uzoneGeometryUp.computeBoundingSphere();
		var uzoneMaterial = new THREE.MeshBasicMaterial({ color: 0x66cdaa, side: THREE.DoubleSide, transparent: true, opacity:0.3});
		var uzoneMaterialUp = new THREE.MeshBasicMaterial({ color: 0x66cdaa, side: THREE.DoubleSide, transparent: true, opacity:0.3});
		Obj_I_uZone.push({'mesh': new THREE.Mesh(uzoneGeometry, uzoneMaterial)});
		Obj_I_uZoneUp.push({'mesh': new THREE.Mesh(uzoneGeometryUp, uzoneMaterialUp)});
	});
	$.each(Obj_I_uZone, function(index){
		scene.add(Obj_I_uZone[index]['mesh']);
	});
	$.each(Obj_I_uZoneUp, function(index){
		scene.add(Obj_I_uZoneUp[index]['mesh']);
	});
}

//сохраниение минимального значения высоты зоны incomezone
$('#zonetable').delegate('#savemin', 'click', function(){
	elem = $(this).prev('li').children('label').children();
	parameters = {}
	parameters['method'] = 'savemin'
	
	parameters['value'] = parseFloat(elem.val());
	parameters['zoneid'] = elem.attr('data-id');
	parameters['landscape_id'] = landscape_id;
	$.ajax({
		type: "POST",
		url: "/incomezonedefine/"+landscape_id,
		data:JSON.stringify(parameters),
		contentType: "application/json; charset=utf-8",
		dataType: "html",
		async: true,
		success: function(data, textStatus, jqXHR){
			$('#zonetable').html(data);
		}
	});
});
$('#zonetable').delegate('#savemax', 'click', function(){
	elem = $(this).prev().children('input');
	parameters = {}
	parameters['method'] = 'savemax'
	
	parameters['value'] = parseFloat(elem.val());
	parameters['zoneid'] = elem.attr('data-id');
	parameters['landscape_id'] = landscape_id;
	$.ajax({
		type: "POST",
		url: "/incomezonedefine/"+landscape_id,
		data:JSON.stringify(parameters),
		contentType: "application/json; charset=utf-8",
		dataType: "html",
		async: true,
		success: function(data, textStatus, jqXHR){
			$('#zonetable').html(data);
		}
	});
});
//сохраниение минимального значения высоты зоны excludezone
$('#excludezonetable').delegate('#savemin_exclude', 'click', function(){
	elem = $(this).prev('li').children('label').children();
	parameters = {}
	parameters['method'] = 'savemin_exclude'
	parameters['value'] = parseFloat(elem.val());
	parameters['zoneid'] = elem.attr('data-id');
	parameters['landscape_id'] = landscape_id;
	$.ajax({
		type: "POST",
		url: "/incomezonedefine/"+landscape_id,
		data:JSON.stringify(parameters),
		contentType: "application/json; charset=utf-8",
		dataType: "html",
		async: true,
		success: function(data, textStatus, jqXHR){
			$('#excludezonetable').html(data);
		}
	});
});
$('#excludezonetable').delegate('#savemax_exclude', 'click', function(){
	elem = $(this).prev().children('input');
	parameters = {}
	parameters['method'] = 'savemax_exclude'
	
	parameters['value'] = parseFloat(elem.val());
	parameters['zoneid'] = elem.attr('data-id');
	parameters['landscape_id'] = landscape_id;
	$.ajax({
		type: "POST",
		url: "/incomezonedefine/"+landscape_id,
		data:JSON.stringify(parameters),
		contentType: "application/json; charset=utf-8",
		dataType: "html",
		async: true,
		success: function(data, textStatus, jqXHR){
			$('#excludezonetable').html(data);
		}
	});
});
//сохраниение минимального значения высоты зоны userzone
$('#userzonetable').delegate('#savemin_uzone', 'click', function(){
	elem = $(this).prev('li').children('label').children();
	parameters = {}
	parameters['method'] = 'savemin_uzone'
	
	parameters['value'] = parseFloat(elem.val());
	parameters['zoneid'] = elem.attr('data-id');
	parameters['landscape_id'] = landscape_id;
	$.ajax({
		type: "POST",
		url: "/incomezonedefine/"+landscape_id,
		data:JSON.stringify(parameters),
		contentType: "application/json; charset=utf-8",
		dataType: "html",
		async: true,
		success: function(data, textStatus, jqXHR){
			$('#uzerzonetable').html(data);
		}
	});
});
$('#userzonetable').delegate('#savemax_uzone', 'click', function(){
	elem = $(this).prev().children('input');
	parameters = {}
	parameters['method'] = 'savemax_uzone'
	
	parameters['value'] = parseFloat(elem.val());
	parameters['zoneid'] = elem.attr('data-id');
	parameters['landscape_id'] = landscape_id;
	$.ajax({
		type: "POST",
		url: "/incomezonedefine/"+landscape_id,
		data:JSON.stringify(parameters),
		contentType: "application/json; charset=utf-8",
		dataType: "html",
		async: true,
		success: function(data, textStatus, jqXHR){
			$('#userzonetable').html(data);
		}
	});
});
// добавить новую uzonegroup
$('body').delegate('#new_uzonegroup', 'click', function(){
	uzonegroupAddRemove('adduzonegroup', user_id, 0);
});
//удалить uzonegroup
$('body').delegate('#deleteuzonegroup', 'click', function(){
	uid = $(this).attr('data-id');
	uzonegroupAddRemove('deleteuzonegroup', user_id, uid);
});

function uzonegroupAddRemove(type, uname, uid){
	parameters = {};
	parameters['user'] = uname;
	parameters['method'] = type;
	parameters['landscape_id'] = landscape_id;
	if (uid != 0){
		parameters['uid'] = parseInt(uid);
	}
	$.ajax({
		type: "POST",
		url: "/incomezonedefine/"+landscape_id,
		data: JSON.stringify(parameters),
		contentType: "application/json; charset=utf-8",
		dataType: "html",
		async: true,
		success: function(data, textStatus, jqXHR){
			$('#uzonegrouptable').html(data);
		}
	});
}
//привязать или отвязать uzonegroup к uzone
$('body').delegate('#linkuzonetogroup', 'click', function(){
	uzoneid = $(this).attr('data-id');
	groupid = $(this).attr('data-group');
	addremoveuzonefromgroup('adduzonetogroup', uzoneid, groupid);
});

$('body').delegate('#unlinkuzonetogroup', 'click', function(){
	uzoneid = $(this).attr('data-id');
	groupid = $(this).attr('data-group');
	addremoveuzonefromgroup('removeuzonetogroup', uzoneid, groupid);
});
function addremoveuzonefromgroup(type, uzoneid, groupid){
	parameters = {}
	parameters['uzoneid'] = uzoneid;
	parameters['groupid'] = groupid;
	parameters['landscape_id'] = landscape_id;
	parameters['user_id'] = user_id;
	parameters['method'] = type;
	$.ajax({
		type: "POST",
		url: "/incomezonedefine/"+landscape_id,
		data: JSON.stringify(parameters),
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		async: true,
		success: function(data, textStatus, jqXHR){
			$('#uzonegrouptable').html(data['uzonegrouptable']);
			$('#userzonetable').html(data['userzonetable']);
		}
	});
}

//получить вершины объекта x, y. Отдельно минимальное значение z.
var ObjMesh;
var ObjMeshUp;

var Obj_I_Zone = [];
var Obj_I_ZoneUp = [];

var Obj_I_eZone = [];
var Obj_I_eZoneUp = []; 

var Obj_I_uZone = [];
var Obj_I_uZoneUp = [];

function getVertices(dae_elem, object){
	scene.remove(ObjMesh);
	scene.remove(ObjMeshUp);

	//удаляем ранее отображаемые incomezone
	$.each(Obj_I_Zone, function(index){
		scene.remove(Obj_I_Zone[index]['mesh']);
	});
	$.each(Obj_I_ZoneUp, function(index){
		scene.remove(Obj_I_ZoneUp[index]['mesh']);
	});
	Obj_I_Zone = [];
	Obj_I_ZoneUp = [];
	//удаляем ранее отображаемые excludezone
	$.each(Obj_I_eZone, function(index){
		scene.remove(Obj_I_eZone[index]['mesh']);
	});
	$.each(Obj_I_eZoneUp, function(index){
		scene.remove(Obj_I_eZoneUp[index]['mesh']);
	});
	Obj_I_eZone = [];
	Obj_I_eZoneUp = [];
	//удаляем ранее отображаемые userzone
	$.each(Obj_I_uZone, function(index){
		scene.remove(Obj_I_uZone[index]['mesh']);
	});
	$.each(Obj_I_uZoneUp, function(index){
		scene.remove(Obj_I_uZoneUp[index]['mesh']);
	});
	Obj_I_uZone = [];
	Obj_I_uZoneUp = [];

	parameters = {};
	parameters['method'] = 'objvertices';
	parameters['landscape_id'] = landscape_id;
	if (dae_elem.indexOf('building') != -1){
		parameters['type'] = 'building';
		parameters['dae_name'] = dae_elem;
	} else if (dae_elem.indexOf('floor') != -1){
		parameters['type'] = 'floor';
		parameters['dae_name'] = dae_elem;
	} else if (dae_elem.indexOf('kabinet') != -1){
		parameters['type'] = 'kabinet';
		parameters['dae_name'] = dae_elem;
	}
	$.ajax({
		type: "POST", 
		url: "/incomezonedefine/"+landscape_id,
		data: JSON.stringify(parameters),
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		async: true,
		success: function(data, textStatus, jqXHR){
			if (data['type'] == parameters['type']){
				// многоугольник объекта
				scene.remove(ObjMesh);
				scene.remove(ObjMeshUp);
				selObject = data;
				var floorVert = [];
				var floorFaces = [];
				var floorVertUp = [];

				$.each(selObject['vertices'], function(index){
					value = selObject['vertices'][index];
					floorVert.push({'x': value[0], 'y': value[1], 'z': selObject['minz']});
				});

				$.each(selObject['vertices'], function(index){
					value = selObject['vertices'][index];
					floorVertUp.push({'x': value[0], 'y': value[1], 'z': selObject['maxz']});
				});

				$.each(object['geometry']['faces'], function(index){
					value = object['geometry']['faces'][index];
					floorFaces.push({'a': value['a'], 'b': value['b'], 'c': value['c']});
				});

				//строим плоскость
				var planeGeometry = new THREE.Geometry();
				$.each(floorVert, function(index){
					x = floorVert[index]['x'];
					y = floorVert[index]['y'];
					z = floorVert[index]['z'];
					planeGeometry.vertices.push(
						new THREE.Vector3(x, y, z + 0.08)
					)
				});
				$.each(floorFaces, function(index){
					a = floorFaces[index]['a'];
					b = floorFaces[index]['b'];
					c = floorFaces[index]['c'];
					planeGeometry.faces.push(
						new THREE.Face3(a, b, c)
					)
				});
				//cтроим верхнюю плоскость
				var planeGeometryUp = new THREE.Geometry();
				$.each(floorVertUp, function(index){
					x = floorVertUp[index]['x'];
					y = floorVertUp[index]['y'];
					z = floorVertUp[index]['z'];
					planeGeometryUp.vertices.push(
						new THREE.Vector3(x, y, z + 0.02)
					)
				});

				$.each(floorFaces, function(index){
					a = floorFaces[index]['a'];
					b = floorFaces[index]['b'];
					c = floorFaces[index]['c'];
					planeGeometryUp.faces.push(
						new THREE.Face3(a, b, c)
					)
				});

				planeGeometry.computeBoundingSphere();
				planeGeometryUp.computeBoundingSphere();

				var planeMaterial = new THREE.MeshBasicMaterial({ color: 0xffff00, side: THREE.DoubleSide, transparent: true, opacity:0.5});
				var planeMaterialUp = new THREE.MeshBasicMaterial({ color: 0xffff00, side: THREE.DoubleSide, transparent: true, opacity:0.3});
				ObjMesh = new THREE.Mesh(planeGeometry, planeMaterial);
				ObjMeshUp = new THREE.Mesh(planeGeometryUp, planeMaterialUp);
				scene.add(ObjMesh);
				scene.add(ObjMeshUp);
				//многоугольники зон incomezone
				$.each(data['izone'], function(index){
					var iZoneVert = [];
					var iZoneVertUp = [];
					var iZoneFaces = [];
					izone = data['izone'][index];
					$.each(izone['vertices'], function(index){
						value = izone['vertices'][index];
						iZoneVert.push({'x': value['x'], 'y': value['y'], 'z': value['zmin']});
					});
					$.each(izone['vertices'], function(index){
						value = izone['vertices'][index];
						iZoneVertUp.push({'x': value['x'], 'y': value['y'], 'z': value['zmax']});
					});
					$.each(izone['faces'], function(index){
						value = izone['faces'][index];
						iZoneFaces.push({'a': value['a'], 'b': value['b'], 'c': value['c']});
					});
					//строим плоскость
					var izoneGeometry = new THREE.Geometry();
					$.each(iZoneVert, function(index){
						x = iZoneVert[index]['x'];
						y = iZoneVert[index]['y'];
						z = iZoneVert[index]['z'];
						izoneGeometry.vertices.push(
							new THREE.Vector3(x, y, z + 0.10)
						)
					});
					$.each(iZoneFaces, function(index){
						a = iZoneFaces[index]['a'];
						b = iZoneFaces[index]['b'];
						c = iZoneFaces[index]['c'];
						izoneGeometry.faces.push(
							new THREE.Face3(a, b, c)
						)
					});
					var izoneGeometryUp = new THREE.Geometry();
					$.each(iZoneVertUp, function(index){
						x = iZoneVertUp[index]['x'];
						y = iZoneVertUp[index]['y'];
						z = iZoneVertUp[index]['z'];
						izoneGeometryUp.vertices.push(
							new THREE.Vector3(x, y, z + 0.04)
						)
					});
					$.each(iZoneFaces, function(index){
						a = iZoneFaces[index]['a'];
						b = iZoneFaces[index]['b'];
						c = iZoneFaces[index]['c'];
						izoneGeometryUp.faces.push(
							new THREE.Face3(a, b, c)
						)
					});
					izoneGeometry.computeBoundingSphere();
					izoneGeometryUp.computeBoundingSphere();
					var izoneMaterial = new THREE.MeshBasicMaterial({ color: 0xec5840, side: THREE.DoubleSide, transparent: true, opacity:0.5});
					var izoneMaterialUp = new THREE.MeshBasicMaterial({ color: 0xec5840, side: THREE.DoubleSide, transparent: true, opacity:0.3});
					//исключаем повторения
					doubled = 0;
					$.each(Obj_I_Zone, function(index){
						if (Obj_I_Zone[index]['id'] == izone['id']){
							doubled = 1;
						}
					});
					if (doubled==0){
						Obj_I_Zone.push({'mesh': new THREE.Mesh(izoneGeometry, izoneMaterial), 'id':izone['id']});
						Obj_I_ZoneUp.push({'mesh': new THREE.Mesh(izoneGeometryUp, izoneMaterialUp), 'id':izone['id']});
					}
				});

				$.each(Obj_I_Zone, function(index){
					scene.add(Obj_I_Zone[index]['mesh']);
				});
				$.each(Obj_I_ZoneUp, function(index){
					scene.add(Obj_I_ZoneUp[index]['mesh']);
				});
				//многоугольник зон excludezone
				$.each(data['ezone'], function(index){
					var eZoneVert = [];
					var eZoneVertUp = [];
					var eZoneFaces = [];
					ezone = data['ezone'][index];
					$.each(ezone['vertices'], function(index){
						value = ezone['vertices'][index];
						eZoneVert.push({'x': value['x'], 'y': value['y'], 'z': value['zmin']});
					});
					$.each(ezone['vertices'], function(index){
						value = ezone['vertices'][index];
						eZoneVertUp.push({'x': value['x'], 'y': value['y'], 'z': value['zmax']});
					});
					$.each(ezone['faces'], function(index){
						value = ezone['faces'][index];
						eZoneFaces.push({'a': value['a'], 'b': value['b'], 'c': value['c']});
					});
					//строим плоскость
					var ezoneGeometry = new THREE.Geometry();
					$.each(eZoneVert, function(index){
						x = eZoneVert[index]['x'];
						y = eZoneVert[index]['y'];
						z = eZoneVert[index]['z'];
						ezoneGeometry.vertices.push(
							new THREE.Vector3(x, y, z + 0.12)
						)
					});
					$.each(eZoneFaces, function(index){
						a = eZoneFaces[index]['a'];
						b = eZoneFaces[index]['b'];
						c = eZoneFaces[index]['c'];
						ezoneGeometry.faces.push(
							new THREE.Face3(a, b, c)
						)
					});
					var ezoneGeometryUp = new THREE.Geometry();
					$.each(eZoneVertUp, function(index){
						x = eZoneVertUp[index]['x'];
						y = eZoneVertUp[index]['y'];
						z = eZoneVertUp[index]['z'];
						ezoneGeometryUp.vertices.push(
							new THREE.Vector3(x, y, z + 0.06)
						)
					});
					$.each(eZoneFaces, function(index){
						a = eZoneFaces[index]['a'];
						b = eZoneFaces[index]['b'];
						c = eZoneFaces[index]['c'];
						ezoneGeometryUp.faces.push(
							new THREE.Face3(a, b, c)
						)
					});
					ezoneGeometry.computeBoundingSphere();
					ezoneGeometryUp.computeBoundingSphere();
					var ezoneMaterial = new THREE.MeshBasicMaterial({ color: 0x483d8b, side: THREE.DoubleSide, transparent: true, opacity:0.5});
					var ezoneMaterialUp = new THREE.MeshBasicMaterial({ color: 0x483d8b, side: THREE.DoubleSide, transparent: true, opacity:0.3});
					//исключаем повторения
					doubled = 0;
					$.each(Obj_I_eZone, function(index){
						if (Obj_I_eZone[index]['id'] == ezone['id']){
							doubled = 1;
						}
					});
					if (doubled==0){
						Obj_I_eZone.push({'mesh': new THREE.Mesh(ezoneGeometry, ezoneMaterial), 'id':ezone['id']});
						Obj_I_eZoneUp.push({'mesh': new THREE.Mesh(ezoneGeometryUp, ezoneMaterialUp), 'id':ezone['id']});
					}
				});
				$.each(Obj_I_eZone, function(index){
					scene.add(Obj_I_eZone[index]['mesh']);
				});
				$.each(Obj_I_eZoneUp, function(index){
					scene.add(Obj_I_eZoneUp[index]['mesh']);
				});
				//многоугольник зон userzone
				$.each(data['uzone'], function(index){
					var uZoneVert = [];
					var uZoneVertUp = [];
					var uZoneFaces = [];
					uzone = data['uzone'][index];
					$.each(uzone['vertices'], function(index){
						value = uzone['vertices'][index];
						uZoneVert.push({'x': value['x'], 'y': value['y'], 'z': value['zmin']});
					});
					$.each(uzone['vertices'], function(index){
						value = uzone['vertices'][index];
						uZoneVertUp.push({'x': value['x'], 'y': value['y'], 'z': value['zmax']});
					});
					$.each(uzone['faces'], function(index){
						value = uzone['faces'][index];
						uZoneFaces.push({'a': value['a'], 'b': value['b'], 'c': value['c']});
					});
					//строим плоскость
					var uzoneGeometry = new THREE.Geometry();
					$.each(uZoneVert, function(index){
						x = uZoneVert[index]['x'];
						y = uZoneVert[index]['y'];
						z = uZoneVert[index]['z'];
						uzoneGeometry.vertices.push(
							new THREE.Vector3(x, y, z + 0.12)
						)
					});
					$.each(uZoneFaces, function(index){
						a = uZoneFaces[index]['a'];
						b = uZoneFaces[index]['b'];
						c = uZoneFaces[index]['c'];
						uzoneGeometry.faces.push(
							new THREE.Face3(a, b, c)
						)
					});
					var uzoneGeometryUp = new THREE.Geometry();
					$.each(uZoneVertUp, function(index){
						x = uZoneVertUp[index]['x'];
						y = uZoneVertUp[index]['y'];
						z = uZoneVertUp[index]['z'];
						uzoneGeometryUp.vertices.push(
							new THREE.Vector3(x, y, z + 0.06)
						)
					});
					$.each(uZoneFaces, function(index){
						a = uZoneFaces[index]['a'];
						b = uZoneFaces[index]['b'];
						c = uZoneFaces[index]['c'];
						uzoneGeometryUp.faces.push(
							new THREE.Face3(a, b, c)
						)
					});
					uzoneGeometry.computeBoundingSphere();
					uzoneGeometryUp.computeBoundingSphere();
					var uzoneMaterial = new THREE.MeshBasicMaterial({ color: 0x87cefa, side: THREE.DoubleSide, transparent: true, opacity:0.5});
					var uzoneMaterialUp = new THREE.MeshBasicMaterial({ color: 0x87cefa, side: THREE.DoubleSide, transparent: true, opacity:0.3});
					//исключаем повторения
					doubled = 0;
					$.each(Obj_I_uZone, function(index){
						if (Obj_I_uZone[index]['id'] == uzone['id']){
							doubled = 1;
						}
					});
					if (doubled==0){
						Obj_I_uZone.push({'mesh': new THREE.Mesh(uzoneGeometry, uzoneMaterial), 'id':uzone['id']});
						Obj_I_uZoneUp.push({'mesh': new THREE.Mesh(uzoneGeometryUp, uzoneMaterialUp), 'id':uzone['id']});
					}
				});
				$.each(Obj_I_uZone, function(index){
					scene.add(Obj_I_uZone[index]['mesh']);
				});
				$.each(Obj_I_uZoneUp, function(index){
					scene.add(Obj_I_uZoneUp[index]['mesh']);
				});
			}
		}
	});
}

//показать зону incomezone
$('body').delegate('#show', 'click', function(){
	$.each(Obj_I_Zone, function(index){
		scene.remove(Obj_I_Zone[index]['mesh']);
	});
	$.each(Obj_I_ZoneUp, function(index){
		scene.remove(Obj_I_ZoneUp[index]['mesh']);
	});
	parameters = {};
	parameters['method'] = 'show';
	parameters['landscape_id'] = landscape_id;
	parameters['zoneid'] = parseInt($(this).attr('data-id'));
	$.ajax({
		type: "POST",
		url: "/incomezonedefine/"+landscape_id,
		data:JSON.stringify(parameters),
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		async: true,
		success: function(data, textStatus, jqXHR){
			showIncomeZones([data['izone'][0]]);
		}
	});
});

function showIncomeZones(arr){
	$.each(Obj_I_Zone, function(index){
		scene.remove(Obj_I_Zone[index]['mesh']);
	});
	$.each(Obj_I_ZoneUp, function(index){
		scene.remove(Obj_I_ZoneUp[index]['mesh']);
	});
	Obj_I_Zone = [];
	Obj_I_ZoneUp = [];
	$.each(arr, function(index){
		var iZoneVert = [];
		var iZoneVertUp = [];
		var iZoneFaces = [];
		izone = arr[index];
		$.each(izone['vertices'], function(index){
			value = izone['vertices'][index];
			iZoneVert.push({'x': value['x'], 'y': value['y'], 'z': value['zmin']});
			iZoneVertUp.push({'x': value['x'], 'y': value['y'], 'z': value['zmax']});
		});
		$.each(izone['faces'], function(index){
			value = izone['faces'][index];
			iZoneFaces.push({'a': value['a'], 'b': value['b'], 'c': value['c']});
		});
		//строим плоскость
		var izoneGeometry = new THREE.Geometry();
		$.each(iZoneVert, function(index){
			x = iZoneVert[index]['x'];
			y = iZoneVert[index]['y'];
			z = iZoneVert[index]['z'];
			izoneGeometry.vertices.push(
				new THREE.Vector3(x, y, z + 0.12)
			)
		});
		$.each(iZoneFaces, function(index){
			a = iZoneFaces[index]['a'];
			b = iZoneFaces[index]['b'];
			c = iZoneFaces[index]['c'];
			izoneGeometry.faces.push(
				new THREE.Face3(a, b, c)
			)
		});
		
		var izoneGeometryUp = new THREE.Geometry();
		$.each(iZoneVertUp, function(index){
			x = iZoneVertUp[index]['x'];
			y = iZoneVertUp[index]['y'];
			z = iZoneVertUp[index]['z'];
			izoneGeometryUp.vertices.push(
				new THREE.Vector3(x, y, z + 0.06)
			)
		});
		$.each(iZoneFaces, function(index){
			a = iZoneFaces[index]['a'];
			b = iZoneFaces[index]['b'];
			c = iZoneFaces[index]['c'];
			izoneGeometryUp.faces.push(
				new THREE.Face3(a, b, c)
			)
		});
		izoneGeometry.computeBoundingSphere();
		izoneGeometryUp.computeBoundingSphere();
		var izoneMaterial = new THREE.MeshBasicMaterial({ color: 0xdc143c, side: THREE.DoubleSide, transparent: true, opacity:0.3});
		var izoneMaterialUp = new THREE.MeshBasicMaterial({ color: 0xdc143c, side: THREE.DoubleSide, transparent: true, opacity:0.3});
		Obj_I_Zone.push({'mesh': new THREE.Mesh(izoneGeometry, izoneMaterial)});
		Obj_I_ZoneUp.push({'mesh': new THREE.Mesh(izoneGeometryUp, izoneMaterialUp)});
	});
	$.each(Obj_I_Zone, function(index){
		scene.add(Obj_I_Zone[index]['mesh']);
	});
	$.each(Obj_I_ZoneUp, function(index){
		scene.add(Obj_I_ZoneUp[index]['mesh']);
	});
}

function showExcludeZones(arr){
	$.each(Obj_I_eZone, function(index){
		scene.remove(Obj_I_eZone[index]['mesh']);
	});
	$.each(Obj_I_eZoneUp, function(index){
		scene.remove(Obj_I_eZoneUp[index]['mesh']);
	});
	Obj_I_eZone = [];
	Obj_I_eZoneUp = [];
	$.each(arr, function(index){
		var eZoneVert = [];
		var eZoneVertUp = [];
		var eZoneFaces = [];
		ezone = arr[index];
		$.each(ezone['vertices'], function(index){
			value = ezone['vertices'][index];
			eZoneVert.push({'x': value['x'], 'y': value['y'], 'z': value['zmin']});
			eZoneVertUp.push({'x': value['x'], 'y': value['y'], 'z': value['zmax']});
		});
		$.each(ezone['faces'], function(index){
			value = ezone['faces'][index];
			eZoneFaces.push({'a': value['a'], 'b': value['b'], 'c': value['c']});
		});
		//строим плоскость
		var ezoneGeometry = new THREE.Geometry();
		$.each(eZoneVert, function(index){
			x = eZoneVert[index]['x'];
			y = eZoneVert[index]['y'];
			z = eZoneVert[index]['z'];
			ezoneGeometry.vertices.push(
				new THREE.Vector3(x, y, z + 0.12)
			)
		});
		$.each(eZoneFaces, function(index){
			a = eZoneFaces[index]['a'];
			b = eZoneFaces[index]['b'];
			c = eZoneFaces[index]['c'];
			ezoneGeometry.faces.push(
				new THREE.Face3(a, b, c)
			)
		});
		
		var ezoneGeometryUp = new THREE.Geometry();
		$.each(eZoneVertUp, function(index){
			x = eZoneVertUp[index]['x'];
			y = eZoneVertUp[index]['y'];
			z = eZoneVertUp[index]['z'];
			ezoneGeometryUp.vertices.push(
				new THREE.Vector3(x, y, z + 0.06)
			)
		});
		$.each(eZoneFaces, function(index){
			a = eZoneFaces[index]['a'];
			b = eZoneFaces[index]['b'];
			c = eZoneFaces[index]['c'];
			ezoneGeometryUp.faces.push(
				new THREE.Face3(a, b, c)
			)
		});
		ezoneGeometry.computeBoundingSphere();
		ezoneGeometryUp.computeBoundingSphere();
		var ezoneMaterial = new THREE.MeshBasicMaterial({ color: 0x4b0082, side: THREE.DoubleSide, transparent: true, opacity:0.3});
		var ezoneMaterialUp = new THREE.MeshBasicMaterial({ color: 0x4b0082, side: THREE.DoubleSide, transparent: true, opacity:0.3});
		Obj_I_eZone.push({'mesh': new THREE.Mesh(ezoneGeometry, ezoneMaterial)});
		Obj_I_eZoneUp.push({'mesh': new THREE.Mesh(ezoneGeometryUp, ezoneMaterialUp)});
	});
	$.each(Obj_I_eZone, function(index){
		scene.add(Obj_I_eZone[index]['mesh']);
	});
	$.each(Obj_I_eZoneUp, function(index){
		scene.add(Obj_I_eZoneUp[index]['mesh']);
	});
}
//показать зону excludezone
$('body').delegate('#show_exclude', 'click', function(){
	$.each(Obj_I_eZone, function(index){
		scene.remove(Obj_I_eZone[index]['mesh']);
	});
	$.each(Obj_I_eZoneUp, function(index){
		scene.remove(Obj_I_eZoneUp[index]['mesh']);
	});
	parameters = {};
	parameters['method'] = 'show_exclude';
	parameters['landscape_id'] = landscape_id;
	parameters['zoneid'] = parseInt($(this).attr('data-id'));
	$.ajax({
		type: "POST",
		url: "/incomezonedefine/"+landscape_id,
		data:JSON.stringify(parameters),
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		async: true,
		success: function(data, textStatus, jqXHR){
			Obj_I_eZone = [];
			Obj_I_eZoneUp = [];
			var eZoneVert = [];
			var eZoneVertUp = [];
			var eZoneFaces = [];
			ezone = data['ezone'][0];
			$.each(ezone['vertices'], function(index){
				value = ezone['vertices'][index];
				eZoneVert.push({'x': value['x'], 'y': value['y'], 'z': value['zmin']});
				eZoneVertUp.push({'x': value['x'], 'y': value['y'], 'z': value['zmax']});
			});
			$.each(ezone['faces'], function(index){
				value = ezone['faces'][index];
				eZoneFaces.push({'a': value['a'], 'b': value['b'], 'c': value['c']});
			});
			//строим плоскость
			var ezoneGeometry = new THREE.Geometry();
			$.each(eZoneVert, function(index){
				x = eZoneVert[index]['x'];
				y = eZoneVert[index]['y'];
				z = eZoneVert[index]['z'];
				ezoneGeometry.vertices.push(
					new THREE.Vector3(x, y, z + 0.12)
				)
			});
			$.each(eZoneFaces, function(index){
				a = eZoneFaces[index]['a'];
				b = eZoneFaces[index]['b'];
				c = eZoneFaces[index]['c'];
				ezoneGeometry.faces.push(
					new THREE.Face3(a, b, c)
				)
			});
			
			var ezoneGeometryUp = new THREE.Geometry();
			$.each(eZoneVertUp, function(index){
				x = eZoneVertUp[index]['x'];
				y = eZoneVertUp[index]['y'];
				z = eZoneVertUp[index]['z'];
				ezoneGeometryUp.vertices.push(
					new THREE.Vector3(x, y, z + 0.06)
				)
			});
			$.each(eZoneFaces, function(index){
				a = eZoneFaces[index]['a'];
				b = eZoneFaces[index]['b'];
				c = eZoneFaces[index]['c'];
				ezoneGeometryUp.faces.push(
					new THREE.Face3(a, b, c)
				)
			});
			ezoneGeometry.computeBoundingSphere();
			ezoneGeometryUp.computeBoundingSphere();
			var ezoneMaterial = new THREE.MeshBasicMaterial({ color: 0x4b0082, side: THREE.DoubleSide, transparent: false, opacity:0.5});
			var ezoneMaterialUp = new THREE.MeshBasicMaterial({ color: 0x4b0082, side: THREE.DoubleSide, transparent: false, opacity:0.3});
			//исключаем повторения
			doubled = 0;
			$.each(Obj_I_eZone, function(index){
				if (Obj_I_eZone[index]['id'] == ezone['id']){
					doubled = 1;
				}
			});
			if (doubled==0){
				Obj_I_eZone.push({'mesh': new THREE.Mesh(ezoneGeometry, ezoneMaterial), 'id':ezone['id']});
				Obj_I_eZoneUp.push({'mesh': new THREE.Mesh(ezoneGeometryUp, ezoneMaterialUp), 'id':ezone['id']});
			}
			$.each(Obj_I_eZone, function(index){
				scene.add(Obj_I_eZone[index]['mesh']);
			});
			$.each(Obj_I_eZoneUp, function(index){
				scene.add(Obj_I_eZoneUp[index]['mesh']);
			});
		}
	});
});

//показать зону userzone
$('body').delegate('#show_uzone', 'click', function(){
	$.each(Obj_I_uZone, function(index){
		scene.remove(Obj_I_uZone[index]['mesh']);
	});
	$.each(Obj_I_uZoneUp, function(index){
		scene.remove(Obj_I_uZoneUp[index]['mesh']);
	});
	$.each(Obj_I_eZone, function(index){
		scene.remove(Obj_I_eZone[index]['mesh']);
	});
	$.each(Obj_I_eZoneUp, function(index){
		scene.remove(Obj_I_eZoneUp[index]['mesh']);
	});
	parameters = {};
	parameters['method'] = 'show_uzone';
	parameters['landscape_id'] = landscape_id;
	parameters['zoneid'] = parseInt($(this).attr('data-id'));
	$.ajax({
		type: "POST",
		url: "/incomezonedefine/"+landscape_id,
		data:JSON.stringify(parameters),
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		async: true,
		success: function(data, textStatus, jqXHR){
			showZonesOfGroup([data['uzone'][0]]);
			showIncomeZones(data['uzone'][0]['izones']);
			showExcludeZones(data['uzone'][0]['ezones']);
		}
	});
});