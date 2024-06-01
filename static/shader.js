window.onload = function () {
  const canvas = document.querySelector("canvas");
  const gl = canvas.getContext("webgl");
  if (!gl) {
    alert("Failed to initialize WebGL.");
  }

  const vertexShaderSource = `
            attribute vec4 a_position;
            void main() {
                gl_Position = a_position;
            }
        `;

  const fragmentShaderSource = `
            precision highp float;
            uniform vec2 u_resolution;
            uniform float u_time;

            float hash(vec3 p) {
                return fract(sin(dot(p, vec3(127.1, 311.7, 235.2))) * 43758.5453);
            }

            float noise(vec3 p) {
                vec3 i = floor(p);
                vec3 f = fract(p);

                vec3 u = f * f * (3.0 - 2.0 * f);

                return mix(
                    mix(
                        mix(hash(i), hash(i + vec3(1.0, 0.0, 0.0)), u.x),
                        mix(hash(i + vec3(0.0, 1.0, 0.0)), hash(i + vec3(1.0, 1.0, 0.0)), u.x),
                        u.y
                    ),
                    mix(
                        mix(hash(i + vec3(0.0, 0.0, 1.0)), hash(i + vec3(1.0, 0.0, 1.0)), u.x),
                        mix(hash(i + vec3(0.0, 1.0, 1.0)), hash(i + vec3(1.0, 1.0, 1.0)), u.x),
                        u.y
                    ),
                    u.z
                );
            }

            float fbm(vec3 p) {
                float v = 0.0;
                float a = 0.5;
                vec3 shift = vec3(101.618);

                for (int i = 0; i < 9; ++i) {
                    v += a * noise(p);
                    p = p * 2.0 + shift;
                    a *= 0.48;
                }

                return v;
            }

            float h(float t) {
                return sin(t * 6.283) * 0.5 + 0.5;
            }

            vec3 aurora(vec2 uv, float time) {
                vec2 q = vec2(uv.x, 1.0 - uv.y + u_time * 0.03);
                vec3 fbmUV = vec3(q * 10., time * 0.5);
                float f = fbm(fbmUV);


                vec3 color = vec3(h(f), h(f + 0.333), h(f + 0.666));

                float mask = smoothstep(0.2, 0.0, abs(uv.y + 0.5 - f) * 5.0); // Mask

                return color * mask;
            }

            float ball(vec2 uv, vec2 center, float radius) {
                vec2 d = uv - center;
                float r2 = dot(d, d);

                // r2 = max(0.0, radius * radius - r2);
                // return pow(r2, 2.0);
                float rad2 = radius * radius;
                return rad2 / (rad2 + r2);
            }

            vec3 getColor(vec2 uv, float time) {
                float lightness = 0.0;

                for (int i = 0; i < 50; ++i) {
                  float t = time * 0.004;
                  float x = 0.0;
                  float y = 0.0;
                  float p1 = sin(t + hash(vec3(i)) * 6.283) * 0.5 + 0.5;
                  float p2 = 1.0 - p1;
                  x += p1 * (noise(vec3(float(i) * 100.0, 0.0, t)) - 0.5) * 3.0;
                  x += p2 * (noise(vec3(float(i) * 100.0, 100.0, t + 0.5)) - 0.5) * 3.0;
                  y += p1 * (noise(vec3(float(i) * 100.0, 200.0, t)) - 0.5) * 2.0;
                  y += p2 * (noise(vec3(float(i) * 100.0, 300.0, t + 0.5)) - 0.5) * 2.0;
                  lightness += ball(uv, vec2(x, y), hash(vec3(i)) * 0.05 + 0.025);
                  // lightness += ball(uv, vec2(x, y), 0.1);
                }

                lightness -= 0.5; // some amount between 0 and 0.5*ballcount
                lightness = max(0.0, lightness);
                lightness = lightness / (lightness + 1.0);
                lightness *= 2.0;
                // lightness = -cos(lightness * 6.283 * 3.) * 0.5 + 0.5;

                float multiplier = 0.8;
                vec3 col0 = vec3(0.0) * multiplier;
                vec3 col1 = vec3(0.5, 0.42, 0.2) * multiplier;
                vec3 col2 = vec3(0.5, 0.2, 0.0) * multiplier;
                vec3 col3 = vec3(0.3, 0.0, 0.1) * multiplier;

                lightness -= 0.25;
                if (lightness < 0.0) {
                    return vec3(0.0);
                }
                lightness *= 5.0;
                if (lightness > 3.0) {
                  col0 = col3;
                }

                lightness = mod(lightness, 3.0);

                if (lightness < 0.5) {
                    float a = 0.0;
                    float b = 0.5;
                    float t = (lightness - a) / (b - a);
                    t = pow(t, 1.0);
                    t = smoothstep(0.0, 1.0, t);
                    return mix(col0, col1, t);
                } else if (lightness < 2.0) {
                  float a = 0.5;
                  float b = 2.0;
                  float t = (lightness - a) / (b - a);
                  t = pow(t, 1.0);
                  t = smoothstep(0.0, 1.0, t);
                  return mix(col1, col2, t);
                } else {
                  float a = 2.0;
                  float b = 3.0;
                  float t = (lightness - a) / (b - a);
                  t = pow(t, 1.0);
                  t = smoothstep(0.0, 1.0, t);
                  return mix(col2, col3, t);
                }
                // float r = pow(lightness, 0.5) * 0.5;
                // float g = pow(lightness, 4.0) * 0.4;
                // float b = pow(lightness, 2.0) * 0.2;
                // vec3 col = vec3(r, g, b);
                // return col;
            }

            void main() {
                vec2 uv = gl_FragCoord.xy - u_resolution.xy * 0.5;
                uv /= u_resolution.y;
                gl_FragColor = vec4(getColor(uv, u_time), 1.0);
            }
        `;

  function createShader(gl, type, source) {
    const shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    const success = gl.getShaderParameter(shader, gl.COMPILE_STATUS);
    if (success) {
      return shader;
    }
    console.error(gl.getShaderInfoLog(shader));
    gl.deleteShader(shader);
  }

  function createProgram(gl, vertexShader, fragmentShader) {
    const program = gl.createProgram();
    gl.attachShader(program, vertexShader);
    gl.attachShader(program, fragmentShader);
    gl.linkProgram(program);
    const success = gl.getProgramParameter(program, gl.LINK_STATUS);
    if (success) {
      return program;
    }
    console.error(gl.getProgramInfoLog(program));
    gl.deleteProgram(program);
  }

  function createFullScreenQuad(gl) {
    const quadBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, quadBuffer);
    gl.bufferData(
      gl.ARRAY_BUFFER,
      new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]),
      gl.STATIC_DRAW
    );
    return quadBuffer;
  }

  const vertexShader = createShader(gl, gl.VERTEX_SHADER, vertexShaderSource);
  const fragmentShader = createShader(
    gl,
    gl.FRAGMENT_SHADER,
    fragmentShaderSource
  );
  const program = createProgram(gl, vertexShader, fragmentShader);
  const positionAttributeLocation = gl.getAttribLocation(program, "a_position");
  const resolutionUniformLocation = gl.getUniformLocation(
    program,
    "u_resolution"
  );
  const timeUniformLocation = gl.getUniformLocation(program, "u_time");
  const quadBuffer = createFullScreenQuad(gl);

  function render() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    gl.viewport(0, 0, gl.canvas.width, gl.canvas.height);
    gl.clearColor(0, 0, 0, 1);
    gl.clear(gl.COLOR_BUFFER_BIT);
    gl.useProgram(program);
    gl.bindBuffer(gl.ARRAY_BUFFER, quadBuffer);

    gl.enableVertexAttribArray(positionAttributeLocation);
    gl.vertexAttribPointer(positionAttributeLocation, 2, gl.FLOAT, false, 0, 0);
    gl.uniform2f(resolutionUniformLocation, gl.canvas.width, gl.canvas.height);
    gl.uniform1f(timeUniformLocation, performance.now() * 0.001);

    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    requestAnimationFrame(render);
  }

  requestAnimationFrame(render);
};
