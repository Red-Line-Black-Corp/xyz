// Lightweight Three.js scene showing translucent grid, sagittal/coronal/transverse planes,
// labeled axes and a stylized head/torso proxy for orientation.
(function () {
  const container = document.getElementById("scene");

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0a0a0a);

  const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 5000);
  camera.position.set(400, 200, 400);

  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  container.appendChild(renderer.domElement);

  const controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.target.set(0,0,0);
  controls.update();

  // Axes helper (RAS: +X right, +Y anterior/forward, +Z superior/up)
  const axes = new THREE.AxesHelper(200);
  scene.add(axes);

  // translucent 3D grid (XY, YZ, XZ benchmark)
  const gridXY = new THREE.GridHelper(800, 16, 0x444444, 0x222222);
  gridXY.rotation.x = Math.PI / 2; // XY plane
  gridXY.material.opacity = 0.25; gridXY.material.transparent = true;
  scene.add(gridXY);

  // Planes: sagittal (XZ), coronal (YZ), transverse (XY)
  const planeMat = new THREE.MeshBasicMaterial({ color: 0x0066ff, opacity: 0.18, transparent: true, side: THREE.DoubleSide });
  const sagittal = new THREE.Mesh(new THREE.PlaneGeometry(600, 400), planeMat.clone());
  sagittal.rotation.y = Math.PI / 2; sagittal.position.x = 0; // midsagittal
  const coronal = new THREE.Mesh(new THREE.PlaneGeometry(600, 400), planeMat.clone()); coronal.position.y = 0;
  const transverse = new THREE.Mesh(new THREE.PlaneGeometry(600, 600), planeMat.clone()); transverse.rotation.x = Math.PI/2; transverse.position.z = 0;

  scene.add(sagittal); scene.add(coronal); scene.add(transverse);

  // Stylized head & torso proxy (simple spheres & cylinders anchored to anatomical landmarks)
  const headGeom = new THREE.SphereGeometry(40, 32, 16);
  const headMat = new THREE.MeshPhongMaterial({ color: 0xffccaa, opacity: 0.95, transparent: true });
  const head = new THREE.Mesh(headGeom, headMat);
  head.position.set(0, 80, 30); // roughly near glabella origin offset
  scene.add(head);

  const torsoGeom = new THREE.CylinderGeometry(60, 75, 160, 32);
  const torsoMat = new THREE.MeshPhongMaterial({ color: 0x88aaee, opacity: 0.9, transparent: true });
  const torso = new THREE.Mesh(torsoGeom, torsoMat);
  torso.position.set(0, -20, -40);
  scene.add(torso);

  // Landmarks: glabella, tragion (approx), occipital
  function makeLabel(text, pos, color=0xffee88){
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    ctx.font = '24px Arial';
    ctx.fillStyle = '#ffffff';
    ctx.fillText(text, 2, 24);
    const tex = new THREE.CanvasTexture(canvas);
    const spriteMat = new THREE.SpriteMaterial({ map: tex, depthTest: false });
    const sprite = new THREE.Sprite(spriteMat);
    sprite.scale.set(80, 30, 1);
    sprite.position.copy(pos);
    scene.add(sprite);
  }
  // glabella at origin
  const glabella = new THREE.Vector3(0, 0, 0);
  makeLabel('Glabella (Origin)', glabella);

  makeLabel('Tragion (approx)', new THREE.Vector3(75, 10, 25));
  makeLabel('Occipital (approx)', new THREE.Vector3(0, -40, -120));

  // Lighting
  const hemi = new THREE.HemisphereLight(0xffffff, 0x444444, 0.6);
  scene.add(hemi);
  const dir = new THREE.DirectionalLight(0xffffff, 0.6);
  dir.position.set(200, 400, 100);
  scene.add(dir);

  // Animation (simple keyframe along +Y then rotate)
  let animating = false;
  let startTime = 0;
  function startAnimation() { animating = true; startTime = performance.now(); }
  function stopAnimation() { animating = false; head.position.set(0,80,30); head.rotation.set(0,0,0); torso.position.set(0,-20,-40); }

  // UI bindings
  document.getElementById('playBtn').addEventListener('click', () => startAnimation());
  document.getElementById('stopBtn').addEventListener('click', () => stopAnimation());
  document.getElementById('showPlanes').addEventListener('change', (ev) => {
    const show = ev.target.checked;
    sagittal.visible = show; coronal.visible = show; transverse.visible = show;
  });

  function animate() {
    requestAnimationFrame(animate);
    const now = performance.now();
    if (animating) {
      const t = ((now - startTime) / 1000.0) % 6.0; // 6s loop
      // translate head gently anterior (+Y) and back
      head.position.y = 80 + 30 * Math.sin((t / 6.0) * Math.PI * 2.0);
      // rotate torso slowly about Z
      torso.rotation.z = 0.05 * Math.sin((t / 6.0) * Math.PI * 2.0);
    }
    renderer.render(scene, camera);
  }
  animate();

  // Resize
  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth/window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });
})();
