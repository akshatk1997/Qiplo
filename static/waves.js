/**
 * Qiplo Waves at Home Motion Engine
 * Inspired by James Camarota's Waves at Home & Jakub Antalik's Distortion Waves
 * Multi-stop chromatic ripple waves, glowing rims, edge particles, and fluid state changes.
 */

(function () {
    'use strict';

    const PALETTES = {
        aurora: ['#ff5fa8', '#ff9a5a', '#ffd76a', '#4fd8e8', '#4d8dff', '#a45cff'],
        ember: ['#ff6a3d', '#ffb347', '#ffe08a', '#ff8c42', '#ff3d81', '#ffc46b'],
        ocean: ['#3b82f6', '#22d3ee', '#a5c8ff', '#2563eb', '#38bdf8', '#6f7bff'],
        violet: ['#a855f7', '#ec4899', '#f0abfc', '#6366f1', '#8b5cf6', '#ff7ac2'],
        cyber: ['#00f5ff', '#3b82f6', '#8b5cf6', '#d946ef', '#ff007f', '#00f5ff']
    };

    function hexToRgb(hex) {
        const c = parseInt(hex.replace('#', ''), 16);
        return [(c >> 16) & 255, (c >> 8) & 255, c & 255];
    }

    function samplePalette(colors, t) {
        t = ((t % 1) + 1) % 1;
        const n = colors.length;
        const idx = t * n;
        const i0 = Math.floor(idx) % n;
        const i1 = (i0 + 1) % n;
        const f = idx - Math.floor(idx);
        const rgb0 = hexToRgb(colors[i0]);
        const rgb1 = hexToRgb(colors[i1]);
        return [
            Math.round(rgb0[0] + (rgb1[0] - rgb0[0]) * f),
            Math.round(rgb0[1] + (rgb1[1] - rgb0[1]) * f),
            Math.round(rgb0[2] + (rgb1[2] - rgb0[2]) * f)
        ];
    }

    // Trigger a chromatic distortion wave across any card element
    function triggerCardWave(el, clientX, clientY, paletteName = 'aurora', duration = 750) {
        if (!el || !(el instanceof HTMLElement)) return;

        const rect = el.getBoundingClientRect();
        if (rect.width <= 0 || rect.height <= 0) return;

        const srcX = (clientX != null) ? (clientX - rect.left) : (rect.width / 2);
        const srcY = (clientY != null) ? (clientY - rect.top) : (rect.height / 2);

        // Position helper
        const prevPosition = window.getComputedStyle(el).position;
        if (prevPosition === 'static') {
            el.style.position = 'relative';
        }

        const canvas = document.createElement('canvas');
        canvas.className = 'qiplo-card-wave-canvas';
        canvas.style.position = 'absolute';
        canvas.style.left = '0';
        canvas.style.top = '0';
        canvas.style.width = '100%';
        canvas.style.height = '100%';
        canvas.style.pointerEvents = 'none';
        canvas.style.borderRadius = window.getComputedStyle(el).borderRadius || '16px';
        canvas.style.zIndex = '15';
        canvas.style.overflow = 'hidden';

        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        canvas.width = Math.round(rect.width * dpr);
        canvas.height = Math.round(rect.height * dpr);

        el.appendChild(canvas);

        const ctx = canvas.getContext('2d');
        if (!ctx) {
            canvas.remove();
            return;
        }

        ctx.scale(dpr, dpr);

        const colors = PALETTES[paletteName] || PALETTES.aurora;
        const maxRadius = Math.hypot(
            Math.max(srcX, rect.width - srcX),
            Math.max(srcY, rect.height - srcY)
        ) + 40;

        const startTime = performance.now();

        // Particles left behind the wave
        const particleCount = Math.min(18, Math.round((rect.width * rect.height) / 12000));
        const particles = [];
        for (let i = 0; i < particleCount; i++) {
            const angle = Math.random() * Math.PI * 2;
            const dist = Math.random() * (maxRadius * 0.85);
            particles.push({
                x: srcX + Math.cos(angle) * dist,
                y: srcY + Math.sin(angle) * dist,
                r: 1 + Math.random() * 2.2,
                color: colors[i % colors.length],
                alpha: 0,
                targetAlpha: 0.5 + Math.random() * 0.45,
                delay: (dist / maxRadius) * 0.6
            });
        }

        function renderFrame(now) {
            const elapsed = now - startTime;
            const progress = Math.min(1, elapsed / duration);

            ctx.clearRect(0, 0, rect.width, rect.height);

            // Ease-out progress for wave front
            const easeFront = 1 - Math.pow(1 - progress, 1.8);
            const currentRadius = easeFront * maxRadius;

            // Draw glowing rim
            const rimWidth = Math.max(35, currentRadius * 0.28);
            const rimGrad = ctx.createRadialGradient(
                srcX, srcY, Math.max(0, currentRadius - rimWidth),
                srcX, srcY, currentRadius + 15
            );

            const fade = Math.sin(progress * Math.PI);
            const c0 = samplePalette(colors, progress);
            const c1 = samplePalette(colors, progress + 0.35);
            const c2 = samplePalette(colors, progress + 0.7);

            rimGrad.addColorStop(0, `rgba(${c0[0]}, ${c0[1]}, ${c0[2]}, 0)`);
            rimGrad.addColorStop(0.5, `rgba(${c1[0]}, ${c1[1]}, ${c1[2]}, ${0.45 * fade})`);
            rimGrad.addColorStop(0.85, `rgba(255, 255, 255, ${0.7 * fade})`);
            rimGrad.addColorStop(1, `rgba(${c2[0]}, ${c2[1]}, ${c2[2]}, 0)`);

            ctx.save();
            ctx.fillStyle = rimGrad;
            ctx.beginPath();
            ctx.arc(srcX, srcY, currentRadius + 15, 0, Math.PI * 2);
            ctx.fill();

            // Edge particles
            for (let i = 0; i < particles.length; i++) {
                const p = particles[i];
                if (progress > p.delay) {
                    const localP = (progress - p.delay) / (1 - p.delay);
                    const pFade = Math.sin(localP * Math.PI);
                    ctx.fillStyle = p.color;
                    ctx.globalAlpha = p.targetAlpha * pFade;
                    ctx.beginPath();
                    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                    ctx.fill();
                }
            }

            ctx.restore();

            // Linger glow along edges
            if (progress > 0.4) {
                const edgeAlpha = Math.sin((progress - 0.4) / 0.6 * Math.PI) * 0.35;
                el.style.boxShadow = `0 0 25px rgba(${c1[0]}, ${c1[1]}, ${c1[2]}, ${edgeAlpha.toFixed(3)})`;
            }

            if (progress < 1) {
                requestAnimationFrame(renderFrame);
            } else {
                canvas.remove();
                el.style.boxShadow = '';
            }
        }

        requestAnimationFrame(renderFrame);
    }

    // Wide sweep wave across a panel or container (e.g. on Tab change)
    function triggerSweepWave(container, direction = 'left-to-right', paletteName = 'ocean') {
        if (!container || !(container instanceof HTMLElement)) return;
        const rect = container.getBoundingClientRect();
        if (rect.width <= 0 || rect.height <= 0) return;

        const srcX = (direction === 'left-to-right') ? -50 : rect.width + 50;
        const srcY = rect.height / 2;
        triggerCardWave(container, rect.left + srcX, rect.top + srcY, paletteName, 850);
    }

    // Ambient Hero Wave Canvas (Fluid Living Telemetry Ripple)
    function initHeroWaveCanvas(canvasId = 'heroWaveCanvas') {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let width, height, dpr;
        function resize() {
            dpr = Math.min(window.devicePixelRatio || 1, 2);
            width = canvas.parentElement ? canvas.parentElement.clientWidth : 1200;
            height = canvas.parentElement ? canvas.parentElement.clientHeight : 160;
            canvas.width = Math.round(width * dpr);
            canvas.height = Math.round(height * dpr);
            ctx.scale(dpr, dpr);
        }

        window.addEventListener('resize', resize, { passive: true });
        resize();

        let time = 0;
        const waves = [
            { speed: 0.018, freq: 0.006, amp: 24, phase: 0, palette: PALETTES.cyber },
            { speed: 0.024, freq: 0.009, amp: 18, phase: 1.5, palette: PALETTES.aurora },
            { speed: 0.012, freq: 0.004, amp: 14, phase: 3.2, palette: PALETTES.violet }
        ];

        function animate() {
            ctx.clearRect(0, 0, width, height);

            time += 1;

            waves.forEach((w, wIdx) => {
                ctx.beginPath();
                ctx.moveTo(0, height);

                for (let x = 0; x <= width; x += 6) {
                    const y = (height * 0.6) +
                        Math.sin(x * w.freq + time * w.speed + w.phase) * w.amp +
                        Math.cos(x * w.freq * 0.5 - time * w.speed * 0.6) * (w.amp * 0.4);
                    if (x === 0) {
                        ctx.lineTo(x, y);
                    } else {
                        ctx.lineTo(x, y);
                    }
                }

                ctx.lineTo(width, height);
                ctx.closePath();

                const grad = ctx.createLinearGradient(0, 0, width, 0);
                const colors = w.palette;
                colors.forEach((c, idx) => {
                    grad.addColorStop(idx / (colors.length - 1), c);
                });

                ctx.fillStyle = grad;
                ctx.globalAlpha = 0.08 + wIdx * 0.04;
                ctx.fill();

                // Luminous top crest line
                ctx.beginPath();
                for (let x = 0; x <= width; x += 6) {
                    const y = (height * 0.6) +
                        Math.sin(x * w.freq + time * w.speed + w.phase) * w.amp +
                        Math.cos(x * w.freq * 0.5 - time * w.speed * 0.6) * (w.amp * 0.4);
                    if (x === 0) ctx.moveTo(x, y);
                    else ctx.lineTo(x, y);
                }
                ctx.strokeStyle = grad;
                ctx.lineWidth = 1.5;
                ctx.globalAlpha = 0.25 + wIdx * 0.15;
                ctx.stroke();
            });

            ctx.globalAlpha = 1;
            requestAnimationFrame(animate);
        }

        requestAnimationFrame(animate);
    }

    // Auto-bind click waves to interactive cards & buttons
    function bindInteractiveWaves() {
        document.addEventListener('click', function (e) {
            const target = e.target.closest('.primaryBtn, .ghostBtn, .tab, .special-module-card, .telemetryCard, .aiCard, .fStatCard, .chip, .termBox');
            if (!target) return;

            // Pick palette based on context
            let pal = 'aurora';
            if (target.classList.contains('primaryBtn') || target.classList.contains('active')) {
                pal = 'cyber';
            } else if (target.closest('#tab-sandbox') || target.classList.contains('danger') || target.classList.contains('dangerBtn')) {
                pal = 'ember';
            } else if (target.closest('#tab-customers') || target.closest('#tab-overview')) {
                pal = 'ocean';
            } else if (target.closest('#tab-business') || target.closest('#tab-copilot')) {
                pal = 'violet';
            }

            // Tactile press scale feedback (like in cards.js button: scale 0.975)
            target.style.transition = 'transform 0.12s cubic-bezier(0.16, 1, 0.3, 1)';
            target.style.transform = 'scale(0.975)';
            setTimeout(() => {
                target.style.transform = '';
            }, 140);

            // Trigger card wave
            const cardParent = target.closest('.aiCard, .special-module-card, .telemetryCard, .framer-card, .bizCard, .presentationHub') || target;
            triggerCardWave(cardParent, e.clientX, e.clientY, pal, 650);
        }, { passive: true });
    }

    // Expose global QiploWaves API
    window.QiploWaves = {
        PALETTES,
        trigger: triggerCardWave,
        sweep: triggerSweepWave,
        initHeroWave: initHeroWaveCanvas,
        bindInteractive: bindInteractiveWaves
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            bindInteractiveWaves();
            initHeroWaveCanvas('heroWaveCanvas');
        });
    } else {
        bindInteractiveWaves();
        initHeroWaveCanvas('heroWaveCanvas');
    }
})();
