$(function(){

    /*global variables*/
    var axis;
    var grid,color;
    var scene, camera, renderer;
    var controls, gui;
    var stats;
    var spotLight, hemi;
    var SCREEN_WIDTH, SCREEN_HEIGHT;
    var loader, model, ballmodel, ballglowmodel;



    /* change shere position  */
    var xNew, yNew, zNew;
    var xCur, yCur, zCur;

    $('#move').on('click', function(){
        xNew = 15;
        yNew = 15;
        zNew = 15;
        xCur = ballmodel.position.x;
        yCur = ballmodel.position.y;
        zCur = ballmodel.position.z;
    });

    $('#back').on('click', function(){
        xNew = 0;
        yNew = 0;
        zNew = 0;
        xCur = ballmodel.position.x;
        yCur = ballmodel.position.y;
        zCur = ballmodel.position.z;
    });

    $('#random').on('click', function(){
        xNew = parseInt((Math.random()*(-15 - 30)+30).toFixed(4));
        yNew = parseInt((Math.random()*(-15 - 30)+30).toFixed(4));
        zNew = parseInt((Math.random()*(-15 - 30)+30).toFixed(4));
        xCur = ballmodel.position.x;
        yCur = ballmodel.position.y;
        zCur = ballmodel.position.z;
    });
    


    function init(){
        /*creates empty scene object and renderer*/
        scene = new THREE.Scene();
        camera =  new THREE.PerspectiveCamera(85, window.innerWidth/window.innerHeight, .1, 1000);
        renderer = new THREE.WebGLRenderer({antialias:true});
        
        renderer.setClearColor(0x66c0cf);
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.shadowMapEnabled= true;
        renderer.shadowMapSoft = true;
        
        /* add axis helper*/
        axis = new THREE.AxisHelper(30);
        scene.add(axis);

        grid = new THREE.GridHelper(200, 25);
        color = new THREE.Color("rgb(255, 0, 0)");
        grid.setColors(color, 0x000000);
        grid.rotation.x = -0.5* Math.PI
        scene.add(grid);

        /*add controls*/
        controls = new THREE.OrbitControls( camera, renderer.domElement );
        controls.addEventListener( 'change', render );
                    
        camera.position.set(0, -50, 40);
        camera.lookAt(scene.position);

        hemi = new THREE.HemisphereLight(0xbbbbbb, 0x0099FF);
        scene.add(hemi);
        
        /*adds spot light with starting parameters*/
        spotLight = new THREE.SpotLight(0xffffff);
        spotLight.castShadow = true;
        spotLight.position.set (20, 35, 40);
        scene.add(spotLight);
        
        /*add loader call add model function*/
        loader = new THREE.JSONLoader();
        loader.load( '/static/js/webgl/models/floor.json', floor );
   
        ball();
        ballglow();
        /*adds controls to scene*/
        gui = new dat.GUI();
        parameters = 
        { c: 1.0, p: 1.4, bs: false, fs: true, nb: false, ab: true, mv: true, color: "#ffff00" };
    
        var top = gui.addFolder('Glow Shader Attributes');
        
        var cGUI = top.add( parameters, 'c' ).min(0.0).max(1.0).step(0.01).name("c").listen();
        cGUI.onChange( function(value) { 
            ballglowmodel.material.uniforms[ "c" ].value = parameters.c; 
        });
        
        var pGUI = top.add( parameters, 'p' ).min(0.0).max(6.0).step(0.01).name("p").listen();
        pGUI.onChange( function(value) { 
            ballglowmodel.material.uniforms[ "p" ].value = parameters.p; 
        });

        var glowColor = top.addColor( parameters, 'color' ).name('Glow Color').listen();
        glowColor.onChange( function(value) {
            ballglowmodel.material.uniforms.glowColor.value.setHex( value.replace("#", "0x"));   
        });
        top.open();
        
        // toggle front side / back side 
        var folder1 = gui.addFolder('Render side');
        var fsGUI = folder1.add( parameters, 'fs' ).name("THREE.FrontSide").listen();
        fsGUI.onChange( function(value) { 
            if (value) 
            {
                bsGUI.setValue(false);
                ballglowmodel.material.side = THREE.FrontSide;  
            }
        });
        var bsGUI = folder1.add( parameters, 'bs' ).name("THREE.BackSide").listen();
        bsGUI.onChange( function(value) { 
            if (value)
            {
                fsGUI.setValue(false);
                ballglowmodel.material.side = THREE.BackSide;  
            }
        });
        folder1.open();
        
        // toggle normal blending / additive blending
        var folder2 = gui.addFolder('Blending style');
        var nbGUI = folder2.add( parameters, 'nb' ).name("THREE.NormalBlending").listen();
        nbGUI.onChange( function(value) { 
            if (value) 
            {
                abGUI.setValue(false);
                ballglowmodel.material.blending = THREE.NormalBlending;  
            }
        });
        var abGUI = folder2.add( parameters, 'ab' ).name("THREE.AdditiveBlending").listen();
        abGUI.onChange( function(value) { 
            if (value)
            {
                nbGUI.setValue(false);
                ballglowmodel.material.blending = THREE.AdditiveBlending; 
            }
        });
        folder2.open();

        // toggle mesh visibility
        var folder3 = gui.addFolder('Miscellaneous');
        var mvGUI = folder3.add( parameters, 'mv' ).name("Meshes-Visible").listen();
        mvGUI.onChange( function(value) { 
            ballmodel.visible = value; 
        });
        folder3.open();
        gui.close();

        $("#webGL-container").append(renderer.domElement);
        /*stats*/
        stats = new Stats();        
        stats.domElement.style.position = 'absolute';
        stats.domElement.style.left = '0px';
        stats.domElement.style.top = '0px';     
        $("#webGL-container").append( stats.domElement );       
    }

    function floor( geometry,  materials ){
        var material = new THREE.MeshLambertMaterial({color: 0x0000ff, transparent: true, opacity:0.5});
        model = new THREE.Mesh( geometry, material );
        model.scale.set (10,10,10);
        model.position.set (0,0,0);
        /*scene.add( model );*/            
    }
    
    function ball( geometry,  materials ){
        var shaderProp = {
            uniforms: {
                color_dark : {
                    type: "v4",
                    value: new THREE.Vector4(1.0, 1.0, 0.0, 1.0)
                },
            },
            vertexShader: document.getElementById("vs0").textContent,
            fragmentShader: document.getElementById("fs0").textContent
        }
        var shaderMat = new THREE.ShaderMaterial(shaderProp);
        var ballGeometry = new THREE.SphereGeometry(10, 32, 16);

        ballmodel = new THREE.Mesh( ballGeometry, shaderMat);
        ballmodel.position.set (0,0,0);
        scene.add( ballmodel );
    }

    function ballglow(){
        var shaderProp = {
            uniforms: {
                "c": {type: "f", value: 0.3},
                "p": {type: "f", value: 3.8},
                glowColor: {type: "c", value: new THREE.Color(0xffff00)},
                viewVector: {type: "v3", value: camera.position}
            },
            vertexShader: document.getElementById("glowVertexShader").textContent,
            fragmentShader: document.getElementById("glowFragmentShader").textContent,
            side: THREE.BackSide,
            blending: THREE.AdditiveBlending,
            transparent: true
        };
        var shaderMat = new THREE.ShaderMaterial(shaderProp);
        var ballGlowGeometry = new THREE.SphereGeometry(13,32,16)
        ballglowmodel = new THREE.Mesh(ballGlowGeometry, shaderMat);
        ballglowmodel.position.set(0,0,0);
        ballglowmodel.scale.multiplyScalar(1, 2);
        scene.add(ballglowmodel);
    }


    function render() {

        var xCur, yCur, zCur;
        xCur = ballmodel.position.x;
        yCur = ballmodel.position.y;
        zCur = ballmodel.position.z;
        var step = 0.9;
        if((xCur < xNew + step) && ((xNew - xCur) > 0)){
            ballmodel.position.x += step;
            ballglowmodel.position.x +=step;
        }

        if((yCur < yNew + step) && ((yNew - yCur) > 0)){
            ballmodel.position.y += step;
            ballglowmodel.position.y +=step;
        }

        if((zCur < zNew + step) && ((zNew - zCur) > 0)){
            ballmodel.position.z += step;
            ballglowmodel.position.z +=step;
        }


        if((xCur > xNew + step) && ((xNew - xCur) < 0)){
            ballmodel.position.x -= step;
            ballglowmodel.position.x -=step;
        }

        if((yCur > yNew + step) && ((yNew - yCur) < 0)){
            ballmodel.position.y -= step;
            ballglowmodel.position.y -=step;
        }

        if((zCur > zNew + step) && ((zNew - zCur) < 0)){
            ballmodel.position.z -= step;
            ballglowmodel.position.z -=step;
        }
        /*ballmodel.position.x = 15+( 10*(Math.cos(step)));
        ballmodel.position.y = 15 +( 10*Math.abs(Math.sin(step)));
        ballmodel.position.z = 15+( 10*(Math.cos(step)));

        ballglowmodel.position.x = 15+( 10*(Math.cos(step)));
        ballglowmodel.position.y = 15 +( 10*Math.abs(Math.sin(step)));
        ballglowmodel.position.z = 15+( 10*(Math.cos(step)));*/
    }

    function update(){
        if (ballglowmodel){
            ballglowmodel.material.uniforms.viewVector.value = new THREE.Vector3().subVectors(camera.position, ballglowmodel.position);
        }
    }

    function animate(){
        if (ballmodel) {
            ballmodel.rotation.y += .1;    
        }
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