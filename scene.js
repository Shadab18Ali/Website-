/* Original WebGL storefront sculpture. No external renderer or texture downloads. */
(() => {
  const canvas = document.querySelector('#atelierCanvas');
  if (!canvas || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const gl = canvas.getContext('webgl', { alpha: false, antialias: false, powerPreference: 'low-power' });
  if (!gl) return;

  const vertex = `attribute vec2 aPosition; void main(){gl_Position=vec4(aPosition,0.0,1.0);}`;
  const fragment = `
    precision highp float;
    uniform vec2 uResolution;
    uniform vec2 uPointer;
    uniform float uTime;

    float box(vec3 p,vec3 b){vec3 q=abs(p)-b;return length(max(q,0.0))+min(max(q.x,max(q.y,q.z)),0.0);}
    float roundBox(vec3 p,vec3 b,float r){return box(p,b-vec3(r))-r;}
    float torus(vec3 p,vec2 t){vec2 q=vec2(length(p.xz)-t.x,p.y);return length(q)-t.y;}
    vec2 add(vec2 a,vec2 b){return a.x<b.x?a:b;}
    vec2 scene(vec3 p){
      vec2 d=vec2(p.y+0.23,1.0);
      d=add(d,vec2(roundBox(p-vec3(0.0,-0.05,0.0),vec3(2.35,0.18,1.62),0.10),2.0));
      // A freestanding browser portal assembled from architectural beams.
      d=add(d,vec2(roundBox(p-vec3(-1.18,1.43,0.0),vec3(0.15,1.40,0.15),0.06),3.0));
      d=add(d,vec2(roundBox(p-vec3(1.18,1.43,0.0),vec3(0.15,1.40,0.15),0.06),3.0));
      d=add(d,vec2(roundBox(p-vec3(0.0,2.83,0.0),vec3(1.32,0.15,0.15),0.06),3.0));
      d=add(d,vec2(roundBox(p-vec3(0.0,0.04,0.0),vec3(1.32,0.11,0.15),0.04),3.0));
      d=add(d,vec2(roundBox(p-vec3(0.0,1.43,0.09),vec3(1.01,1.13,0.045),0.035),4.0));
      // Floating product: a polished object and an orbiting commerce ring.
      vec3 product=p-vec3(0.30,1.39,0.55);
      product.y+=sin(uTime*0.8)*0.065;
      d=add(d,vec2(length(product)-0.43,5.0));
      vec3 ring=product;ring.xz=mat2(0.85,-0.53,0.53,0.85)*ring.xz;
      d=add(d,vec2(torus(ring,vec2(0.59,0.045)),6.0));
      // UI cards and loose building blocks around the portal.
      vec3 card=p-vec3(1.58,1.96,0.72);card.xy=mat2(0.96,-0.28,0.28,0.96)*card.xy;
      d=add(d,vec2(roundBox(card,vec3(0.48,0.34,0.055),0.06),7.0));
      vec3 card2=p-vec3(-1.65,0.83,0.66);card2.xy=mat2(0.96,0.28,-0.28,0.96)*card2.xy;
      d=add(d,vec2(roundBox(card2,vec3(0.39,0.31,0.07),0.05),8.0));
      d=add(d,vec2(roundBox(p-vec3(-1.43,0.32,-0.61),vec3(0.31,0.31,0.31),0.04),9.0));
      d=add(d,vec2(roundBox(p-vec3(1.49,0.23,-0.58),vec3(0.24,0.24,0.24),0.04),9.0));
      return d;
    }
    vec3 normal(vec3 p){vec2 e=vec2(0.002,0.0);return normalize(vec3(scene(p+e.xyy).x-scene(p-e.xyy).x,scene(p+e.yxy).x-scene(p-e.yxy).x,scene(p+e.yyx).x-scene(p-e.yyx).x));}
    float shadow(vec3 ro,vec3 rd){float res=1.0;float t=0.03;for(int i=0;i<20;i++){float h=scene(ro+rd*t).x;res=min(res,10.0*h/t);t+=clamp(h,0.025,0.24);if(h<0.001||t>9.0)break;}return clamp(res,0.25,1.0);}
    vec3 material(float id,vec3 p){
      if(id<1.5){float grid=0.0;vec2 q=abs(fract(p.xz*0.7)-0.5);grid=1.0-smoothstep(0.012,0.027,min(q.x,q.y));return mix(vec3(0.75,0.72,0.67),vec3(0.69,0.67,0.62),grid*0.16);}
      if(id<2.5)return vec3(0.22,0.31,0.35);
      if(id<3.5)return vec3(0.12,0.25,0.30);
      if(id<4.5){
        vec3 c=vec3(0.93,0.88,0.78);
        if(p.y>2.38)c=vec3(0.96,0.93,0.87);
        else if(p.y<0.48)c=vec3(0.17,0.33,0.35);
        else if(p.x< -0.31 && p.y>1.12 && p.y<1.98)c=vec3(0.87,0.44,0.26);
        else if(p.x< -0.35 && p.y<1.05 && p.y>0.80)c=vec3(0.17,0.33,0.35);
        return c;
      }
      if(id<5.5)return vec3(0.94,0.35,0.16);
      if(id<6.5)return vec3(0.93,0.72,0.34);
      if(id<7.5)return vec3(0.26,0.63,0.58);
      if(id<8.5)return vec3(0.95,0.77,0.43);
      return vec3(0.74,0.34,0.24);
    }
    void main(){
      vec2 uv=(gl_FragCoord.xy-0.5*uResolution)/uResolution.y;
      float ang=0.05+uPointer.x*0.15;
      vec3 ro=vec3(4.10+sin(ang)*1.6,3.00+uPointer.y*0.28,7.95);
      vec3 ta=vec3(-1.18,1.28,0.0);
      vec3 ww=normalize(ta-ro),uu=normalize(cross(ww,vec3(0.0,1.0,0.0))),vv=cross(uu,ww);
      vec3 rd=normalize(uv.x*uu+uv.y*vv+1.48*ww);
      vec3 bg=mix(vec3(0.84,0.81,0.75),vec3(0.90,0.86,0.79),smoothstep(-0.35,0.65,uv.y));
      float t=0.0;vec2 hit=vec2(0.0);
      for(int i=0;i<72;i++){hit=scene(ro+rd*t);if(hit.x<0.001||t>23.0)break;t+=hit.x*0.78;}
      vec3 col=bg;
      if(t<23.0){
        vec3 p=ro+rd*t;vec3 n=normal(p);vec3 light=normalize(vec3(-0.55,0.9,0.65));
        float diff=max(dot(n,light),0.0);float shade=shadow(p+n*0.008,light);
        float ambient=0.62+0.12*n.y;float spec=pow(max(dot(reflect(-light,n),-rd),0.0),26.0)*0.17;
        col=material(hit.y,p)*(ambient+diff*0.62*shade)+spec;
        float fog=1.0-exp(-0.004*t*t);col=mix(col,bg,fog);
      }
      col=pow(col,vec3(0.94));
      gl_FragColor=vec4(col,1.0);
    }
  `;

  function compile(type, source) {
    const shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
      console.warn('Storefront 3D scene unavailable:', gl.getShaderInfoLog(shader));
      gl.deleteShader(shader);
      return null;
    }
    return shader;
  }
  const vs = compile(gl.VERTEX_SHADER, vertex);
  const fs = compile(gl.FRAGMENT_SHADER, fragment);
  if (!vs || !fs) return;
  const program = gl.createProgram();
  gl.attachShader(program, vs);
  gl.attachShader(program, fs);
  gl.linkProgram(program);
  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) return;
  gl.useProgram(program);
  const buffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1,-1,1,-1,-1,1,1,1]), gl.STATIC_DRAW);
  const pos = gl.getAttribLocation(program, 'aPosition');
  gl.enableVertexAttribArray(pos);
  gl.vertexAttribPointer(pos, 2, gl.FLOAT, false, 0, 0);
  const resolution = gl.getUniformLocation(program, 'uResolution');
  const pointer = gl.getUniformLocation(program, 'uPointer');
  const time = gl.getUniformLocation(program, 'uTime');
  const target = { x: 0, y: 0 };
  const current = { x: 0, y: 0 };
  let visible = true;
  let lastFrame = 0;
  const started = performance.now();
  const observer = new IntersectionObserver(entries => { visible = entries[0].isIntersecting; }, { threshold: 0 });
  observer.observe(canvas);
  const hero = canvas.closest('.hero');
  hero.addEventListener('pointermove', event => {
    if (!window.matchMedia('(pointer: fine)').matches) return;
    const rect = hero.getBoundingClientRect();
    target.x = (event.clientX - rect.left) / rect.width * 2 - 1;
    target.y = (event.clientY - rect.top) / rect.height * 2 - 1;
  });
  hero.addEventListener('pointerleave', () => { target.x = 0; target.y = 0; });

  function frame(now) {
    requestAnimationFrame(frame);
    if (!visible || document.hidden || now - lastFrame < 42) return;
    lastFrame = now;
    const rect = canvas.getBoundingClientRect();
    const scale = Math.min(window.devicePixelRatio || 1, innerWidth < 700 ? 0.70 : 0.82);
    const width = Math.max(1, Math.round(rect.width * scale));
    const height = Math.max(1, Math.round(rect.height * scale));
    if (canvas.width !== width || canvas.height !== height) {
      canvas.width = width; canvas.height = height;
      gl.viewport(0, 0, width, height);
    }
    current.x += (target.x - current.x) * 0.04;
    current.y += (target.y - current.y) * 0.04;
    gl.uniform2f(resolution, width, height);
    gl.uniform2f(pointer, current.x, current.y);
    gl.uniform1f(time, (now - started) / 1000);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    if (!hero.classList.contains('webgl-ready')) hero.classList.add('webgl-ready');
  }
  requestAnimationFrame(frame);
})();
