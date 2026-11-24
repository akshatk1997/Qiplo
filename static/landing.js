/**
 * QIPLO — Public Enterprise Landing Page Interactive Scripts
 * Theme Line: Plus Jakarta Sans / Inter / Living Waves / Modern Glassmorphism
 */

(function () {
    'use strict';

    // 1. Theme State Initialization & Persistence
    function initTheme() {
        const savedTheme = localStorage.getItem('qiplo_theme') || (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark');
        applyTheme(savedTheme);

        const toggleBtn = document.getElementById('landingThemeToggleBtn');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => {
                const isLight = document.body.classList.contains('light-theme');
                const nextTheme = isLight ? 'dark' : 'light';
                applyTheme(nextTheme);
                localStorage.setItem('qiplo_theme', nextTheme);
            });
        }
    }

    function applyTheme(theme) {
        if (theme === 'light') {
            document.body.classList.remove('dark-theme');
            document.body.classList.add('light-theme');
        } else {
            document.body.classList.remove('light-theme');
            document.body.classList.add('dark-theme');
        }
    }

    // 2. Animated Sinusoidal Living Wave Canvas
    function initLandingWaves() {
        const canvas = document.getElementById('landingWaveCanvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let width, height, dpr;
        function resize() {
            dpr = Math.min(window.devicePixelRatio || 1, 2);
            width = canvas.parentElement ? canvas.parentElement.clientWidth : 1200;
            height = canvas.parentElement ? canvas.parentElement.clientHeight : 60;
            canvas.width = Math.round(width * dpr);
            canvas.height = Math.round(height * dpr);
            ctx.scale(dpr, dpr);
        }

        window.addEventListener('resize', resize, { passive: true });
        resize();

        let time = 0;
        const waves = [
            { speed: 0.020, freq: 0.007, amp: 14, phase: 0, colors: ['#4338CA', '#6366F1', '#A855F7'] },
            { speed: 0.026, freq: 0.010, amp: 10, phase: 1.8, colors: ['#FF6B35', '#FF1361', '#F59E0B'] },
            { speed: 0.015, freq: 0.005, amp: 8, phase: 3.4, colors: ['#00F5D4', '#00BBF9', '#10B981'] }
        ];

        function animate() {
            ctx.clearRect(0, 0, width, height);
            time += 1;

            waves.forEach((w, wIdx) => {
                ctx.beginPath();
                ctx.moveTo(0, height);

                for (let x = 0; x <= width; x += 8) {
                    const y = (height * 0.55) +
                        Math.sin(x * w.freq + time * w.speed + w.phase) * w.amp +
                        Math.cos(x * w.freq * 0.5 - time * w.speed * 0.7) * (w.amp * 0.35);
                    ctx.lineTo(x, y);
                }

                ctx.lineTo(width, height);
                ctx.closePath();

                const grad = ctx.createLinearGradient(0, 0, width, 0);
                w.colors.forEach((c, idx) => {
                    grad.addColorStop(idx / (w.colors.length - 1), c);
                });

                ctx.fillStyle = grad;
                ctx.globalAlpha = 0.10 + wIdx * 0.05;
                ctx.fill();

                // Luminous top crest line
                ctx.beginPath();
                for (let x = 0; x <= width; x += 8) {
                    const y = (height * 0.55) +
                        Math.sin(x * w.freq + time * w.speed + w.phase) * w.amp +
                        Math.cos(x * w.freq * 0.5 - time * w.speed * 0.7) * (w.amp * 0.35);
                    if (x === 0) ctx.moveTo(x, y);
                    else ctx.lineTo(x, y);
                }
                ctx.strokeStyle = grad;
                ctx.lineWidth = 1.5;
                ctx.globalAlpha = 0.35 + wIdx * 0.15;
                ctx.stroke();
            });

            ctx.globalAlpha = 1;
            requestAnimationFrame(animate);
        }

        animate();
    }

    // 3. Interactive Hero 3-Step Decision Navigator
    function initHeroConsoleNavigator() {
        const stepTabs = document.querySelectorAll('.heroConsoleStepTab');
        const screenPanes = document.querySelectorAll('.screenPane');

        stepTabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const step = tab.getAttribute('data-console-step');

                stepTabs.forEach(t => {
                    t.classList.remove('active');
                    const pill = t.querySelector('.workflowStepPill');
                    if (pill) {
                        pill.textContent = 'Explore';
                        pill.classList.remove('active');
                    }
                });

                tab.classList.add('active');
                const activePill = tab.querySelector('.workflowStepPill');
                if (activePill) {
                    activePill.textContent = 'Active Step';
                    activePill.classList.add('active');
                }

                screenPanes.forEach(pane => {
                    pane.classList.remove('active');
                    if (pane.id === `consolePane${step}`) {
                        pane.classList.add('active');
                    }
                });
            });
        });
    }

    // 4. Interactive Hero AI Sandbox Lever Tester
    function initSandboxLeverTester() {
        const tenureInput = document.getElementById('heroTenureSlider');
        const csatInput = document.getElementById('heroCsatSlider');
        const ticketsInput = document.getElementById('heroTicketsSlider');

        const tenureVal = document.getElementById('heroTenureVal');
        const csatVal = document.getElementById('heroCsatVal');
        const ticketsVal = document.getElementById('heroTicketsVal');

        const gaugeText = document.getElementById('heroGaugeText');
        const gaugeBadge = document.getElementById('heroGaugeBadge');

        function recalculate() {
            if (!tenureInput || !csatInput || !ticketsInput) return;

            const t = parseInt(tenureInput.value, 10);
            const c = parseFloat(csatInput.value);
            const k = parseInt(ticketsInput.value, 10);

            if (tenureVal) tenureVal.textContent = `${t} mo`;
            if (csatVal) csatVal.textContent = `${c}/10`;
            if (ticketsVal) ticketsVal.textContent = `${k}`;

            // Logistic probability calculation
            // Base logits: high satisfaction & tenure reduces risk, high tickets increases risk
            const logit = 1.15 - (0.045 * t) - (0.38 * c) + (0.24 * k);
            const prob = 1 / (1 + Math.exp(-logit));
            const pct = Math.round(prob * 1000) / 10;

            if (gaugeText) {
                gaugeText.textContent = `${pct}%`;
                if (pct < 35) {
                    gaugeText.style.color = '#10B981';
                    if (gaugeBadge) {
                        gaugeBadge.textContent = 'LOW ATTRITION RISK';
                        gaugeBadge.className = 'actionBadgeTriage badgeAutomation';
                    }
                } else if (pct < 65) {
                    gaugeText.style.color = '#F59E0B';
                    if (gaugeBadge) {
                        gaugeBadge.textContent = 'MODERATE ATTRITION RISK';
                        gaugeBadge.className = 'actionBadgeTriage badgeMediumRisk';
                    }
                } else {
                    gaugeText.style.color = '#EF4444';
                    if (gaugeBadge) {
                        gaugeBadge.textContent = 'CRITICAL SLA ATTRITION RISK';
                        gaugeBadge.className = 'actionBadgeTriage badgeHighRisk';
                    }
                }
            }
        }

        [tenureInput, csatInput, ticketsInput].forEach(slider => {
            if (slider) slider.addEventListener('input', recalculate);
        });

        recalculate();
    }

    // 5. Interactive Real-Time ARR & Churn ROI Calculator
    function initRoiCalculator() {
        const arrSlider = document.getElementById('roiArrSlider');
        const churnSlider = document.getElementById('roiChurnSlider');
        const reductionSlider = document.getElementById('roiReductionSlider');

        const arrLabel = document.getElementById('roiArrLabel');
        const churnLabel = document.getElementById('roiChurnLabel');
        const reductionLabel = document.getElementById('roiReductionLabel');

        const outputLost = document.getElementById('roiOutputLost');
        const outputSaved = document.getElementById('roiOutputSaved');
        const output5Year = document.getElementById('roiOutput5Year');
        const outputRoi = document.getElementById('roiOutputRoi');

        function formatCurrency(num) {
            return '$' + Math.round(num).toLocaleString('en-US');
        }

        function updateRoi() {
            if (!arrSlider || !churnSlider || !reductionSlider) return;

            const arr = parseFloat(arrSlider.value);
            const churnRate = parseFloat(churnSlider.value) / 100;
            const reductionRate = parseFloat(reductionSlider.value) / 100;

            if (arrLabel) arrLabel.textContent = formatCurrency(arr);
            if (churnLabel) churnLabel.textContent = `${churnSlider.value}%`;
            if (reductionLabel) reductionLabel.textContent = `${reductionSlider.value}%`;

            const annualLost = arr * churnRate;
            const annualSaved = annualLost * reductionRate;
            // 5-year compounded value with 15% net expansion rate
            const fiveYearVal = annualSaved * 5.85;
            // ROI ratio based on $12,000 baseline enterprise tier
            const estimatedRoiRatio = Math.max(2.5, Math.round((annualSaved / 12000) * 10) / 10);

            if (outputLost) outputLost.textContent = formatCurrency(annualLost) + ' / yr';
            if (outputSaved) outputSaved.textContent = '+' + formatCurrency(annualSaved) + ' / yr';
            if (output5Year) output5Year.textContent = '+' + formatCurrency(fiveYearVal);
            if (outputRoi) outputRoi.textContent = `${estimatedRoiRatio}x ROI`;
        }

        [arrSlider, churnSlider, reductionSlider].forEach(el => {
            if (el) el.addEventListener('input', updateRoi);
        });

        updateRoi();

        // Export Deck Action Handler
        const exportBtn = document.getElementById('roiExportDeckBtn');
        if (exportBtn) {
            exportBtn.addEventListener('click', async () => {
                const originalText = exportBtn.innerHTML;
                exportBtn.disabled = true;
                exportBtn.innerHTML = '<i data-lucide="loader-2" class="lucide-icon spin"></i> Generating Custom Deck...';
                if (window.lucide) window.lucide.createIcons();

                try {
                    const response = await fetch('/api/presentation/generate', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            theme: 'executive',
                            title: 'Qiplo Enterprise Churn & ROI Outlook',
                            include_roster: true,
                            include_business_rules: true
                        })
                    });

                    if (response.ok) {
                        const data = await response.json();
                        showToast('Executive Presentation Deck generated successfully! Redirecting...');
                        setTimeout(() => {
                            window.location.href = '/dashboard#presentation';
                        }, 1200);
                    } else {
                        window.location.href = '/dashboard#presentation';
                    }
                } catch (err) {
                    window.location.href = '/dashboard#presentation';
                } finally {
                    exportBtn.disabled = false;
                    exportBtn.innerHTML = originalText;
                    if (window.lucide) window.lucide.createIcons();
                }
            });
        }
    }

    // 6. Pricing Monthly / Annual Toggle
    function initPricingToggle() {
        const toggleSwitch = document.getElementById('pricingBillingToggle');
        const proPriceVal = document.getElementById('pricingProPrice');
        const proPeriodVal = document.getElementById('pricingProPeriod');

        if (!toggleSwitch || !proPriceVal) return;

        let isAnnual = true;

        toggleSwitch.addEventListener('click', () => {
            isAnnual = !isAnnual;
            toggleSwitch.classList.toggle('active', isAnnual);

            if (isAnnual) {
                proPriceVal.textContent = '$399';
                if (proPeriodVal) proPeriodVal.textContent = '/ month (billed annually)';
            } else {
                proPriceVal.textContent = '$499';
                if (proPeriodVal) proPeriodVal.textContent = '/ month (billed monthly)';
            }
        });
    }

    // 7. FAQ Accordion Handlers
    function initFaqAccordion() {
        const faqItems = document.querySelectorAll('.faqItem');

        faqItems.forEach(item => {
            const btn = item.querySelector('.faqQuestionBtn');
            if (!btn) return;

            btn.addEventListener('click', () => {
                const isOpen = item.classList.contains('open');
                // Close all others
                faqItems.forEach(i => i.classList.remove('open'));
                // Toggle current
                if (!isOpen) {
                    item.classList.add('open');
                }
            });
        });
    }

    // 8. Enterprise Architecture Review Modal
    function initArchitectureModal() {
        const modal = document.getElementById('enterpriseDemoModal');
        const openBtns = document.querySelectorAll('.openEnterpriseModalBtn');
        const closeBtn = document.getElementById('closeEnterpriseModalBtn');
        const form = document.getElementById('enterpriseDemoForm');

        if (!modal) return;

        openBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                modal.classList.add('active');
            });
        });

        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                modal.classList.remove('active');
            });
        }

        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('active');
            }
        });

        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                const emailInput = form.querySelector('input[type="email"]');
                const email = emailInput ? emailInput.value : 'your company';
                modal.classList.remove('active');
                showToast(`Architecture Review scheduled for ${email}! A Senior ML Architect will contact you shortly.`);
                form.reset();
            });
        }
    }

    // 9. Toast Notification Utility
    function showToast(msg) {
        let toast = document.getElementById('landingToast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'landingToast';
            toast.style.cssText = `
                position: fixed;
                bottom: 24px;
                right: 24px;
                background: #1E1B4B;
                color: #FFFFFF;
                border: 1.5px solid #6366F1;
                padding: 14px 22px;
                border-radius: 12px;
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: 0.88rem;
                font-weight: 600;
                box-shadow: 0 10px 30px rgba(0,0,0,0.4), 0 0 15px rgba(99,102,241,0.4);
                z-index: 10000;
                display: flex;
                align-items: center;
                gap: 10px;
                transition: opacity 0.3s ease, transform 0.3s ease;
                opacity: 0;
                transform: translateY(10px);
            `;
            document.body.appendChild(toast);
        }

        toast.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00F5FF" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg> <span>${msg}</span>`;
        toast.style.opacity = '1';
        toast.style.transform = 'translateY(0)';

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(10px)';
        }, 4000);
    }

    // Expose showToast globally
    window.showLandingToast = showToast;

    // Initialization on DOM Ready
    document.addEventListener('DOMContentLoaded', () => {
        initTheme();
        initLandingWaves();
        initHeroConsoleNavigator();
        initSandboxLeverTester();
        initRoiCalculator();
        initPricingToggle();
        initFaqAccordion();
        initArchitectureModal();

        if (window.lucide && typeof window.lucide.createIcons === 'function') {
            window.lucide.createIcons();
        }
    });

})();
