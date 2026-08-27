import { useEffect, useRef, useCallback } from 'react';

const lerp = (a, b, t) => a + (b - a) * t;

const hexToRgb = (hex) => {
  const r = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return r ? [parseInt(r[1], 16), parseInt(r[2], 16), parseInt(r[3], 16)] : [255, 255, 255];
};

export const AuroraBeam = ({
  color = '#34d399',
  midColor = '#22d3ee',
  deepColor = '#a78bfa',
  speed = 1.0,
  sheets = 5,
  amplitude = 0.12,
  frequency = 3.2,
  thickness = 0.05,
  tail = 0.22,
  position = 0.0,
  slant = 0.1,
  spread = 0.16,
  rays = 0.45,
  rayScale = 26,
  rayDrift = 0.8,
  reactivity = 0.7,
  gain = 1.5,
  exposure = 2.4,
  contrast = 1.0,
  hueDrift = 1.0,
  grain = 0.05,
  opacity = 1.0,
  cursorInteraction = true,
  cursorSway = 0.5,
  paused = false,
  backgroundColor = 'transparent',
  className = '',
}) => {
  const canvasRef = useRef(null);
  const animRef = useRef(null);
  const mouseRef = useRef({ x: 0.5, y: 0.5, active: false });
  const smoothMouseRef = useRef({ x: 0.5, y: 0.5 });
  const timeRef = useRef(0);
  const lastFrameRef = useRef(performance.now());

  const c1 = hexToRgb(color);
  const c2 = hexToRgb(midColor);
  const c3 = hexToRgb(deepColor);

  const draw = useCallback((ctx, w, h, t) => {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    ctx.clearRect(0, 0, w, h);

    if (backgroundColor !== 'transparent') {
      ctx.fillStyle = backgroundColor;
      ctx.fillRect(0, 0, w, h);
    }

    const aspect = w / h;
    const centerY = h * (0.5 + position);
    const mx = smoothMouseRef.current.x;
    const my = smoothMouseRef.current.y;

    const mouseOffsetX = cursorInteraction && mouseRef.current.active
      ? (mx - 0.5) * cursorSway * 0.3
      : 0;
    const mouseOffsetY = cursorInteraction && mouseRef.current.active
      ? (my - 0.5) * cursorSway * 0.15
      : 0;

    for (let s = 0; s < sheets; s++) {
      const sheetT = s / Math.max(sheets - 1, 1);
      const yOffset = (sheetT - 0.5) * spread * h;
      const sheetSlant = slant * h * (sheetT - 0.5);

      const colorMix = sheetT * hueDrift;
      let sr, sg, sb;
      if (colorMix < 0.5) {
        const m = colorMix * 2;
        sr = lerp(c1[0], c2[0], m) / 255;
        sg = lerp(c1[1], c2[1], m) / 255;
        sb = lerp(c1[2], c2[2], m) / 255;
      } else {
        const m = (colorMix - 0.5) * 2;
        sr = lerp(c2[0], c3[0], m) / 255;
        sg = lerp(c2[1], c3[1], m) / 255;
        sb = lerp(c2[2], c3[2], m) / 255;
      }

      const wavePhase = t * speed * 0.5 + s * 0.7;
      const sheetThickness = thickness * h * (1.0 - sheetT * 0.3);
      const sheetAlpha = (1.0 - sheetT * 0.15) * reactivity;

      ctx.save();
      ctx.globalCompositeOperation = 'screen';
      ctx.globalAlpha = sheetAlpha * opacity;

      const segments = 120;
      ctx.beginPath();

      for (let i = 0; i <= segments; i++) {
        const frac = i / segments;
        const x = frac * w;
        const wave = Math.sin(frac * Math.PI * frequency + wavePhase) * amplitude * h;
        const wave2 = Math.sin(frac * Math.PI * frequency * 1.7 + wavePhase * 0.6) * amplitude * h * 0.3;
        const y = centerY + yOffset + wave + wave2 + sheetSlant + mouseOffsetY * h;
        const offsetX = mouseOffsetX * w * Math.sin(frac * Math.PI);

        if (i === 0) {
          ctx.moveTo(x + offsetX, y - sheetThickness);
        } else {
          ctx.lineTo(x + offsetX, y - sheetThickness);
        }
      }

      for (let i = segments; i >= 0; i--) {
        const frac = i / segments;
        const x = frac * w;
        const wave = Math.sin(frac * Math.PI * frequency + wavePhase) * amplitude * h;
        const wave2 = Math.sin(frac * Math.PI * frequency * 1.7 + wavePhase * 0.6) * amplitude * h * 0.3;
        const y = centerY + yOffset + wave + wave2 + sheetSlant + mouseOffsetY * h;
        const tailFade = Math.pow(1.0 - frac, tail * 2) * sheetThickness * 2;
        const offsetX = mouseOffsetX * w * Math.sin(frac * Math.PI);

        ctx.lineTo(x + offsetX, y + sheetThickness + tailFade);
      }

      ctx.closePath();

      const grad = ctx.createLinearGradient(0, centerY + yOffset - sheetThickness * 2, 0, centerY + yOffset + sheetThickness * 4);
      grad.addColorStop(0, `rgba(${Math.round(sr * 255)}, ${Math.round(sg * 255)}, ${Math.round(sb * 255)}, 0)`);
      grad.addColorStop(0.3, `rgba(${Math.round(sr * 255)}, ${Math.round(sg * 255)}, ${Math.round(sb * 255)}, ${0.6 * gain})`);
      grad.addColorStop(0.5, `rgba(${Math.round(sr * 255)}, ${Math.round(sg * 255)}, ${Math.round(sb * 255)}, ${1.0 * gain})`);
      grad.addColorStop(0.7, `rgba(${Math.round(sr * 255)}, ${Math.round(sg * 255)}, ${Math.round(sb * 255)}, ${0.4 * gain})`);
      grad.addColorStop(1, `rgba(${Math.round(sr * 255)}, ${Math.round(sg * 255)}, ${Math.round(sb * 255)}, 0)`);

      ctx.fillStyle = grad;
      ctx.filter = `blur(${Math.max(8, sheetThickness * 0.8)}px)`;
      ctx.fill();
      ctx.filter = 'none';

      ctx.restore();
    }

    if (rays > 0) {
      ctx.save();
      ctx.globalCompositeOperation = 'screen';
      ctx.globalAlpha = rays * opacity * 0.5;

      const rayCount = Math.floor(rayScale);
      for (let i = 0; i < rayCount; i++) {
        const frac = i / rayCount;
        const x = frac * w;
        const drift = Math.sin(t * rayDrift * 0.3 + frac * 5.0) * 20;
        const rayAlpha = (0.3 + 0.7 * Math.sin(frac * Math.PI * 3 + t * 0.5)) * 0.15;
        const rayWidth = 1.5 + Math.sin(t * 0.8 + i) * 0.8;

        ctx.beginPath();
        ctx.moveTo(x + drift, centerY - h * 0.4);
        ctx.lineTo(x + drift + slant * 40, centerY + h * 0.4);
        ctx.strokeStyle = `rgba(${Math.round((c1[0] + c2[0]) / 2)}, ${Math.round((c1[1] + c2[1]) / 2)}, ${Math.round((c1[2] + c2[2]) / 2)}, ${rayAlpha})`;
        ctx.lineWidth = rayWidth;
        ctx.stroke();
      }

      ctx.restore();
    }

    if (grain > 0) {
      // Cheap film grain: draw small translucent speckles instead of a full
      // per-pixel getImageData/putImageData round-trip, which is extremely
      // expensive on full-screen canvases and causes visible flickering.
      ctx.save();
      ctx.globalAlpha = grain * opacity * 0.5;
      const speckCount = Math.floor((w * h) / 1200);
      for (let i = 0; i < speckCount; i++) {
        const sx = Math.floor(Math.random() * w);
        const sy = Math.floor(Math.random() * h);
        const lightness = Math.random();
        ctx.fillStyle = lightness > 0.5
          ? 'rgba(255,255,255,0.35)'
          : 'rgba(0,0,0,0.35)';
        ctx.fillRect(sx, sy, 1, 1);
      }
      ctx.restore();
    }

    if (contrast !== 1.0) {
      ctx.save();
      ctx.globalCompositeOperation = 'source-over';
      const contrastVal = (contrast - 1) * 100;
      ctx.filter = `contrast(${100 + contrastVal}%)`;
      ctx.drawImage(ctx.canvas, 0, 0);
      ctx.filter = 'none';
      ctx.restore();
    }
  }, [c1, c2, c3, speed, sheets, amplitude, frequency, thickness, tail, position, slant, spread, rays, rayScale, rayDrift, reactivity, gain, exposure, contrast, hueDrift, grain, opacity, cursorInteraction, cursorSway, backgroundColor]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const container = canvas.parentElement;

    const resize = () => {
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      const rect = container.getBoundingClientRect();
      canvas.width = rect.width * dpr;
      canvas.height = rect.height * dpr;
      canvas.style.width = rect.width + 'px';
      canvas.style.height = rect.height + 'px';
      ctx.scale(dpr, dpr);
    };

    resize();
    const ro = new ResizeObserver(resize);
    ro.observe(container);

    const onMouseMove = (e) => {
      const rect = canvas.getBoundingClientRect();
      mouseRef.current.x = (e.clientX - rect.left) / rect.width;
      mouseRef.current.y = (e.clientY - rect.top) / rect.height;
      mouseRef.current.active = true;
    };
    const onMouseLeave = () => {
      mouseRef.current.active = false;
    };

    canvas.addEventListener('mousemove', onMouseMove);
    canvas.addEventListener('mouseleave', onMouseLeave);

    let isVisible = true;
    let isPageVisible = !document.hidden;

    const io = new IntersectionObserver(
      ([entry]) => {
        isVisible = entry.isIntersecting;
      },
      { threshold: 0 }
    );
    io.observe(canvas);

    const onVisibility = () => {
      isPageVisible = !document.hidden;
    };
    document.addEventListener('visibilitychange', onVisibility);

    const animate = (now) => {
      if (!paused && isVisible && isPageVisible) {
        const dt = (now - lastFrameRef.current) / 1000;
        timeRef.current += dt * speed;

        smoothMouseRef.current.x = lerp(smoothMouseRef.current.x, mouseRef.current.x, 0.05);
        smoothMouseRef.current.y = lerp(smoothMouseRef.current.y, mouseRef.current.y, 0.05);

        const rect = container.getBoundingClientRect();
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        ctx.scale(dpr, dpr);

        draw(ctx, rect.width, rect.height, timeRef.current);
      }
      lastFrameRef.current = now;
      animRef.current = requestAnimationFrame(animate);
    };

    animRef.current = requestAnimationFrame(animate);

    return () => {
      if (animRef.current) cancelAnimationFrame(animRef.current);
      ro.disconnect();
      io.disconnect();
      document.removeEventListener('visibilitychange', onVisibility);
      canvas.removeEventListener('mousemove', onMouseMove);
      canvas.removeEventListener('mouseleave', onMouseLeave);
    };
  }, [draw, paused, speed]);

  return (
    <div
      className={`aurora-beam-container ${className}`.trim()}
      style={{ position: 'relative', width: '100%', height: '100%', overflow: 'hidden' }}
    >
      <canvas
        ref={canvasRef}
        style={{ position: 'absolute', inset: 0, display: 'block' }}
      />
    </div>
  );
};

export default AuroraBeam;
