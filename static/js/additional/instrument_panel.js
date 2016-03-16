//**********************************************
// панель инструментов
//**********************************************

$('body').delegate('.show_hide_button', 'click', function(){
	$('.instrument_block').css('right', 0);
});

$('body').delegate('.close_panel', 'click', function(){
	$('.instrument_block').css('right', '-100%');
});

$('.income_zone_button').on('click', function(){
	$('.incomezone_panel').css('right', 0);
});

$('.close_incomezone_panel').on('click', function(){
	$('.incomezone_panel').css('right', '-100%');
});
//записать вершины
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
//удалить зону
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

//прицепить к объекту
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
//отйцепить от объекта
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
//отметка привязанных зон в таблице
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

//сохраниение минимального значения высоты зоны
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
//получить вершины объекта x, y. Отдельно минимальное значение z.
var ObjMesh;
var ObjMeshUp;

var Obj_I_Zone = [];
var Obj_I_ZoneUp = [];


function getVertices(dae_elem, object){
	scene.remove(ObjMesh);
	scene.remove(ObjMeshUp);

	$.each(Obj_I_Zone, function(index){
		scene.remove(Obj_I_Zone[index]['mesh']);
	});
	$.each(Obj_I_ZoneUp, function(index){
		scene.remove(Obj_I_ZoneUp[index]['mesh']);
	});
	Obj_I_Zone = [];
	Obj_I_ZoneUp = [];

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
				//многоугольники зон
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
			}
			console.log(Obj_I_Zone);
		}
	});
}

//показать зону
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
			console.log(izoneGeometry);
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