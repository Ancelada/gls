// Set up the scene, camera, and renderer as global variables.
var scene, camera, renderer;

init();
animate();

// Sets up the scene.
function init() {
  // Create the scene and set the scene size.
  scene = new THREE.Scene();
  var WIDTH = window.innerWidth,
      HEIGHT = window.innerHeight;

  // Create a renderer and add it to the DOM.
  renderer = new THREE.WebGLRenderer({antialias:true});
  renderer.setSize(WIDTH, HEIGHT);
  document.body.appendChild(renderer.domElement);

  // Create a camera, zoom it out from the model a bit, and add it to the scene.
  camera = new THREE.PerspectiveCamera(45, WIDTH / HEIGHT, 0.1, 20000);
  camera.position.set(50,150,100);
  scene.add(camera);

  // Create an event listener that resizes the renderer with the browser window.
  window.addEventListener('resize', function() {
    var WIDTH = window.innerWidth,
        HEIGHT = window.innerHeight;
    renderer.setSize(WIDTH, HEIGHT);
    camera.aspect = WIDTH / HEIGHT;
    camera.updateProjectionMatrix();
  });

  scene = new THREE.Scene();
  var WIDTH = window.innerWidth,
      HEIGHT = window.innerHeight;

  renderer = new THREE.WebGLRenderer({antialias:true});
  renderer.setSize(WIDTH, HEIGHT);
  document.body.appendChild(renderer.domElement);

  camera = new THREE.PerspectiveCamera(45, WIDTH / HEIGHT, 0.1, 10000);
  camera.position.set(50,150,100);
  scene.add(camera);

  window.addEventListener('resize', function() {
    var WIDTH = window.innerWidth,
        HEIGHT = window.innerHeight;
    renderer.setSize(WIDTH, HEIGHT);
    camera.aspect = WIDTH / HEIGHT;
    camera.updateProjectionMatrix();
  });

  controls = new THREE.OrbitControls(camera, renderer.domElement);

  var light = new THREE.PointLight(0xfffff3, 0.8);
  light.position.set(-100,200,100);
  scene.add(light);

  var sphereSize = 1; 
  var pointLightHelper = new THREE.PointLightHelper( light, sphereSize ); 
  scene.add( pointLightHelper );

  var light2 = new THREE.PointLight(0xd7f0ff, 0.2);
  light2.position.set(200,200,100);
  scene.add(light2);

  var sphereSize = 1; 
  var pointLightHelper2 = new THREE.PointLightHelper( light2, sphereSize ); 
  scene.add( pointLightHelper2 );

  var light3 = new THREE.PointLight(0xFFFFFF, 0.5);
  light3.position.set(150,200,-100);
  scene.add(light3);

  var sphereSize = 1; 
  var pointLightHelper3 = new THREE.PointLightHelper( light3, sphereSize ); 
  scene.add( pointLightHelper3 );


  var loader = new THREE.ColladaLoader();
  loader.options.convertUpAxis = true;
  loader.load( 'static/js/webgl/models/dummy1.dae', function ( collada ) {
  //dummy1.dae
    var dae = collada.scene;
    var skin = collada.skins[ 0 ];
    dae.position.set(0,0,0);//x,z,y- if you think in blender dimensions ;)
    dae.scale.set(1.5,1.5,1.5);
    scene.add(dae);
  });
  
}

function animate() {
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
  controls.update();
}