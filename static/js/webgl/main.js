$(document).ready(function(){
    
    function parseString(){
        /* разбор данных */
        var csrf_token = $("input[name='csrfmiddlewaretoken']").val();
        $.ajax({
            type: 'POST',
            url: '/save_slmp',
            data: {'csrfmiddlewaretoken': csrf_token},
            dataType: 'html',
            success: function(data, textStatus, jqXHR){
                console.log(data)
            },
        });
    }

    setInterval(parseString, 10000);    
});

$(function(){
    var marks;
    var cube, cubeGeometry, cubeMaterial;
    var scene, camera, renderer;
    var controls, guiControls, datGUI;
    var axis, grid, color;
    var planeGeometry;
    var planeMaterial;
    var cube, plane;
    var spotLight;
    var stats;
    var SCREEN_WIDTH, SCREEN_HEIGHT;
    
    cube = [];

    function init(xpar, ypar, zpar){    
        /*creates empty scene object and renderer*/
        scene = new THREE.Scene();
        camera =  new THREE.PerspectiveCamera(45, window.innerWidth/window.innerHeight, .1, 500);
        renderer = new THREE.WebGLRenderer({antialias:true});
        
        renderer.setClearColor(0xdddddd);
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.shadowMapEnabled= true;
        renderer.shadowMapSoft = true;
        
        /*add controls*/
        controls = new THREE.OrbitControls( camera, renderer.domElement );
        
        /*adds helpers*/
        axis =  new THREE.AxisHelper(10);
        scene.add (axis);
        
        grid = new THREE.GridHelper(100, 10);
        grid.rotation.x = -0.5* Math.PI
        color = new THREE.Color("rgb(255,0,0)");
        grid.setColors(color, 0x000000);
        
        scene.add(grid);
        
        

        /*create plane*/    
        planeGeometry = new THREE.PlaneGeometry (200,200,200);
        planeMaterial = new THREE.MeshLambertMaterial({color:0xffffff});
        plane = new THREE.Mesh(planeGeometry, planeMaterial);
        
        /*position and add objects to scene*/
        plane.receiveShadow = true; 
        scene.add(plane);
        
        
            
        camera.position.set(0, -50, 40);
        camera.rotation.y = -1*Math.PI;
        camera.lookAt(scene.position);
        
        /*datGUI controls object*/
        guiControls = new function(){
            this.rotationX  = 0.0;
            this.rotationY  = 0.0;
            this.rotationZ  = 0.0;
            
            this.lightX = 20;
            this.lightY = 35;
            this.lightZ = 40;
            this.intensity = 1;     
            this.distance = 0;
            this.angle = 1.570;
            this.exponent = 0;
            this.shadowCameraNear = 10;
            this.shadowCameraFar = 100;
            this.shadowCameraFov = 50;
            this.shadowCameraVisible=true;
            this.shadowMapWidth=1028;
            this.shadowMapHeight=1028;
            this.shadowBias=0;
            this.shadowDarkness=0.5;        
            this.target = cube;

        }
        /*adds spot light with starting parameters*/
        spotLight = new THREE.SpotLight(0xffffff);
        spotLight.castShadow = true;
        spotLight.position.set (20, 35, 80);
        spotLight.intensity = guiControls.intensity;        
        spotLight.distance = guiControls.distance;
        spotLight.angle = guiControls.angle;
        spotLight.exponent = guiControls.exponent;
        spotLight.shadowCameraNear = guiControls.shadowCameraNear;
        spotLight.shadowCameraFar = guiControls.shadowCameraFar;
        spotLight.shadowCameraFov = guiControls.shadowCameraFov;
        spotLight.shadowCameraVisible = guiControls.shadowCameraVisible;
        spotLight.shadowBias = guiControls.shadowBias;
        spotLight.shadowDarkness = guiControls.shadowDarkness;
        scene.add(spotLight);

        /*adds controls to scene*/
        $("#webGL-container").append(renderer.domElement);

        /*stats*/
        stats = new Stats();        
        stats.domElement.style.position = 'absolute';
        stats.domElement.style.left = '0px';
        stats.domElement.style.top = '0px';     
        $("#webGL-container").append( stats.domElement );

    }


    /*ajax запрос, возвращает ID и местоположение меток*/

    

    /*function getxyzvalues(){
        var arr = {"landscapeID": "001"};
        $.ajax({
            type: 'POST',
            url: '/getxyzvalues',
            data: JSON.stringify(arr),
            contentType: "application/json; charset=utf-8",
            dataType: 'json',
            async: false,
            success: function(data, textStatus, jqXHR){
                marks = data;
                if (marks != undefined){
                    if (cube) {
                        $.each(cube, function(index){
                            scene.remove(cube[index]);
                        });                            
                    }
                    $.each(marks, function(index){
                        
                        cubeGeometry = new THREE.BoxGeometry(5, 5, 5);
                        cubeMaterial = new THREE.MeshLambertMaterial({color:0xff3300});
                        cube[index]  = new THREE.Mesh(cubeGeometry, cubeMaterial);

                        cube[index].position.x = marks[index][0]['x'];
                        cube[index].position.y = marks[index][0]['y'];
                        cube[index].position.z = marks[index][0]['z'];
                        cube[index].castShadow = true; 
                        scene.add(cube[index]);
                    });
                }
            },
            
        });
    }*/

    /* конец ajax запрос, возвращает ID и местоположение меток */
    


    /* вызов  ajax запрос, возвращает ID и местоположение меток каждые 10 сек*/
    /*setInterval(getxyzvalues, 5000);*/
    /* конец вызов  ajax запрос, возвращает ID и местоположение меток каждые 10 сек*/




    function animate(){
        requestAnimationFrame(animate);
        stats.update();     
        renderer.render(scene, camera);
    }
    
    $(window).resize(function(){


        SCREEN_WIDTH = window.innerWidth;
        SCREEN_HEIGHT = window.innerHeight;

        camera.aspect = SCREEN_WIDTH / SCREEN_HEIGHT;
        camera.updateProjectionMatrix();

        renderer.setSize( SCREEN_WIDTH, SCREEN_HEIGHT );



    });
    init(); 
    animate();
});