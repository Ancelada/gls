$(function(){
	/*global variables*/
    var axis;
    var grid,color;
    var scene, camera, renderer;
    var controls, gui;
    var stats;
    var spotLight, hemi;
    var SCREEN_WIDTH, SCREEN_HEIGHT;

    function init(){
        /*creates empty scene object and renderer*/
        scene = new THREE.Scene();
        camera =  new THREE.PerspectiveCamera(85, window.innerWidth/window.innerHeight, .1, 1000);
        renderer = new THREE.WebGLRenderer({antialias:true});
        
        /*renderer.setClearColor(0x66c0cf);*/
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.shadowMapEnabled= true;
        renderer.shadowMapSoft = true;
        
        /* add axis helper*/
        axis = new THREE.AxisHelper(30);
        scene.add(axis);

        grid = new THREE.GridHelper(100, 25);
        color = new THREE.Color("rgb(255, 0, 0)");
        grid.setColors(color, 0x000000);
        grid.rotation.x = -0.5* Math.PI
        scene.add(grid);
        
        //skyshader
        var vertexShader = document.getElementById( 'vertexShader' ).textContent;
        var fragmentShader = document.getElementById( 'fragmentShader' ).textContent;
        var uniforms = {
            topColor:      { type: "c", value: new THREE.Color(0x000000) },
            bottomColor: { type: "c", value: new THREE.Color( 0x262626 ) },
            offset:         { type: "f", value: 100 },
            exponent:     { type: "f", value: 0.7 }
        }

        //skydome

        var skyGeo = new THREE.SphereGeometry( 300, 32, 15 );
        var skyMat = new THREE.ShaderMaterial( { vertexShader: vertexShader, fragmentShader: fragmentShader, uniforms: uniforms, side: THREE.BackSide } );

        var sky = new THREE.Mesh( skyGeo, skyMat );
        scene.add( sky );




        /*adds spot light with starting parameters*/
        spotLight = new THREE.SpotLight(0xffffff);
        spotLight.castShadow = true;
        spotLight.position.set (20, 35, 40);
        scene.add(spotLight);
        

        /* add collada import */
        var loader = new THREE.ColladaLoader();
        /*loader.options.convertUpAxis = true;*/
        loader.load( 'static/js/webgl/models/dummy1.dae', function ( collada ) {
        //dummy1.dae
        var dae = collada.scene;
        var skin = collada.skins[ 0 ];
        dae.position.set(0,0,0);//x,z,y- if you think in blender dimensions ;)
        dae.scale.set(1.5,1.5,1.5);
        scene.add(dae);
        });

        /* add parent mesh */
        var cubeGeom = new THREE.BoxGeometry(20, 20, 20, 2, 2, 2);
        var cubeMaterial = new THREE.MeshLambertMaterial({color: 0x0000ff, transparent: true, opacity:0.5});
		this.cube = new THREE.Mesh(cubeGeom, cubeMaterial);
		cube.position.set(0,0,0);
		scene.add(cube);


		/* add children mesh */
		var cylinder_geometry = new THREE.CylinderGeometry(10, 10, 15);
		var cylinder_material = new THREE.MeshNormalMaterial();
		this.cylinder = new THREE.Mesh(cylinder_geometry, cylinder_material);
		cylinder.position = cube.position;
		scene.add(cylinder);

		/* put child inside parent*/
		cube.add(cylinder);
		cube.updateMatrixWorld();

		/* set default camera position */
        camera.position.set(0, -20, 0);
        /* set up direction to axis Z*/
        camera.up.set( 0, 0, 1 );
        /* set camera as child to cube */
        cube.add(camera);
        console.log(camera);

        /*add controls*/
        controls = new THREE.OrbitControls( camera, renderer.domElement );
        controls.addEventListener( 'change', render );

        hemi = new THREE.HemisphereLight(0xbbbbbb, 0x0099FF);
        scene.add(hemi);


        $("#webGL-container").append(renderer.domElement);
        /*stats*/
        stats = new Stats();        
        stats.domElement.style.position = 'absolute';
        stats.domElement.style.left = '0px';
        stats.domElement.style.top = '0px';     
        $("#webGL-container").append( stats.domElement );       
    }

    function render(){
    }

    function update(){
    }

    function animate(){
    	cube.rotation.z += .01;
        requestAnimationFrame(animate);
        render();
        update();
        stats.update();     
        renderer.render(scene, camera);
    }

    init();
    animate();


    $(window).resize(function(){
        SCREEN_WIDTH = window.innerWidth;
        SCREEN_HEIGHT = window.innerHeight;
        camera.aspect = SCREEN_WIDTH / SCREEN_HEIGHT;
        camera.updateProjectionMatrix();
        renderer.setSize( SCREEN_WIDTH, SCREEN_HEIGHT );
    });
});