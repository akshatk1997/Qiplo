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

    // Ambient Hero Wave Canvas (Fluid Living Telemetry Ripple - Chromatic Ribbon Wave)
    function initHeroWaveCanvas(canvasId = 'heroWaveCanvas') {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let width, height, dpr;
        function resize() {
            dpr = Math.min(window.devicePixelRatio || 1, 2);
            width = canvas.parentElement ? canvas.parentElement.clientWidth : 1200;
            height = canvas.parentElement ? canvas.parentElement.clientHeight : 56;
            canvas.width = Math.round(width * dpr);
            canvas.height = Math.round(height * dpr);
            ctx.scale(dpr, dpr);
        }

        window.addEventListener('resize', resize, { passive: true });
        resize();

        let time = 0;
        // 6 distinct pastel/vivid chromatic ribbon lines matching the reference UI:
        // Sky Blue, Soft Purple/Indigo, Rose Pink, Amber Orange, Canary Yellow, Turquoise Mint
        const ribbonLines = [
            { color: '#38BDF8', speed: 0.013, freq: 0.0042, amp: 14, phase: 0.0, yOffset: -5 },
            { color: '#818CF8', speed: 0.017, freq: 0.0050, amp: 16, phase: 1.1, yOffset: -2 },
            { color: '#F472B6', speed: 0.011, freq: 0.0038, amp: 15, phase: 2.3, yOffset: 1 },
            { color: '#FB923C', speed: 0.019, freq: 0.0055, amp: 13, phase: 3.5, yOffset: 4 },
            { color: '#FACC15', speed: 0.015, freq: 0.0046, amp: 14, phase: 4.7, yOffset: 6 },
            { color: '#2DD4BF', speed: 0.021, freq: 0.0052, amp: 12, phase: 5.8, yOffset: 0 }
        ];

        function animate() {
            ctx.clearRect(0, 0, width, height);
            time += 1;

            const isDark = document.body && document.body.classList.contains('dark-theme');
            const centerY = height * 0.48;

            // Generate points along smooth sine harmonics
            const pointsByLine = ribbonLines.map(line => {
                const pts = [];
                for (let x = 0; x <= width + 8; x += 8) {
                    const y = centerY + line.yOffset +
                        Math.sin(x * line.freq + time * line.speed + line.phase) * line.amp +
                        Math.cos(x * (line.freq * 0.6) - time * (line.speed * 0.7) + line.phase * 0.5) * (line.amp * 0.4);
                    pts.push({ x, y });
                }
                return pts;
            });

            // Delicate iridescent silk gradient fill between top and bottom ribbon envelopes
            if (pointsByLine.length >= 2) {
                const topPts = pointsByLine[0];
                const botPts = pointsByLine[4] || pointsByLine[pointsByLine.length - 1];

                ctx.beginPath();
                ctx.moveTo(topPts[0].x, topPts[0].y);
                for (let i = 1; i < topPts.length; i++) {
                    ctx.lineTo(topPts[i].x, topPts[i].y);
                }
                for (let i = botPts.length - 1; i >= 0; i--) {
                    ctx.lineTo(botPts[i].x, botPts[i].y);
                }
                ctx.closePath();

                const ribbonGrad = ctx.createLinearGradient(0, 0, width, 0);
                ribbonGrad.addColorStop(0.0, 'rgba(56, 189, 248, 0.06)');
                ribbonGrad.addColorStop(0.25, 'rgba(129, 140, 248, 0.07)');
                ribbonGrad.addColorStop(0.5, 'rgba(244, 114, 182, 0.07)');
                ribbonGrad.addColorStop(0.75, 'rgba(251, 146, 60, 0.06)');
                ribbonGrad.addColorStop(1.0, 'rgba(250, 204, 21, 0.05)');

                ctx.fillStyle = ribbonGrad;
                ctx.fill();
            }

            // Draw individual graceful, luminous ribbon strokes
            ribbonLines.forEach((line, idx) => {
                const pts = pointsByLine[idx];
                ctx.beginPath();
                ctx.moveTo(pts[0].x, pts[0].y);

                for (let i = 1; i < pts.length; i++) {
                    const xc = (pts[i - 1].x + pts[i].x) / 2;
                    const yc = (pts[i - 1].y + pts[i].y) / 2;
                    ctx.quadraticCurveTo(pts[i - 1].x, pts[i - 1].y, xc, yc);
                }
                ctx.lineTo(pts[pts.length - 1].x, pts[pts.length - 1].y);

                ctx.strokeStyle = line.color;
                ctx.lineWidth = isDark ? 1.75 : 1.55;
                ctx.globalAlpha = isDark ? 0.9 : 0.82;

                if (isDark) {
                    ctx.shadowColor = line.color;
                    ctx.shadowBlur = 6;
                } else {
                    ctx.shadowBlur = 0;
                }

                ctx.stroke();
            });

            ctx.globalAlpha = 1.0;
            ctx.shadowBlur = 0;
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
            initHeroWaveCanvas('bottomCtaWaveCanvas');
        });
    } else {
        bindInteractiveWaves();
        initHeroWaveCanvas('heroWaveCanvas');
        initHeroWaveCanvas('bottomCtaWaveCanvas');
    }
})();
