//**********************************************
// панель инструментов
//**********************************************

$('body').delegate('.show_hide_button', 'click', function(){
	$('.instrument_block').css('right', 0);
});

$('body').delegate('.close_panel', 'click', function(){
	$('.instrument_block').css('right', '-100%');
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
        $(this).addClass('secondary')
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
//прицепить к объекту includezone
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

//сохраниение минимального значения высоты зоны incomezone
$('#zonetable').delegate('#savemin', 'click', function(){
	elem = $(this).prev('li').children('label').children();
	parameters = {}
	parameters['method'] = 'savemin'
	
	parameters['value'] = parseFloat(elem.val());
	parameters['zoneid'] = elem.attr('data-id');
	parameters['landscape_id'] = landscape_id;
	if (elem.val()>0){
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
	} 
});
$('#zonetable').delegate('#savemax', 'click', function(){
	elem = $(this).prev().children('input');
	parameters = {}
	parameters['method'] = 'savemax'
	
	parameters['value'] = parseFloat(elem.val());
	parameters['zoneid'] = elem.attr('data-id');
	parameters['landscape_id'] = landscape_id;
	if (elem.val()>0){
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
	} 
});
//сохраниение минимального значения высоты зоны excludezone
$('#excludezonetable').delegate('#savemin_exclude', 'click', function(){
	elem = $(this).prev('li').children('label').children();
	parameters = {}
	parameters['method'] = 'savemin_exclude'
	
	parameters['value'] = parseFloat(elem.val());
	parameters['zoneid'] = elem.attr('data-id');
	parameters['landscape_id'] = landscape_id;
	if (elem.val()>0){
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
	} 
});
$('#excludezonetable').delegate('#savemax_exclude', 'click', function(){
	elem = $(this).prev().children('input');
	parameters = {}
	parameters['method'] = 'savemax_exclude'
	
	parameters['value'] = parseFloat(elem.val());
	parameters['zoneid'] = elem.attr('data-id');
	parameters['landscape_id'] = landscape_id;
	if (elem.val()>0){
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
	} 
});

//получить вершины объекта x, y. Отдельно минимальное значение z.
var ObjMesh;
var ObjMeshUp;

var Obj_I_Zone = [];
var Obj_I_ZoneUp = [];

var Obj_I_eZone = [];
var Obj_I_eZoneUp = []; 


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
			Obj_I_Zone = [];
			Obj_I_ZoneUp = [];
			var iZoneVert = [];
			var iZoneVertUp = [];
			var iZoneFaces = [];
			izone = data['izone'][0];
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
			var izoneMaterial = new THREE.MeshBasicMaterial({ color: 0xdc143c, side: THREE.DoubleSide, transparent: false, opacity:0.5});
			var izoneMaterialUp = new THREE.MeshBasicMaterial({ color: 0xdc143c, side: THREE.DoubleSide, transparent: false, opacity:0.3});
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
			$.each(Obj_I_Zone, function(index){
				scene.add(Obj_I_Zone[index]['mesh']);
			});
			$.each(Obj_I_ZoneUp, function(index){
				scene.add(Obj_I_ZoneUp[index]['mesh']);
			});
		}
	});
});

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