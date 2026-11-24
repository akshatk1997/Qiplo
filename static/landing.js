/**
 * QIPLO — Public Enterprise Landing Page Interactive Controller (v2.8.0)
 * Theme Line: Plus Jakarta Sans / Inter / JetBrains Mono / Living Waves
 * Full Visibility, Live Interactivity, and Innovative Visuals
 */

(function () {
    'use strict';

    // Helper: Safely trigger Lucide icon creation
    function refreshIcons() {
        if (window.lucide && typeof window.lucide.createIcons === 'function') {
            window.lucide.createIcons();
        }
    }

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
        const toggleBtn = document.getElementById('landingThemeToggleBtn');
        if (theme === 'light') {
            document.body.classList.remove('dark-theme');
            document.body.classList.add('light-theme');
            if (toggleBtn) {
                toggleBtn.innerHTML = '<i data-lucide="moon" class="lucide-icon" style="width: 17px; height: 17px;"></i>';
                toggleBtn.title = "Switch to Dark Mode";
            }
        } else {
            document.body.classList.remove('light-theme');
            document.body.classList.add('dark-theme');
            if (toggleBtn) {
                toggleBtn.innerHTML = '<i data-lucide="sun" class="lucide-icon" style="width: 17px; height: 17px;"></i>';
                toggleBtn.title = "Switch to Light Mode";
            }
        }
        refreshIcons();
        if (window.QiploWaves && typeof window.QiploWaves.initHeroWave === 'function') {
            window.QiploWaves.initHeroWave('heroWaveCanvas');
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
                ctx.globalAlpha = 0.12 + wIdx * 0.06;
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
                ctx.lineWidth = 1.6;
                ctx.globalAlpha = 0.40 + wIdx * 0.18;
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
                    t.classList.remove('step-active');
                    const pill = t.querySelector('.workflowStepPill');
                    if (pill) {
                        pill.textContent = 'Explore';
                        pill.classList.remove('active');
                    }
                });

                tab.classList.add('active');
                tab.classList.add('step-active');
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
                refreshIcons();
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

            // Tabular Hybrid Transformer Logit Formula
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

    // 5. Interactive Real-Time ARR & Churn ROI Calculator with Presets
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
            const fiveYearVal = annualSaved * 5.85;
            const estimatedRoiRatio = Math.max(2.5, Math.round((annualSaved / 12000) * 10) / 10);

            if (outputLost) outputLost.textContent = formatCurrency(annualLost) + ' / yr';
            if (outputSaved) outputSaved.textContent = '+' + formatCurrency(annualSaved) + ' / yr';
            if (output5Year) output5Year.textContent = '+' + formatCurrency(fiveYearVal);
            if (outputRoi) outputRoi.textContent = `${estimatedRoiRatio}x ROI`;
        }

        [arrSlider, churnSlider, reductionSlider].forEach(el => {
            if (el) el.addEventListener('input', updateRoi);
        });

        // Preset Handlers
        const presetButtons = document.querySelectorAll('.roiPresetBtn');
        presetButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                presetButtons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                const pArr = parseFloat(btn.getAttribute('data-arr'));
                const pChurn = parseFloat(btn.getAttribute('data-churn'));
                const pRed = parseFloat(btn.getAttribute('data-reduction') || '25');

                if (arrSlider) arrSlider.value = pArr;
                if (churnSlider) churnSlider.value = pChurn;
                if (reductionSlider) reductionSlider.value = pRed;

                updateRoi();
                showToast(`Applied ${btn.textContent.trim()} scenario!`);
            });
        });

        updateRoi();

        // Export Deck Action Handler
        const exportBtn = document.getElementById('roiExportDeckBtn');
        if (exportBtn) {
            exportBtn.addEventListener('click', async () => {
                const originalText = exportBtn.innerHTML;
                exportBtn.disabled = true;
                exportBtn.innerHTML = '<i data-lucide="loader-2" class="lucide-icon spin"></i> Compiling Board Presentation...';
                refreshIcons();

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
                        showToast('Executive Presentation Deck generated successfully! Redirecting...');
                        setTimeout(() => {
                            window.location.href = '/dashboard#presentation';
                        }, 1000);
                    } else {
                        window.location.href = '/dashboard#presentation';
                    }
                } catch (err) {
                    window.location.href = '/dashboard#presentation';
                } finally {
                    exportBtn.disabled = false;
                    exportBtn.innerHTML = originalText;
                    refreshIcons();
                }
            });
        }
    }

    // 6. Innovative Module 1: Interactive Live Cohort Matrix
    function initCohortMatrix() {
        const cohortData = {
            critical: [
                { id: "ACC-904", name: "AcroScale Global", mrr: "$3,400/mo", tenure: "4 mos", risk: "89%", factor: "Payment Delay (3x)", action: "Dispatch Executive SLA" },
                { id: "ACC-812", name: "NexusFin Payments", mrr: "$4,800/mo", tenure: "2 mos", risk: "84%", factor: "CSAT Drop (<4.0)", action: "Assign CS Director" },
                { id: "ACC-774", name: "HyperStack Cloud", mrr: "$2,200/mo", tenure: "6 mos", risk: "78%", factor: "Open Escalations (5)", action: "Offer Renewal Discount" }
            ],
            moderate: [
                { id: "ACC-610", name: "DevPulse Analytics", mrr: "$1,800/mo", tenure: "14 mos", risk: "52%", factor: "Product Usage (-24%)", action: "Schedule Feature Review" },
                { id: "ACC-544", name: "OmniChannel B2B", mrr: "$2,600/mo", tenure: "11 mos", risk: "48%", factor: "Seat De-allocations", action: "Trigger Re-engagement" },
                { id: "ACC-490", name: "LogiTech Systems", mrr: "$1,400/mo", tenure: "16 mos", risk: "42%", factor: "SLA Warning Near", action: "Send Health Survey" }
            ],
            healthy: [
                { id: "ACC-302", name: "CloudFleet Global", mrr: "$8,200/mo", tenure: "36 mos", risk: "8%", factor: "Expansion Eligible", action: "Pitch Enterprise Tier" },
                { id: "ACC-219", name: "CyberMatrix Security", mrr: "$6,500/mo", tenure: "28 mos", risk: "12%", factor: "High Engagement (9.6)", action: "Nominate Case Study" },
                { id: "ACC-108", name: "FinFlow Technologies", mrr: "$5,100/mo", tenure: "42 mos", risk: "6%", factor: "Multi-Year Contract", action: "Maintain VIP Support" }
            ]
        };

        const tabBtns = document.querySelectorAll('.cohortTabBtn');
        const grid = document.getElementById('cohortLiveAccountsGrid');
        if (!grid) return;

        function renderCohort(type) {
            const list = cohortData[type] || cohortData.critical;
            grid.innerHTML = list.map(item => `
                <div class="cohortAccountCard">
                    <div>
                        <div class="accountHeadRow">
                            <span class="accountNameText">${item.name}</span>
                            <span class="accountArrText">${item.mrr}</span>
                        </div>
                        <div class="accountIdText">ID: ${item.id}</div>
                        <div class="accountMetricsRow">
                            <div>Tenure: <strong>${item.tenure}</strong></div>
                            <div>Risk Score: <strong class="accountRiskVal" style="color: ${parseFloat(item.risk) > 60 ? '#EF4444' : (parseFloat(item.risk) > 30 ? '#F59E0B' : '#10B981')};">${item.risk}</strong></div>
                        </div>
                        <div class="accountFactorRow">Primary Factor: <strong class="accountFactorVal">${item.factor}</strong></div>
                    </div>
                    <button type="button" class="accountActionTriggerBtn" onclick="window.triggerAccountAction('${item.name}', '${item.action}')">
                        <i data-lucide="zap" class="lucide-icon" style="width: 14px; height: 14px;"></i>
                        <span>${item.action}</span>
                    </button>
                </div>
            `).join('');
            refreshIcons();
        }

        tabBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                tabBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                const cohortType = btn.getAttribute('data-cohort');
                renderCohort(cohortType);
            });
        });

        renderCohort('critical');
    }

    // Global helper for interactive account action trigger
    window.triggerAccountAction = function (accountName, actionTitle) {
        showToast(`⚡ Action Triggered: "${actionTitle}" for ${accountName}! Synced to Slack & CS Queue.`);
    };

    // 7. Innovative Module 2: Tabular Transformer Attention Visualizer
    function initAttentionVisualizer() {
        const nodes = document.querySelectorAll('.attentionNode');
        const textEl = document.getElementById('attentionExplanationText');
        const factorEl = document.getElementById('attentionFactorName');

        const explanations = {
            payment: "Payment Delays (>2 cycles) exhibited a +34.2% Shapley attribution score. The self-attention head links late payments with support tickets to predict churn 45 days before contract expiration.",
            tickets: "Support Ticket Escalations (3+ critical SLA incidents) showed strong attention correlation with month-to-month contracts. High attention weights flag immediate customer frustration.",
            contract: "Month-to-Month Contracts amplify attrition sensitivity by 3.8x compared to annual agreements. The Transformer models contract duration as a foundational anchor feature.",
            csat: "Customer Satisfaction Scores (<5.0) contribute directly to negative feature embeddings. When paired with high monthly charges, risk classification escalates automatically to Tier 1 Triage.",
            usage: "Usage Velocity Drops (-25% 30-day rolling activity) trigger early warning signals before explicit billing disputes emerge, providing a 60-day window for retention intervention."
        };

        nodes.forEach(node => {
            node.addEventListener('click', () => {
                nodes.forEach(n => n.classList.remove('active'));
                node.classList.add('active');

                const key = node.getAttribute('data-feature');
                if (textEl && explanations[key]) {
                    textEl.textContent = explanations[key];
                }
                if (factorEl) {
                    factorEl.textContent = node.querySelector('.attentionNodeName').textContent;
                }
                refreshIcons();
            });
        });
    }

    // 8. Innovative Module 3: 5-Slide Executive Pitch Deck Live Previewer
    function initDeckPreviewer() {
        const slides = [
            { num: 1, title: "Executive Overview & Attrition Benchmark", summary: "High-level summary of portfolio retention, 250 active cohort accounts, $41.5K monitored ARR, and quarterly risk trajectory." },
            { num: 2, title: "High-Risk Cohort Root-Cause Breakdown", summary: "Drill-down into Tier 1 at-risk contracts, isolating billing discrepancies, unresolved support tickets, and pricing sensitivity." },
            { num: 3, title: "Tabular Transformer Predictive Sensitivity", summary: "Neural self-attention feature interaction curves showing tenure versus satisfaction inflection thresholds." },
            { num: 4, title: "Prescriptive SLA Triage Action Plan", summary: "Operational SLA playbooks, automated CSM task allocations, and immediate commercial incentive recommendations." },
            { num: 5, title: "Financial ARR Recovery & 5-Year Outlook", summary: "Bottom-line ROI model demonstrating +$150K direct revenue preservation and 12.5x return on investment." }
        ];

        let currentIdx = 0;
        const slideNumEl = document.getElementById('deckPreviewSlideNum');
        const slideTitleEl = document.getElementById('deckPreviewSlideTitle');
        const slideDescEl = document.getElementById('deckPreviewSlideDesc');
        const prevBtn = document.getElementById('deckPrevBtn');
        const nextBtn = document.getElementById('deckNextBtn');
        const thumbs = document.querySelectorAll('.deckThumbItem');

        function updateSlide(idx) {
            currentIdx = (idx + slides.length) % slides.length;
            const s = slides[currentIdx];

            if (slideNumEl) slideNumEl.textContent = `Slide 0${s.num} of 05`;
            if (slideTitleEl) slideTitleEl.textContent = s.title;
            if (slideDescEl) slideDescEl.textContent = s.summary;

            thumbs.forEach((t, i) => {
                t.classList.toggle('active', i === currentIdx);
            });
            refreshIcons();
        }

        if (prevBtn) prevBtn.addEventListener('click', () => updateSlide(currentIdx - 1));
        if (nextBtn) nextBtn.addEventListener('click', () => updateSlide(currentIdx + 1));

        thumbs.forEach((thumb, i) => {
            thumb.addEventListener('click', () => updateSlide(i));
        });

        updateSlide(0);
    }

    // 9. Pricing Monthly / Annual Toggle
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

    // 10. FAQ Accordion Handlers
    function initFaqAccordion() {
        const faqItems = document.querySelectorAll('.faqItem');

        faqItems.forEach(item => {
            const btn = item.querySelector('.faqQuestionBtn');
            if (!btn) return;

            btn.addEventListener('click', () => {
                const isOpen = item.classList.contains('open');
                faqItems.forEach(i => i.classList.remove('open'));
                if (!isOpen) {
                    item.classList.add('open');
                }
                refreshIcons();
            });
        });
    }

    // 11. Enterprise Architecture Review Modal
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

    // 12. Toast Notification Utility
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
                box-shadow: 0 10px 30px rgba(0,0,0,0.5), 0 0 18px rgba(99,102,241,0.5);
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

    window.showLandingToast = showToast;

    // Initialization
    function onInit() {
        initTheme();
        initLandingWaves();
        initHeroConsoleNavigator();
        initSandboxLeverTester();
        initRoiCalculator();
        initCohortMatrix();
        initAttentionVisualizer();
        initDeckPreviewer();
        initPricingToggle();
        initFaqAccordion();
        initArchitectureModal();
        refreshIcons();
        if (window.QiploWaves && typeof window.QiploWaves.initHeroWave === 'function') {
            window.QiploWaves.initHeroWave('heroWaveCanvas');
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', onInit);
    } else {
        onInit();
    }

})();
