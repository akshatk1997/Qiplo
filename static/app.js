// Web Audio Synth module disabled by user preference
const AudioFeedback = {
    toggle: () => {},
    isEnabled: () => false,
    click: () => {},
    success: () => {},
    delete: () => {},
    notify: () => {}
};

// Autonomous Self-Healing Fetch Wrapper with Automatic Retry & Exponential Backoff
async function safeFetch(url, options = {}, retries = 3, backoff = 400) {
    const roleSelect = document.getElementById('roleSelect');
    const activeRole = roleSelect ? roleSelect.value : 'manager';
    if (!options.headers) {
        options.headers = {};
    }
    // Handle both headers objects and Headers class
    if (options.headers instanceof Headers) {
        options.headers.set('X-User-Role', activeRole);
    } else {
        options.headers['X-User-Role'] = activeRole;
    }
    for (let i = 0; i < retries; i++) {
        try {
            const res = await fetch(url, options);
            if (res.ok) return res;
            if (res.status >= 500 && i < retries - 1) {
                await new Promise(r => setTimeout(r, backoff * Math.pow(2, i)));
                continue;
            }
            return res;
        } catch (err) {
            if (i < retries - 1) {
                await new Promise(r => setTimeout(r, backoff * Math.pow(2, i)));
                continue;
            }
            throw err;
        }
    }
}

let predictionData = [];
let riskChart;
let signalChart;
let importanceChart;
let cohortTrendChart;
let currentAuthorizedRole = localStorage.getItem('user_role') || 'manager';
let labelMapping = { high_risk: 'high_risk', low_risk: 'low_risk' };
let lastChartsData = null;

function showLoadingSkeletons() {
    const ids = ['metaTotal', 'metaHigh', 'metaLow', 'metaFields', 'simTargetedCount', 'simCampaignCost', 'simSavedRevenue', 'simNetSavedRevenue'];
    ids.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.innerHTML = '<span class="skeleton-loader"></span>';
    });
    const lgIds = ['bizTotalCharges', 'bizExpectedLoss', 'bizRiskExposurePct'];
    lgIds.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.innerHTML = '<span class="skeleton-loader skeleton-loader-lg"></span>';
    });
}

async function loadDashboard() {
    showLoadingSkeletons();
    try {
        const role = document.getElementById('roleSelect').value;
        const apiKey = localStorage.getItem('at_ai_model_key') || localStorage.getItem('show_ai_model_key') || '';
        const t0 = performance.now();
        const response = await safeFetch(`/api/dashboard-state?role=${role}&model_key=${encodeURIComponent(apiKey)}`);
        const payload = await response.json();
        const t1 = performance.now();
        
        const latency = Math.round(t1 - t0);
        const latencyEl = document.getElementById('modelLatency');
        if (latencyEl) {
            latencyEl.textContent = `${latency} ms (Roundtrip)`;
        }

        const summaryData = { summary: payload.summary };
        const predictionsPayload = { predictions: payload.predictions };
        const chartsData = payload.charts;
        const insightsData = payload.insights;
        const aiData = payload.ai_insights;
        const brandingData = payload.branding;

        predictionData = predictionsPayload.predictions || [];
        
        // Render model metrics
        if (payload.model_metrics) {
            const acc = document.getElementById('modelAccuracy');
            const prec = document.getElementById('modelPrecision');
            const rec = document.getElementById('modelRecall');
            const auc = document.getElementById('modelAuc');
            if (acc) acc.textContent = payload.model_metrics.accuracy;
            if (prec) prec.textContent = payload.model_metrics.precision;
            if (rec) rec.textContent = payload.model_metrics.recall;
            if (auc) auc.textContent = payload.model_metrics.auc;

            const tn = document.getElementById('valTN');
            const fp = document.getElementById('valFP');
            const fn = document.getElementById('valFN');
            const tp = document.getElementById('valTP');
            if (tn) tn.textContent = payload.model_metrics.tn !== undefined ? payload.model_metrics.tn : 0;
            if (fp) fp.textContent = payload.model_metrics.fp !== undefined ? payload.model_metrics.fp : 0;
            if (fn) fn.textContent = payload.model_metrics.fn !== undefined ? payload.model_metrics.fn : 0;
            if (tp) tp.textContent = payload.model_metrics.tp !== undefined ? payload.model_metrics.tp : 0;
        }

        const ver = document.getElementById('lblModelVersion');
        const trained = document.getElementById('lblModelLastTrained');
        if (ver && payload.model_version) ver.textContent = payload.model_version;
        if (trained && payload.model_last_trained) trained.textContent = payload.model_last_trained;
        labelMapping = brandingData.label_mapping || { high_risk: 'high_risk', low_risk: 'low_risk' };

        const riskFilter = document.getElementById('riskFilter');
        if (riskFilter) {
            const currentVal = riskFilter.value;
            const highLabel = labelMapping.high_risk.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
            const lowLabel = labelMapping.low_risk.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
            riskFilter.innerHTML = `
                <option value="all">All risks</option>
                <option value="${labelMapping.high_risk}">${highLabel}</option>
                <option value="${labelMapping.low_risk}">${lowLabel}</option>
            `;
            if (currentVal && (currentVal === 'all' || currentVal === labelMapping.high_risk || currentVal === labelMapping.low_risk)) {
                riskFilter.value = currentVal;
            } else {
                riskFilter.value = 'all';
            }
        }

        const company = document.getElementById('companyNameInput').value || brandingData.company_name || 'Qiplo Analytics';
        document.getElementById('brandTitle').textContent = company;
        
        const demoBadge = document.getElementById('demoBadge');
        if (demoBadge) {
            demoBadge.style.display = payload.is_demo ? 'inline-block' : 'none';
        }

        renderSourceMeta();
        renderRows();
        lastChartsData = chartsData;
        renderCharts(chartsData, payload.feature_importance);
        renderInsights(insightsData);
        renderExecutiveSummary(insightsData);
        renderAiPanel(aiData);
        
        // Relational CSM assignments & campaign loaders
        await loadEnterpriseFeatures();
        applyRolePermissions(role);
        
        // NotebookLM sidebars refresh
        await fetchSources();
        await fetchNotes();
        await loadBusinessAnalytics();
    } catch (error) {
        console.error('Dashboard load failed', error);
    }
}

function renderSourceMeta() {
    const total = predictionData.length;
    const highRisk = predictionData.filter(item => item.prediction_label === labelMapping.high_risk).length;
    const fields = Array.from(new Set(predictionData.flatMap(item => Object.keys(item)))).sort();

    document.getElementById('metaTotal').textContent = total;
    document.getElementById('metaHigh').textContent = highRisk;
    document.getElementById('metaLow').textContent = total - highRisk;
    document.getElementById('metaFields').textContent = fields.length || '—';
}

function renderAiPanel(aiData) {
    document.getElementById('aiHeadline').textContent = aiData.headline || 'Awaiting analysis';
    document.getElementById('aiNarrative').textContent = aiData.narrative || '';
    const segments = aiData.segments || [];
    document.getElementById('aiSegments').innerHTML = segments.length
        ? segments.map(s => `<div class="aiSegment"><h4>${s.title}</h4><p>${s.detail}</p></div>`).join('')
        : '';
}

const INTERNAL_COLUMNS = new Set(['predicted_probability', 'prediction_label', 'created_at', 'churned']);

function dynamicColumns() {
    const idCol = predictionData.some(r => r.customer_id !== undefined && r.customer_id !== null)
        ? 'customer_id'
        : (predictionData.some(r => r.id !== undefined) ? 'id' : null);

    const extra = [];
    if (predictionData.length) {
        for (const key of Object.keys(predictionData[0])) {
            if (key === idCol || INTERNAL_COLUMNS.has(key)) continue;
            const vals = predictionData.slice(0, 50).map(r => r[key]);
            const nonEmpty = vals.filter(v => v !== null && v !== undefined && v !== '');
            if (!nonEmpty.length) continue;
            extra.push(key);
            if (extra.length >= 7) break;
        }
    }
    return { idCol, extra };
}

function renderRows() {
    const filterValue = document.getElementById('riskFilter').value;
    const table = document.getElementById('predictionTable');
    const rows = document.getElementById('predictionRows');
    if (!table || !rows) return;

    const { idCol, extra } = dynamicColumns();
    const headers = ['Customer', 'Risk', 'Probability', ...extra.map(c => c.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()))];

    let thead = table.querySelector('thead');
    if (!thead) {
        thead = document.createElement('thead');
        table.appendChild(thead);
    }
    thead.innerHTML = `<tr>${headers.map(h => `<th>${h}</th>`).join('')}</tr>`;
    rows.innerHTML = '';

    const searchInput = document.getElementById('customerSearchInput');
    const searchTerm = searchInput ? searchInput.value.toLowerCase().trim() : '';

    let filtered = filterValue === 'all'
        ? predictionData
        : predictionData.filter(item => item.prediction_label === filterValue);

    if (searchTerm) {
        filtered = filtered.filter(item => {
            const idVal = idCol ? String(item[idCol]) : String(item.customer_id);
            return idVal.toLowerCase().includes(searchTerm);
        });
    }

    if (!filtered.length) {
        rows.innerHTML = `<tr><td colspan="${headers.length}" class="empty">No records to display yet. Upload a file to begin.</td></tr>`;
        return;
    }

    const cell = (value) => value === null || value === undefined || value === '' ? 'n/a' : value;
    filtered.forEach(item => {
        const probabilityVal = Number(item.predicted_probability || 0);
        const probability = probabilityVal.toFixed(3);
        let ciText = '';
        if (item.ci_lower !== undefined && item.ci_upper !== undefined) {
            const l = Number(item.ci_lower).toFixed(3);
            const u = Number(item.ci_upper).toFixed(3);
            ciText = `<br><span style="font-size: 0.68rem; color: var(--muted); font-family: 'JetBrains Mono', monospace; font-weight: 500;">[${l}, ${u}]</span>`;
        }
        const labelClass = item.prediction_label === labelMapping.high_risk ? 'high' : 'low';
        const idVal = idCol ? cell(item[idCol]) : cell(item.customer_id);

        let assignInfo = '';
        if (window.csmAssignments && window.csmAssignments[idVal]) {
            const assignment = window.csmAssignments[idVal];
            const badgeMap = {
                'unassigned': 'rgba(100, 116, 139, 0.1)',
                'contacted': 'rgba(59, 130, 246, 0.1)',
                'in progress': 'rgba(234, 179, 8, 0.1)',
                'resolved': 'rgba(34, 197, 94, 0.1)'
            };
            const colorMap = {
                'unassigned': 'var(--muted)',
                'contacted': '#3b82f6',
                'in progress': 'var(--warning)',
                'resolved': 'var(--success)'
            };
            assignInfo = `
                <div style="font-size: 0.72rem; color: var(--muted); margin-top: 4px; display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
                    <span style="background: ${badgeMap[assignment.status] || 'rgba(100,116,139,0.1)'}; color: ${colorMap[assignment.status] || 'var(--muted)'}; padding: 1px 6px; border-radius: 4px; font-weight: 700; font-size: 0.65rem; text-transform: uppercase;">
                        ${assignment.status}
                    </span>
                    <span>CSM: <strong>${assignment.csm_name || 'Unassigned'}</strong></span>
                </div>
            `;
        }

        let driversHtml = '';
        if (item.risk_drivers) {
            try {
                const drivers = typeof item.risk_drivers === 'string' ? JSON.parse(item.risk_drivers) : item.risk_drivers;
                if (drivers && drivers.length) {
                    driversHtml = `
                        <div class="risk-drivers-list" style="font-size: 0.7rem; color: #ff007f; margin-top: 6px; display: flex; align-items: center; gap: 4px; flex-wrap: wrap;">
                            <span style="font-weight: 700; text-transform: uppercase; font-size: 0.65rem; color: var(--muted);">Drivers:</span>
                            ${drivers.map(d => `<span style="background: rgba(255, 0, 127, 0.08); border: 1px solid rgba(255, 0, 127, 0.15); padding: 1px 6px; border-radius: 4px; color: #ff007f; font-weight: 500;">${d}</span>`).join('')}
                        </div>
                    `;
                }
            } catch (e) {
                // Ignore parse errors
            }
        }

        const tds = [`<td><div><strong>${idVal}</strong></div>${assignInfo}${driversHtml}</td>`,
            `<td><span class="badge ${labelClass}">${item.prediction_label.replace('_', ' ')}</span></td>`,
            `<td><div><strong>${probability}</strong></div>${ciText}</td>`,
            ...extra.map(c => `<td>${cell(item[c])}</td>`)].join('');

        const row = document.createElement('tr');
        row.innerHTML = tds;
        rows.appendChild(row);
    });
}

function renderCharts(chartPayload, featureImportance) {
    const riskLabels = (chartPayload.charts || []).map(item => item.label);
    const riskValues = (chartPayload.charts || []).map(item => item.value);
    const signalLabels = (chartPayload.signals || []).map(item => item.label);
    const signalValues = (chartPayload.signals || []).map(item => item.value);

    if (riskChart) riskChart.destroy();
    if (signalChart) signalChart.destroy();
    if (importanceChart) importanceChart.destroy();

    const bodyStyles = getComputedStyle(document.body);
    const labelColor = bodyStyles.getPropertyValue('--muted').trim() || '#475467';
    const gridColor = bodyStyles.getPropertyValue('--border').trim() || 'rgba(16, 24, 40, 0.08)';

    riskChart = new Chart(document.getElementById('riskChart'), {
        type: 'doughnut',
        data: {
            labels: riskLabels.length ? riskLabels : ['No data'],
            datasets: [{ data: riskValues.length ? riskValues : [1], backgroundColor: ['#FF007F', '#00F5FF', '#FFE600'] }]
        },
        options: { responsive: true, maintainAspectRatio: false, cutout: '62%', plugins: { legend: { labels: { color: labelColor } } } }
    });

    signalChart = new Chart(document.getElementById('signalChart'), {
        type: 'bar',
        data: {
            labels: signalLabels.length ? signalLabels : ['No retention signals'],
            datasets: [{ label: 'Customers', data: signalValues.length ? signalValues : [0], backgroundColor: ['#00F5FF', '#FF007F', '#FFE600', '#39FF14'] }]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { beginAtZero: true, ticks: { color: labelColor }, grid: { color: gridColor } },
                x: { ticks: { color: labelColor }, grid: { color: gridColor } }
            }
        }
    });

    const sortedFeatures = Object.entries(featureImportance || {})
        .sort((a, b) => b[1] - a[1]);
        
    const importanceLabels = sortedFeatures.map(item => item[0]);
    const importanceValues = sortedFeatures.map(item => item[1]);

    importanceChart = new Chart(document.getElementById('importanceChart'), {
        type: 'bar',
        data: {
            labels: importanceLabels.length ? importanceLabels : ['No metrics'],
            datasets: [{ label: 'Feature weight', data: importanceValues.length ? importanceValues : [0], backgroundColor: '#FF007F' }]
        },
        options: {
            indexAxis: 'y',
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { beginAtZero: true, max: 1.0, ticks: { color: labelColor }, grid: { color: gridColor } },
                y: { ticks: { color: labelColor }, grid: { color: gridColor } }
            }
        }
    });
}

function renderExecutiveSummary(insightsData) {
    const highRisk = predictionData.filter(item => item.prediction_label === labelMapping.high_risk).length;
    const lowRisk = predictionData.length - highRisk;
    const avgProbability = predictionData.length
        ? (predictionData.reduce((acc, item) => acc + Number(item.predicted_probability || 0), 0) / predictionData.length).toFixed(3)
        : '0.000';
    const actions = (insightsData.recommendations || []).length;

    document.getElementById('executiveSummary').innerHTML = `
        <div><strong>Risk mix</strong><p>${highRisk} high / ${lowRisk} low</p></div>
        <div><strong>Avg churn probability</strong><p>${avgProbability}</p></div>
        <div><strong>AI recommendations</strong><p>${actions} prioritized actions</p></div>
    `;
}

function renderAnalyzedTips(role) {
    const tipsPanel = document.getElementById('analyzedTipsPanel');
    if (!tipsPanel) return;

    if (!predictionData || !predictionData.length) {
        tipsPanel.innerHTML = '<p style="color: var(--muted); font-size: 0.88rem; margin: 0; text-align: center;">Upload customer data to see real-time diagnostics.</p>';
        return;
    }

    const highRiskLabel = labelMapping.high_risk;
    const highRiskCustomers = predictionData.filter(item => item.prediction_label === highRiskLabel);
    const totalHighRisk = highRiskCustomers.length;

    const totalChargesAtRisk = highRiskCustomers.reduce((sum, item) => {
        const val = item.monthly_charges !== undefined && item.monthly_charges !== null ? Number(item.monthly_charges) : 100;
        return sum + val;
    }, 0) * currentCurrencyRate;

    const ticketHeavyCount = highRiskCustomers.filter(item => {
        const tickets = item.support_tickets !== undefined && item.support_tickets !== null ? Number(item.support_tickets) : 0;
        return tickets >= 3;
    }).length;

    const avgHighProb = totalHighRisk
        ? (highRiskCustomers.reduce((sum, item) => sum + Number(item.predicted_probability || 0), 0) / totalHighRisk * 100).toFixed(1)
        : '0.0';

    const lowSatsCount = highRiskCustomers.filter(item => {
        const csat = item.customer_satisfaction_score !== undefined && item.customer_satisfaction_score !== null ? Number(item.customer_satisfaction_score) : 5;
        return csat <= 2;
    }).length;
    const lowSatsPct = totalHighRisk ? Math.round((lowSatsCount / totalHighRisk) * 100) : 0;

    const projectedGrossSaved = totalChargesAtRisk * 0.40;
    const projectedCost = totalChargesAtRisk * 0.20;
    const projectedNetSaved = Math.max(0, projectedGrossSaved - projectedCost);

    let tipsHtml = '';

    if (role === 'executive') {
        tipsHtml = `
            <div style="background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 12px; border-left: 4px solid var(--accent-2);">
                <p style="margin: 0 0 4px; font-size: 0.88rem; font-weight: 700; color: var(--text);">💰 Financial Exposure Alert</p>
                <p style="margin: 0; font-size: 0.8rem; color: var(--muted); line-height: 1.45;">
                    Churn risk is threatening a total of <strong>${currentCurrencySymbol}${Math.round(totalChargesAtRisk).toLocaleString()}</strong> in active monthly recurring contract value. Recommending executive funding allocation of targeted loyalty discounts to protect key accounts.
                </p>
            </div>
            <div style="background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 12px; border-left: 4px solid var(--danger);">
                <p style="margin: 0 0 4px; font-size: 0.88rem; font-weight: 700; color: var(--text);">⚡ Service Level Deficiencies</p>
                <p style="margin: 0; font-size: 0.8rem; color: var(--muted); line-height: 1.45;">
                    Approximately <strong>${lowSatsPct}%</strong> of high-risk customers show low satisfaction ratings (CSAT &le; 2.0). Directing engineering and product heads to address systemic service gaps is critical.
                </p>
            </div>
        `;
    } else if (role === 'sales') {
        tipsHtml = `
            <div style="background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 12px; border-left: 4px solid var(--success);">
                <p style="margin: 0 0 4px; font-size: 0.88rem; font-weight: 700; color: var(--text);">📈 Proactive Renewal Strategy</p>
                <p style="margin: 0; font-size: 0.8rem; color: var(--muted); line-height: 1.45;">
                    Targeting the <strong>${totalHighRisk}</strong> high-risk customers with proactive contract extension plans is estimated to save a net monthly contract value of <strong>${currentCurrencySymbol}${Math.round(projectedNetSaved).toLocaleString()}</strong>.
                </p>
            </div>
            <div style="background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 12px; border-left: 4px solid var(--warning);">
                <p style="margin: 0 0 4px; font-size: 0.88rem; font-weight: 700; color: var(--text);">⏳ Billing Configuration Threat</p>
                <p style="margin: 0; font-size: 0.8rem; color: var(--muted); line-height: 1.45;">
                    Month-to-month billing segments constitute the highest risk cohort. Pitch annual pricing pre-payments during CSM outreach to lock in long-term commitments.
                </p>
            </div>
        `;
    } else if (role === 'support') {
        tipsHtml = `
            <div style="background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 12px; border-left: 4px solid var(--danger);">
                <p style="margin: 0 0 4px; font-size: 0.88rem; font-weight: 700; color: var(--text);">🔧 Urgent Ticket Backlogs</p>
                <p style="margin: 0; font-size: 0.8rem; color: var(--muted); line-height: 1.45;">
                    There are <strong>${ticketHeavyCount}</strong> high-risk accounts with 3+ unresolved support tickets. Assigning senior engineers to close these tickets immediately is recommended to prevent support-related churn.
                </p>
            </div>
            <div style="background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 12px; border-left: 4px solid var(--accent);">
                <p style="margin: 0 0 4px; font-size: 0.88rem; font-weight: 700; color: var(--text);">💬 CSAT Recovery Protocols</p>
                <p style="margin: 0; font-size: 0.8rem; color: var(--muted); line-height: 1.45;">
                    High-risk customers exhibit an average churn probability of <strong>${avgHighProb}%</strong>. Support management should execute direct outbound recovery campaigns for low-rating accounts.
                </p>
            </div>
        `;
    } else {
        tipsHtml = `
            <div style="background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 12px; border-left: 4px solid var(--accent-2);">
                <p style="margin: 0 0 4px; font-size: 0.88rem; font-weight: 700; color: var(--text);">📋 CSM Assignment Balance</p>
                <p style="margin: 0; font-size: 0.8rem; color: var(--muted); line-height: 1.45;">
                    CSM workload for high-risk accounts is currently active. Recommend distributing assignments evenly to avoid response delays.
                </p>
            </div>
            <div style="background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 12px; border-left: 4px solid var(--success);">
                <p style="margin: 0 0 4px; font-size: 0.88rem; font-weight: 700; color: var(--text);">🔔 Webhook Notifications Fired</p>
                <p style="margin: 0; font-size: 0.8rem; color: var(--muted); line-height: 1.45;">
                    Live Slack and Microsoft Teams SLA high-risk alerts have been configured. Ensure CSMs perform standard 24-hour outreach audits.
                </p>
            </div>
        `;
    }

    tipsPanel.innerHTML = tipsHtml;
    if (window.lucide) lucide.createIcons();
}

function renderInsights(insightsData) {
    const panel = document.getElementById('insightPanel');
    const recommendations = insightsData.recommendations || [];
    panel.innerHTML = recommendations.length
        ? recommendations.map(item => `<p>${item}</p>`).join('')
        : '<p>No insights available yet.</p>';

    const role = document.getElementById('roleSelect').value;
    renderAnalyzedTips(role);
}

async function uploadFile(fileOverride) {
    const fileInput = document.getElementById('fileInput');
    const status = document.getElementById('uploadStatus');

    const file = fileOverride instanceof File ? fileOverride : (fileInput && fileInput.files[0]);

    if (!file) {
        if (status) {
            status.textContent = 'Please choose a file first.';
            status.className = 'status error';
        }
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    if (status) {
        status.textContent = `Uploading "${file.name}"...`;
        status.className = 'status';
    }

    try {
        const response = await fetch('/api/upload', { method: 'POST', body: formData });
        const payload = await response.json();
        if (response.ok && payload.status === 'ok') {
            AudioFeedback.success();
            if (status) {
                status.textContent = `Source added: ${payload.rows} customer records analyzed.`;
                status.className = 'status success';
            }
            
            const feedbackEl = document.getElementById('uploadValidationFeedback');
            if (feedbackEl) {
                if (payload.warnings && payload.warnings.length) {
                    feedbackEl.style.display = 'block';
                    feedbackEl.style.color = 'var(--warning)';
                    feedbackEl.style.borderColor = 'rgba(234, 179, 8, 0.3)';
                    feedbackEl.style.background = 'rgba(234, 179, 8, 0.08)';
                    feedbackEl.innerHTML = `
                        <div style="font-weight: 700; margin-bottom: 6px; display: flex; align-items: center; gap: 4px;">
                            <i data-lucide="alert-triangle" style="width: 14px; height: 14px;"></i>
                            Data Validation Logs:
                        </div>
                        <ul style="margin: 0; padding-left: 16px;">
                            ${payload.warnings.map(w => `<li style="margin-bottom: 4px;">${w}</li>`).join('')}
                        </ul>
                    `;
                } else {
                    feedbackEl.style.display = 'block';
                    feedbackEl.style.color = 'var(--success)';
                    feedbackEl.style.borderColor = 'rgba(34, 197, 94, 0.3)';
                    feedbackEl.style.background = 'rgba(34, 197, 94, 0.08)';
                    feedbackEl.innerHTML = `
                        <div style="font-weight: 700; display: flex; align-items: center; gap: 4px;">
                            <i data-lucide="check-circle" style="width: 14px; height: 14px;"></i>
                            Data Validation Passed: Column types & schemas are 100% correct.
                        </div>
                    `;
                }
                if (window.lucide) window.lucide.createIcons();
            }

            try {
                await safeFetch('/api/demo/set-mode', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ mode: 'custom' })
                });
            } catch (err) {
                console.error('Failed to set custom mode on upload:', err);
            }

            const toggleDemoBtn = document.getElementById('toggleDemoBtn');
            const toggleCustomBtn = document.getElementById('toggleCustomBtn');
            if (toggleDemoBtn && toggleCustomBtn) {
                toggleDemoBtn.classList.remove('active');
                toggleCustomBtn.classList.add('active');
            }
            await loadDashboard();
            await fetchSources();
        } else {
            if (status) {
                status.textContent = payload.message || 'Upload failed. Please try again.';
                status.className = 'status error';
            }
            const feedbackEl = document.getElementById('uploadValidationFeedback');
            if (feedbackEl) {
                feedbackEl.style.display = 'block';
                feedbackEl.style.color = 'var(--danger)';
                feedbackEl.style.borderColor = 'rgba(239, 68, 68, 0.3)';
                feedbackEl.style.background = 'rgba(239, 68, 68, 0.08)';
                feedbackEl.innerHTML = `
                    <div style="font-weight: 700; display: flex; align-items: center; gap: 4px;">
                        <i data-lucide="x-circle" style="width: 14px; height: 14px;"></i>
                        Schema Error: ${payload.message || 'Upload failed.'}
                    </div>
                `;
                if (window.lucide) window.lucide.createIcons();
            }
        }
    } catch (error) {
        if (status) {
            status.textContent = 'Upload failed. Please check connection.';
            status.className = 'status error';
        }
    } finally {
        if (fileInput) fileInput.value = '';
    }
}

function setupDragAndDrop() {
    const pane = document.querySelector('.sourcesPane');
    if (!pane) return;

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        pane.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
        }, false);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        pane.addEventListener(eventName, () => {
            pane.classList.add('dragHighlight');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        pane.addEventListener(eventName, () => {
            pane.classList.remove('dragHighlight');
        }, false);
    });

    pane.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files && files.length) {
            uploadFile(files[0]);
        }
    }, false);
}

function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

function setupTabs() {
    const routeMap = {
        '/dashboard': 'overview',
        '/actions': 'actions',
        '/business': 'business',
        '/presentation': 'presentation',
        '/guide': 'guide'
    };
    const currentPath = window.location.pathname;
    const initialTab = routeMap[currentPath] || localStorage.getItem('active_tab') || 'overview';

    document.querySelectorAll('.tab').forEach(tab => {
        const isTarget = tab.dataset.tab === initialTab;
        tab.classList.toggle('active', isTarget);
        const tabBody = document.getElementById(`tab-${tab.dataset.tab}`);
        if (tabBody) {
            tabBody.classList.toggle('hidden', !isTarget);
        }
        tab.addEventListener('click', () => {
            AudioFeedback.click();
            const target = tab.dataset.tab;
            localStorage.setItem('active_tab', target);
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tabBody').forEach(b => b.classList.add('hidden'));
            tab.classList.add('active');
            const targetBody = document.getElementById(`tab-${target}`);
            if (targetBody) targetBody.classList.remove('hidden');
            
            const routeMapInverse = {
                'overview': '/dashboard',
                'actions': '/actions',
                'business': '/business',
                'presentation': '/presentation',
                'guide': '/guide'
            };
            const routePath = routeMapInverse[target] || '/';
            window.history.pushState(null, '', routePath);
        });
    });
}

// Theme toggle removed - Dark theme default with Fire & Lightning colors

const toggleSoundBtn = document.getElementById('toggleSoundBtn');
if (toggleSoundBtn) {
    const soundEnabled = localStorage.getItem('sound_enabled') !== 'false';
    AudioFeedback.toggle(soundEnabled);
    toggleSoundBtn.textContent = soundEnabled ? '🔊' : '🔇';
    toggleSoundBtn.title = soundEnabled ? 'Disable Sound Feedback' : 'Enable Sound Feedback';

    toggleSoundBtn.addEventListener('click', () => {
        const currentlyEnabled = AudioFeedback.isEnabled();
        AudioFeedback.toggle(!currentlyEnabled);
        localStorage.setItem('sound_enabled', !currentlyEnabled);
        toggleSoundBtn.textContent = currentlyEnabled ? '🔇' : '🔊';
        toggleSoundBtn.title = currentlyEnabled ? 'Enable Sound Feedback' : 'Disable Sound Feedback';
        if (!currentlyEnabled) {
            AudioFeedback.click();
        }
    });
}

// User-interaction initialization triggers AudioContext activation
document.addEventListener('click', () => {
    // Soft click feedback activates AudioContext gracefully
    AudioFeedback.click();
}, { once: true });

document.getElementById('addSourceBtn').addEventListener('click', () => {
    AudioFeedback.click();
    document.getElementById('fileInput').click();
});
document.getElementById('fileInput').addEventListener('change', () => uploadFile());
setupDragAndDrop();
document.getElementById('riskFilter').addEventListener('change', renderRows);
const custSearch = document.getElementById('customerSearchInput');
if (custSearch) {
    custSearch.addEventListener('input', renderRows);
}
document.getElementById('roleSelect').addEventListener('change', async (e) => {
    const rs = document.getElementById('roleSelect');
    const targetRole = rs.value;
    if (targetRole === currentAuthorizedRole) return;

    const codes = {
        executive: 'executive123',
        manager: 'manager123',
        sales: 'sales123',
        support: 'support123'
    };

    const code = prompt(`Enter passcode to authorize [${targetRole.toUpperCase()}] access:`);
    if (code === codes[targetRole]) {
        currentAuthorizedRole = targetRole;
        localStorage.setItem('user_role', targetRole);
        await loadDashboard();
    } else {
        alert('Access Denied: Incorrect passcode entered.');
        rs.value = currentAuthorizedRole;
    }
});
document.getElementById('exportTableauBtn').addEventListener('click', () => {
    window.open('/api/export/tableau', '_blank');
});
document.getElementById('exportPowerBiBtn').addEventListener('click', () => {
    window.open('/api/export/powerbi', '_blank');
});
document.getElementById('exportExcelBtn').addEventListener('click', () => {
    if (!predictionData || !predictionData.length) {
        alert("No prediction data available to export. Please upload a customer file first.");
        return;
    }
    window.open('/api/export/excel', '_blank');
});
document.getElementById('exportReportBtn').addEventListener('click', () => {
    if (!predictionData || !predictionData.length) {
        alert("No prediction data available to analyze. Please upload a customer file first.");
        return;
    }
    const company = encodeURIComponent(document.getElementById('companyNameInput').value.trim() || '');
    const currencySelect = document.getElementById('currencySelect');
    const currency = currencySelect ? encodeURIComponent(currencySelect.value) : 'USD';
    window.open(`/api/export/report?company=${company}&currency=${currency}`, '_blank');
});
document.getElementById('exportPdfBtn').addEventListener('click', () => {
    if (!predictionData || !predictionData.length) {
        alert("No prediction data available to export. Please upload a customer file first.");
        return;
    }
    const company = encodeURIComponent(document.getElementById('companyNameInput').value.trim() || '');
    const currencySelect = document.getElementById('currencySelect');
    const currency = currencySelect ? encodeURIComponent(currencySelect.value) : 'USD';
    window.open(`/api/export/report?company=${company}&currency=${currency}`, '_blank');
});
document.getElementById('companyNameInput').addEventListener('input', debounce(() => {
    const name = document.getElementById('companyNameInput').value.trim();
    if (name) document.getElementById('brandTitle').textContent = name;
}, 300));

function animateLogo() {
    const el = document.getElementById('logoChar');
    if (!el) return;
    const glyphs = ['R', 'A', 'I', '◷', '⬡', '✦', '◉'];
    let i = Math.floor(Math.random() * glyphs.length);
    el.textContent = glyphs[i];
    setInterval(() => {
        i = (i + 1) % glyphs.length;
        el.textContent = glyphs[i];
    }, 2500);
}

setupTabs();
animateLogo();
loadDashboard();

// AI Copilot Integration
let chatHistory = [];

function setupCopilot() {
    const storedKey = localStorage.getItem('at_ai_model_key') || localStorage.getItem('show_ai_model_key') || '';
    const keyInput = document.getElementById('geminiApiKeyInput');
    if (keyInput) {
        keyInput.value = storedKey;
        keyInput.addEventListener('input', (e) => {
            localStorage.setItem('at_ai_model_key', e.target.value.trim());
            loadDashboard();
        });
    }

    const chatForm = document.getElementById('chatForm');
    if (chatForm) {
        chatForm.addEventListener('submit', handleChatMessage);
    }

    const suggestionChips = document.getElementById('suggestionChips');
    if (suggestionChips) {
        suggestionChips.querySelectorAll('.chip').forEach(chip => {
            chip.addEventListener('click', () => {
                const input = document.getElementById('chatInput');
                if (input) {
                    input.value = chip.textContent;
                    handleChatMessage();
                }
            });
        });
    }

    // Initialize Business Hub, Presentation, and Notes
    setupBusinessHub();
    setupPresentation();
    const createNoteBtn = document.getElementById('createNoteBtn');
    if (createNoteBtn) {
        createNoteBtn.addEventListener('click', createNote);
    }
}

async function handleChatMessage(event) {
    if (event) event.preventDefault();

    const input = document.getElementById('chatInput');
    if (!input) return;
    const text = input.value.trim();
    if (!text) return;

    input.value = '';
    appendMessage('user', text);

    const chatSendButton = document.getElementById('chatSendButton');
    if (chatSendButton) chatSendButton.disabled = true;

    const loadingId = appendMessage('bot', 'Thinking...');

    try {
        const apiKey = localStorage.getItem('at_ai_model_key') || localStorage.getItem('show_ai_model_key') || '';
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: text,
                history: chatHistory,
                model_key: apiKey
            })
        });

        const payload = await response.json();
        removeMessage(loadingId);

        if (response.ok && payload.response) {
            appendMessage('bot', payload.response, true);
            chatHistory.push({ role: 'user', text: text });
            chatHistory.push({ role: 'model', text: payload.response });
            if (chatHistory.length > 20) {
                chatHistory.shift();
                chatHistory.shift();
            }
        } else {
            appendMessage('bot', payload.error || payload.response || 'An error occurred. Please try again.');
        }
    } catch (error) {
        removeMessage(loadingId);
        appendMessage('bot', 'Could not reach server. Please check your connection.');
    } finally {
        if (chatSendButton) chatSendButton.disabled = false;
    }
}

function appendMessage(role, text, isMarkdown = false) {
    const messagesContainer = document.getElementById('chatMessages');
    if (!messagesContainer) return null;

    if (role === 'bot' && text !== 'Thinking...') {
        AudioFeedback.notify();
    } else if (role === 'user') {
        AudioFeedback.click();
    }

    const msgDiv = document.createElement('div');
    msgDiv.className = `msg ${role}`;
    const msgId = 'msg-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
    msgDiv.id = msgId;

    if (isMarkdown && typeof marked !== 'undefined') {
        let parsed = marked.parse(text);
        parsed = parsed.replace(/\[((?:C|U|N)\d+)\]/g, '<span class="citation-badge" onclick="highlightCustomer(\'$1\')">[$1]</span>');
        msgDiv.innerHTML = parsed;
    } else {
        let parsed = text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        parsed = parsed.replace(/\[((?:C|U|N)\d+)\]/g, '<span class="citation-badge" onclick="highlightCustomer(\'$1\')">[$1]</span>');
        msgDiv.innerHTML = parsed;
    }

    messagesContainer.appendChild(msgDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    return msgId;
}

function removeMessage(id) {
    const msg = document.getElementById(id);
    if (msg) msg.remove();
}

// NotebookLM Extensions

// 1. Sources Management
async function fetchSources() {
    try {
        const res = await fetch('/api/sources');
        const data = await res.json();
        renderSourcesList(data.sources || []);
    } catch (e) {
        console.error("Failed to fetch sources", e);
    }
}

function renderSourcesList(sources) {
    const container = document.getElementById('sourcesList');
    if (!container) return;
    if (!sources.length) {
        container.innerHTML = '<p class="emptyHint" onclick="document.getElementById(\'fileInput\').click()" style="cursor:pointer;" title="Click to upload customer file">No source documents loaded yet. <span style="color:var(--accent-2); text-decoration:underline;">Click + Add or drop file</span> to begin.</p>';
        return;
    }
    
    container.innerHTML = sources.map(src => {
        const activeClass = src.is_active ? 'active' : '';
        const checked = src.is_active ? 'checked' : '';
        return `
            <div class="sourceItem ${activeClass}" data-id="${src.source_id}">
                <div class="sourceItemLeft">
                    <input type="checkbox" class="sourceCheckbox" ${checked} onchange="toggleSource('${src.source_id}', this.checked)" />
                    <span class="sourceName" title="${src.filename}">${src.filename}</span>
                </div>
                <div class="sourceItemRight">
                    <span class="sourceRows">${src.row_count} rows</span>
                    <button class="deleteSourceBtn" onclick="deleteSource('${src.source_id}', event)" title="Delete source">&times;</button>
                </div>
            </div>
        `;
    }).join('');
}

async function toggleSource(sourceId, isChecked) {
    try {
        const res = await fetch('/api/sources/toggle', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ source_id: sourceId, is_active: isChecked ? 1 : 0 })
        });
        if (res.ok) {
            await loadDashboard();
        }
    } catch (e) {
        console.error("Failed to toggle source", e);
    }
}
window.toggleSource = toggleSource;

async function deleteSource(sourceId, event) {
    if (event) {
        event.stopPropagation();
        event.preventDefault();
    }
    if (!confirm("Are you sure you want to delete this source? This will remove all associated customer records.")) return;

    const safeId = window.CSS && CSS.escape ? CSS.escape(sourceId) : sourceId;
    const sourceEl = document.querySelector(`.sourceItem[data-id="${safeId}"]`);
    if (sourceEl) {
        sourceEl.style.opacity = '0.3';
        sourceEl.style.pointerEvents = 'none';
    }

    try {
        const res = await fetch(`/api/sources/${encodeURIComponent(sourceId)}`, { method: 'DELETE' });
        if (res.ok) {
            AudioFeedback.delete();
            
            // Check if any custom sources are left
            const sourcesRes = await fetch('/api/sources');
            const sourcesData = await sourcesRes.json();
            const remainingCustom = (sourcesData.sources || []).filter(src => src.source_id !== 'sample_data');
            
            if (remainingCustom.length === 0) {
                try {
                    await safeFetch('/api/demo/set-mode', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ mode: 'demo' })
                    });
                    
                    const toggleDemoBtn = document.getElementById('toggleDemoBtn');
                    const toggleCustomBtn = document.getElementById('toggleCustomBtn');
                    if (toggleDemoBtn && toggleCustomBtn) {
                        toggleDemoBtn.classList.add('active');
                        toggleCustomBtn.classList.remove('active');
                    }
                } catch (err) {
                    console.error('Failed to set demo mode on delete:', err);
                }
            }

            await loadDashboard();
            await fetchSources();
        } else {
            alert("Failed to delete source. Please try again.");
            if (sourceEl) {
                sourceEl.style.opacity = '1';
                sourceEl.style.pointerEvents = 'auto';
            }
        }
    } catch (e) {
        console.error("Failed to delete source", e);
        if (sourceEl) {
            sourceEl.style.opacity = '1';
            sourceEl.style.pointerEvents = 'auto';
        }
    }
}
window.deleteSource = deleteSource;
window.uploadFile = uploadFile;

// 2. Notes Management
async function fetchNotes() {
    try {
        const res = await fetch('/api/notes');
        const data = await res.json();
        renderNotesList(data.notes || []);
    } catch (e) {
        console.error("Failed to fetch notes", e);
    }
}

function renderNotesList(notes) {
    const container = document.getElementById('notesList');
    if (!container) return;
    if (!notes.length) {
        container.innerHTML = '<p class="emptyHint">No saved notes in your notebook. Click + to add one.</p>';
        return;
    }
    
    container.innerHTML = notes.map(n => `
        <div class="noteItem" id="note-${n.note_id}">
            <div class="noteItemHead">
                <h4>${n.title}</h4>
                <button class="deleteNoteBtn" onclick="deleteNote(${n.note_id})">&times;</button>
            </div>
            <div class="noteItemContent">${marked.parse(n.content)}</div>
        </div>
    `).join('');
}

async function createNote() {
    const title = prompt("Enter note title:");
    if (!title) return;
    const content = prompt("Enter note content:");
    if (!content) return;
    
    try {
        const res = await fetch('/api/notes', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, content })
        });
        if (res.ok) {
            fetchNotes();
        }
    } catch (e) {
        console.error("Failed to create note", e);
    }
}

async function deleteNote(noteId) {
    try {
        const res = await fetch(`/api/notes/${noteId}`, { method: 'DELETE' });
        if (res.ok) {
            fetchNotes();
        }
    } catch (e) {
        console.error("Failed to delete note", e);
    }
}

async function saveSnippetToNotes(title, content) {
    try {
        const res = await fetch('/api/notes', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, content })
        });
        if (res.ok) {
            fetchNotes();
            alert("Saved to Notes!");
        }
    } catch (e) {
        console.error("Failed to save snippet", e);
    }
}

// 3. Business Analytics & Campaign ROI Simulator
let currentCurrencySymbol = '$';
let currentCurrencyRate = 1.0;
let businessAnalyticsData = null;

async function loadBusinessAnalytics() {
    try {
        const res = await fetch('/api/business-analytics');
        businessAnalyticsData = await res.json();
        renderBusinessAnalytics();
    } catch (e) {
        console.error("Failed to load business analytics", e);
    }
}

function renderBusinessAnalytics() {
    if (!businessAnalyticsData) return;
    
    const charges = businessAnalyticsData.total_charges * currentCurrencyRate;
    const loss = businessAnalyticsData.expected_loss * currentCurrencyRate;
    
    document.getElementById('bizTotalCharges').textContent = `${currentCurrencySymbol}${Math.round(charges).toLocaleString()}`;
    document.getElementById('bizExpectedLoss').textContent = `${currentCurrencySymbol}${Math.round(loss).toLocaleString()}`;
    document.getElementById('bizRiskExposurePct').textContent = `${businessAnalyticsData.risk_exposure_pct}%`;
    
    renderBusinessSegments(businessAnalyticsData.segments || []);
    runCampaignSimulation();
    renderCohortTable();
}

function renderBusinessSegments(segments) {
    const tbody = document.getElementById('bizSegmentRows');
    if (!tbody) return;
    if (!segments.length) {
        tbody.innerHTML = '<tr><td colspan="5" class="empty">No segment data available.</td></tr>';
        return;
    }
    tbody.innerHTML = segments.map(s => {
        const loss = s.expected_loss * currentCurrencyRate;
        return `
            <tr>
                <td><strong>${s.dimension}</strong></td>
                <td><span class="badge low">${s.value}</span></td>
                <td>${s.count}</td>
                <td>${(s.avg_risk * 100).toFixed(1)}%</td>
                <td class="danger-text"><strong>${currentCurrencySymbol}${Math.round(loss).toLocaleString()}</strong></td>
            </tr>
        `;
    }).join('');
}

function renderCohortTable() {
    const tbody = document.getElementById('cohortRows');
    if (!tbody) return;
    if (!predictionData || !predictionData.length) {
        tbody.innerHTML = '<tr><td colspan="6" class="empty" style="padding: 20px;">No customer records loaded yet.</td></tr>';
        return;
    }

    const cohorts = {};
    predictionData.forEach(row => {
        const ct = row.contract_type || 'Month-to-month';
        if (!cohorts[ct]) {
            cohorts[ct] = { total: 0, churned: 0 };
        }
        cohorts[ct].total++;
        if (row.prediction_label === 'high_risk' || row.prediction_label === labelMapping.high_risk || row.churned == 1) {
            cohorts[ct].churned++;
        }
    });

    const getHeatmapStyle = (pct) => {
        if (pct >= 90) return 'background-color: rgba(0, 245, 255, 0.40); color: #fff; font-weight: 700;';
        if (pct >= 80) return 'background-color: rgba(0, 245, 255, 0.30); color: #fff;';
        if (pct >= 70) return 'background-color: rgba(0, 245, 255, 0.20); color: #fff;';
        if (pct >= 50) return 'background-color: rgba(0, 245, 255, 0.10); color: var(--text);';
        return 'background-color: rgba(255, 0, 127, 0.25); color: var(--danger); font-weight: 700;';
    };

    tbody.innerHTML = Object.keys(cohorts).map(ct => {
        const c = cohorts[ct];
        const m1Pct = Math.round(((c.total - (c.churned * 0.12)) / c.total) * 100);
        const m3Pct = Math.round(((c.total - (c.churned * 0.32)) / c.total) * 100);
        const m6Pct = Math.round(((c.total - (c.churned * 0.62)) / c.total) * 100);
        const m12Pct = Math.round(((c.total - c.churned) / c.total) * 100);

        return `
            <tr style="border-bottom: 1px solid var(--border);">
                <td style="padding: 12px; text-align: left; font-weight: 700;">${ct} Cohort</td>
                <td style="padding: 12px; background: var(--surface-2);">${c.total}</td>
                <td style="padding: 12px; ${getHeatmapStyle(m1Pct)}">${m1Pct}%</td>
                <td style="padding: 12px; ${getHeatmapStyle(m3Pct)}">${m3Pct}%</td>
                <td style="padding: 12px; ${getHeatmapStyle(m6Pct)}">${m6Pct}%</td>
                <td style="padding: 12px; ${getHeatmapStyle(m12Pct)}">${m12Pct}%</td>
            </tr>
        `;
    }).join('');
    
    updateDrillDownChart();
}

window.updateDrillDownChart = function() {
    const drillSelect = document.getElementById('segmentDrillDownSelect');
    const val = drillSelect ? drillSelect.value : 'all';
    
    let filtered = predictionData;
    if (val !== 'all') {
        if (val.startsWith('contract_')) {
            const contract = val.replace('contract_', '');
            filtered = predictionData.filter(item => (item.contract_type || 'Month-to-month') === contract);
        } else if (val === 'support_high') {
            filtered = predictionData.filter(item => Number(item.support_tickets || 0) >= 3);
        } else if (val === 'support_low') {
            filtered = predictionData.filter(item => Number(item.support_tickets || 0) < 3);
        }
    }
    
    let total = filtered.length;
    let highRiskCount = filtered.filter(item => item.prediction_label === labelMapping.high_risk || item.churned == 1).length;
    
    let m1 = 100;
    let m3 = 100;
    let m6 = 100;
    let m12 = 100;
    
    if (total > 0) {
        m1 = Math.round(((total - (highRiskCount * 0.12)) / total) * 100);
        m3 = Math.round(((total - (highRiskCount * 0.32)) / total) * 100);
        m6 = Math.round(((total - (highRiskCount * 0.62)) / total) * 100);
        m12 = Math.round(((total - highRiskCount) / total) * 100);
    } else {
        m1 = 98; m3 = 85; m6 = 72; m12 = 58;
    }
    
    const xLabels = ['Month 1', 'Month 3', 'Month 6', 'Month 12'];
    const yValues = [m1, m3, m6, m12];
    
    if (cohortTrendChart) cohortTrendChart.destroy();
    
    const canvas = document.getElementById('cohortTrendChart');
    if (!canvas) return;
    
    const bodyStyles = getComputedStyle(document.body);
    const labelColor = bodyStyles.getPropertyValue('--muted').trim() || '#475467';
    const gridColor = bodyStyles.getPropertyValue('--border').trim() || 'rgba(16, 24, 40, 0.08)';
    
    cohortTrendChart = new Chart(canvas, {
        type: 'line',
        data: {
            labels: xLabels,
            datasets: [{
                label: 'Retention Rate %',
                data: yValues,
                borderColor: '#00F5FF',
                backgroundColor: 'rgba(0, 245, 255, 0.08)',
                fill: true,
                tension: 0.3,
                borderWidth: 2,
                pointBackgroundColor: '#00F5FF'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { min: 0, max: 100, ticks: { color: labelColor, callback: value => value + '%' }, grid: { color: gridColor } },
                x: { ticks: { color: labelColor }, grid: { color: gridColor } }
            }
        }
    });
}

function setupBusinessHub() {
    const thresholdInput = document.getElementById('simRiskThreshold');
    const discountInput = document.getElementById('simDiscount');
    const successInput = document.getElementById('simSuccessRate');
    const currencySelect = document.getElementById('currencySelect');
    
    if (thresholdInput) {
        thresholdInput.addEventListener('input', runCampaignSimulation);
    }
    if (discountInput) {
        discountInput.addEventListener('input', runCampaignSimulation);
    }
    if (successInput) {
        successInput.addEventListener('input', runCampaignSimulation);
    }
    if (currencySelect) {
        currencySelect.addEventListener('change', (e) => {
            const opt = e.target.options[e.target.selectedIndex];
            currentCurrencySymbol = opt.getAttribute('data-symbol') || '$';
            currentCurrencyRate = parseFloat(opt.getAttribute('data-rate') || '1.0');
            renderBusinessAnalytics();
        });
    }
}

function runCampaignSimulation() {
    const threshold = parseFloat(document.getElementById('simRiskThreshold').value) / 100;
    const discount = parseFloat(document.getElementById('simDiscount').value) / 100;
    const successRate = parseFloat(document.getElementById('simSuccessRate').value) / 100;
    
    // Update label text indicators
    document.getElementById('valRiskThreshold').textContent = `${Math.round(threshold * 100)}%`;
    document.getElementById('valDiscount').textContent = `${Math.round(discount * 100)}%`;
    document.getElementById('valSuccessRate').textContent = `${Math.round(successRate * 100)}%`;
    
    // Compute targeted pool
    const targeted = predictionData.filter(item => Number(item.predicted_probability || 0) >= threshold);
    const count = targeted.length;
    
    const targetedRevenue = targeted.reduce((sum, item) => {
        const charges = item.monthly_charges !== undefined && item.monthly_charges !== null 
            ? Number(item.monthly_charges) 
            : 100.0;
        return sum + charges;
    }, 0);
    
    const campaignCost = targetedRevenue * discount * currentCurrencyRate;
    const grossSaved = targetedRevenue * successRate * currentCurrencyRate;
    const netSaved = grossSaved - campaignCost;
    
    const roi = campaignCost > 0 ? (netSaved / campaignCost) * 100 : 0;
    
    document.getElementById('simTargetedCount').textContent = count.toLocaleString();
    document.getElementById('simCampaignCost').textContent = `${currentCurrencySymbol}${Math.round(campaignCost).toLocaleString()}`;
    document.getElementById('simSavedRevenue').textContent = `${currentCurrencySymbol}${Math.round(grossSaved).toLocaleString()}`;
    
    const netSavedEl = document.getElementById('simNetSavedRevenue');
    netSavedEl.textContent = `${currentCurrencySymbol}${Math.round(netSaved).toLocaleString()}`;
    if (netSaved >= 0) {
        netSavedEl.parentElement.classList.remove('danger');
        netSavedEl.parentElement.classList.add('success');
    } else {
        netSavedEl.parentElement.classList.remove('success');
        netSavedEl.parentElement.classList.add('danger');
    }
    
    const roiBadge = document.getElementById('simRoiBadge');
    roiBadge.textContent = `ROI: ${Math.round(roi)}%`;
    if (roi >= 20) {
        roiBadge.className = 'roiBadge success';
    } else if (roi >= 0) {
        roiBadge.className = 'roiBadge warning';
    } else {
        roiBadge.className = 'roiBadge danger';
    }
}

// 5. Clickable Citations
function highlightCustomer(customerId) {
    const tabBtn = document.querySelector('.tab[data-tab="customers"]');
    if (tabBtn) tabBtn.click();
    
    const filter = document.getElementById('riskFilter');
    if (filter) {
        filter.value = 'all';
        renderRows();
    }
    
    setTimeout(() => {
        const rows = document.getElementById('predictionRows').querySelectorAll('tr');
        let foundRow = null;
        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            if (cells.length && cells[0].textContent.trim() === customerId) {
                foundRow = row;
            }
        });
        
        if (foundRow) {
            foundRow.scrollIntoView({ behavior: 'smooth', block: 'center' });
            foundRow.classList.add('highlightFlash');
            setTimeout(() => {
                foundRow.classList.remove('highlightFlash');
            }, 2500);
        }
    }, 250);
}

// 4. Presentation Builder Controller
let presentationSlides = [];
let currentSlideIndex = 0;

function setupPresentation() {
    const genBtn = document.getElementById('generatePresBtn');
    if (genBtn) {
        genBtn.addEventListener('click', generatePresentationDeck);
    }

    const prevBtn = document.getElementById('prevSlideBtn');
    if (prevBtn) {
        prevBtn.addEventListener('click', () => changeSlide(-1));
    }

    const nextBtn = document.getElementById('nextSlideBtn');
    if (nextBtn) {
        nextBtn.addEventListener('click', () => changeSlide(1));
    }

    const fullscreenBtn = document.getElementById('fullscreenPresBtn');
    if (fullscreenBtn) {
        fullscreenBtn.addEventListener('click', enterFullscreenPresentation);
    }

    const downloadBtn = document.getElementById('downloadPresBtn');
    if (downloadBtn) {
        downloadBtn.addEventListener('click', downloadStandalonePresentation);
    }

    const downloadPptxBtn = document.getElementById('downloadPresPptxBtn');
    if (downloadPptxBtn) {
        downloadPptxBtn.addEventListener('click', downloadPresentationAsPptx);
    }

    // Keyboard Arrow Navigation
    document.addEventListener('keydown', (e) => {
        const presentationTab = document.querySelector('.tab[data-tab="presentation"]');
        if (presentationTab && presentationTab.classList.contains('active')) {
            if (e.key === 'ArrowLeft') {
                changeSlide(-1);
            } else if (e.key === 'ArrowRight') {
                changeSlide(1);
            } else if (e.key === 'f' || e.key === 'F') {
                enterFullscreenPresentation();
            }
        }
    });

    // Bind Image Style Select Change
    const styleSelect = document.getElementById('presImageStyle');
    if (styleSelect) {
        styleSelect.addEventListener('change', () => {
            if (presentationSlides && presentationSlides.length) {
                renderSlides(presentationSlides);
                updateSlideView();
            }
        });
    }

    // Bind Typography, Palette and Transition select changes
    const fontSelect = document.getElementById('presFontPairing');
    if (fontSelect) {
        fontSelect.addEventListener('change', () => {
            if (presentationSlides && presentationSlides.length) {
                renderSlides(presentationSlides);
                updateSlideView();
            }
        });
    }

    const themeSelect = document.getElementById('presThemeColor');
    if (themeSelect) {
        themeSelect.addEventListener('change', () => {
            if (presentationSlides && presentationSlides.length) {
                renderSlides(presentationSlides);
                updateSlideView();
            }
        });
    }

    const transSelect = document.getElementById('presTransition');
    if (transSelect) {
        transSelect.addEventListener('change', () => {
            if (presentationSlides && presentationSlides.length) {
                renderSlides(presentationSlides);
                updateSlideView();
            }
        });
    }

    // Bind Dynamic Image Generator & Search Tools
    const genImageBtn = document.getElementById('generateSlideImageBtn');
    if (genImageBtn) {
        genImageBtn.addEventListener('click', async () => {
            const promptInput = document.getElementById('slideCustomImagePrompt');
            const keyword = promptInput ? promptInput.value.trim() : '';
            const sourceSelect = document.getElementById('slideImageSource');
            const mediaSource = sourceSelect ? sourceSelect.value : 'unsplash';
            const resultsContainer = document.getElementById('imageResultsContainer');
            
            if (!keyword) {
                alert('Please enter a description or keyword for the media search.');
                return;
            }
            
            if (resultsContainer) {
                resultsContainer.innerHTML = '<span style="font-size:0.75rem; color:var(--muted);">Querying global creative commons engines...</span>';
            }
            
            let urls = [];
            
            try {
                const response = await fetch('/api/media/search', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: keyword, source: mediaSource })
                });
                
                if (response.ok) {
                    const data = await response.json();
                    if (data.results && data.results.length > 0) {
                        urls = data.results.map(r => r.url);
                    }
                }
            } catch (err) {
                console.error("Media search error, falling back to Unsplash", err);
            }
            
            if (urls.length === 0) {
                urls = [
                    `https://images.unsplash.com/featured/300x200?sig=${Math.floor(Math.random()*1000)}&${encodeURIComponent(keyword)}`,
                    `https://images.unsplash.com/featured/300x200?sig=${Math.floor(Math.random()*1000)}&${encodeURIComponent(keyword)}`,
                    `https://images.unsplash.com/featured/300x200?sig=${Math.floor(Math.random()*1000)}&${encodeURIComponent(keyword)}`,
                    `https://images.unsplash.com/featured/300x200?sig=${Math.floor(Math.random()*1000)}&${encodeURIComponent(keyword)}`
                ];
            }
            
            if (resultsContainer) {
                if (urls.length === 0) {
                    resultsContainer.innerHTML = '<span style="font-size:0.75rem; color:var(--danger);">No results found. Try another query.</span>';
                    return;
                }
                resultsContainer.innerHTML = urls.map((url, idx) => `
                    <div class="generatedImageThumb" onclick="selectSlideImage('${url}')" style="flex:0 0 100px; height:70px; border-radius:6px; overflow:hidden; border:2px solid var(--border); cursor:pointer; position:relative; transition:all 0.15s ease;">
                        <img src="${url}" style="width:100%; height:100%; object-fit:cover;" onerror="this.src='https://images.unsplash.com/photo-1557804506-669a67965ba0?auto=format&fit=crop&w=600&q=80'" />
                        <span style="position:absolute; bottom:2px; right:2px; background:rgba(0,0,0,0.6); color:#fff; font-size:0.55rem; padding:1px 3px; border-radius:3px; font-weight:700;">Option ${idx+1}</span>
                    </div>
                `).join('');
            }
        });
    }

    window.selectSlideImage = function(url) {
        if (!presentationSlides || !presentationSlides[currentSlideIndex]) return;
        presentationSlides[currentSlideIndex].imgUrl = url;
        renderSlides(presentationSlides);
        updateSlideView();
        
        document.querySelectorAll('.generatedImageThumb').forEach(thumb => {
            const img = thumb.querySelector('img');
            if (img && img.src === url) {
                thumb.style.borderColor = 'var(--accent)';
            } else {
                thumb.style.borderColor = 'var(--border)';
            }
        });
    };

    // Bind AI Prompt Magic Chips
    document.querySelectorAll('.pres-prompt-chip').forEach(chip => {
        chip.addEventListener('click', () => {
            const promptText = chip.getAttribute('data-prompt');
            const input = document.getElementById('presCustomPrompt');
            if (input) {
                input.value = promptText;
                generatePresentationDeck();
            }
        });
    });

    const saveBtn = document.getElementById('saveSlideBtn');
    if (saveBtn) {
        saveBtn.addEventListener('click', () => {
            const slide = presentationSlides[currentSlideIndex];
            if (!slide) return;
            slide.title = document.getElementById('editSlideTitle').value;
            slide.subtitle = document.getElementById('editSlideSubtitle').value;
            const layoutSelect = document.getElementById('editSlideLayout');
            if (layoutSelect) slide.layout = layoutSelect.value;
            
            if (slide.layout !== 'title') {
                const contentVal = document.getElementById('editSlideContent').value;
                const lines = contentVal.split('\n').map(l => l.trim()).filter(l => l);
                if (slide.layout === 'split_metrics' || slide.layout === 'segment_comparison') {
                    slide.bullets = lines;
                } else if (slide.layout === 'prescriptive_playbook') {
                    slide.playbook = lines.map((line, idx) => {
                        const parts = line.split(':');
                        const types = ['success', 'primary', 'warning', 'accent'];
                        return {
                            title: parts[0] ? parts[0].trim() : `Solution ${idx+1}`,
                            desc: parts[1] ? parts[1].trim() : 'Prescriptive retention action item.',
                            type: types[idx % types.length]
                        };
                    });
                } else if (slide.layout === 'journey_workflow') {
                    slide.steps = lines.map((line, idx) => {
                        const parts = line.split(':');
                        return {
                            step: idx + 1,
                            title: parts[0] ? parts[0].trim() : `Stage ${idx+1}`,
                            description: parts[1] ? parts[1].trim() : ''
                        };
                    });
                }
            }
            renderSlides(presentationSlides);
            updateSlideView();
        });
    }

    const addBtn = document.getElementById('addSlideBtn');
    if (addBtn) {
        addBtn.addEventListener('click', () => {
            const newSlide = {
                layout: 'split_metrics',
                title: 'New Custom Analytics Slide',
                subtitle: 'Ad-hoc retention deep-dive insights',
                bullets: ['Focus on low-satisfaction accounts', 'Offer special contracts to prevent churn']
            };
            presentationSlides.splice(currentSlideIndex + 1, 0, newSlide);
            currentSlideIndex++;
            renderSlides(presentationSlides);
            updateSlideView();
        });
    }

    const delBtn = document.getElementById('deleteSlideBtn');
    if (delBtn) {
        delBtn.addEventListener('click', () => {
            if (!presentationSlides.length) return;
            presentationSlides.splice(currentSlideIndex, 1);
            currentSlideIndex = Math.max(0, Math.min(currentSlideIndex, presentationSlides.length - 1));
            if (presentationSlides.length === 0) {
                document.getElementById('slideViewport').classList.add('hidden');
                document.getElementById('slideEditorPanel').classList.add('hidden');
                document.getElementById('prevSlideBtn').classList.add('hidden');
                document.getElementById('nextSlideBtn').classList.add('hidden');
            } else {
                renderSlides(presentationSlides);
                updateSlideView();
            }
        });
    }

    // Bind Presentation Q&A buttons
    document.querySelectorAll('.qa-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const question = btn.getAttribute('data-question');
            triggerQuickQA(question);
        });
    });

    // Listen for blur event to save contentedited fields
    const viewport = document.getElementById('slideViewport');
    if (viewport) {
        viewport.addEventListener('blur', (e) => {
            if (e.target.hasAttribute('contenteditable')) {
                const slideIdx = Number(e.target.dataset.slideIndex);
                const field = e.target.dataset.field;
                const bulletIdx = e.target.dataset.bulletIndex;
                const playbookIdx = e.target.dataset.playbookIndex;
                const stepIdx = e.target.dataset.stepIndex;
                
                if (presentationSlides[slideIdx]) {
                    if (field === 'title') {
                        presentationSlides[slideIdx].title = e.target.innerText;
                    } else if (field === 'subtitle') {
                        presentationSlides[slideIdx].subtitle = e.target.innerText;
                    } else if (field === 'bullet' && bulletIdx !== undefined) {
                        if (presentationSlides[slideIdx].bullets) {
                            presentationSlides[slideIdx].bullets[Number(bulletIdx)] = e.target.innerText;
                        }
                    } else if (field === 'playbook-title' && playbookIdx !== undefined) {
                        const pIdx = Number(playbookIdx);
                        if (presentationSlides[slideIdx].playbook && presentationSlides[slideIdx].playbook[pIdx]) {
                            presentationSlides[slideIdx].playbook[pIdx].title = e.target.innerText;
                        }
                    } else if (field === 'playbook-desc' && playbookIdx !== undefined) {
                        const pIdx = Number(playbookIdx);
                        if (presentationSlides[slideIdx].playbook && presentationSlides[slideIdx].playbook[pIdx]) {
                            presentationSlides[slideIdx].playbook[pIdx].desc = e.target.innerText;
                        }
                    } else if (field === 'step-title' && stepIdx !== undefined) {
                        const sIdx = Number(stepIdx);
                        if (presentationSlides[slideIdx].steps && presentationSlides[slideIdx].steps[sIdx]) {
                            presentationSlides[slideIdx].steps[sIdx].title = e.target.innerText;
                        }
                    } else if (field === 'step-desc' && stepIdx !== undefined) {
                        const sIdx = Number(stepIdx);
                        if (presentationSlides[slideIdx].steps && presentationSlides[slideIdx].steps[sIdx]) {
                            presentationSlides[slideIdx].steps[sIdx].description = e.target.innerText;
                            presentationSlides[slideIdx].steps[sIdx].desc = e.target.innerText;
                        }
                    }
                    
                    // Sync inputs in the Slide Editor Panel
                    const editTitle = document.getElementById('editSlideTitle');
                    const editSubtitle = document.getElementById('editSlideSubtitle');
                    const editContent = document.getElementById('editSlideContent');
                    
                    if (slideIdx === currentSlideIndex) {
                        if (editTitle && field === 'title') editTitle.value = e.target.innerText;
                        if (editSubtitle && field === 'subtitle') editSubtitle.value = e.target.innerText;
                        if (editContent) {
                            if (presentationSlides[slideIdx].layout === 'split_metrics' || presentationSlides[slideIdx].layout === 'segment_comparison') {
                                editContent.value = (presentationSlides[slideIdx].bullets || []).join('\n');
                            } else if (presentationSlides[slideIdx].layout === 'prescriptive_playbook') {
                                editContent.value = (presentationSlides[slideIdx].playbook || []).map(p => `${p.title}: ${p.desc}`).join('\n');
                            } else if (presentationSlides[slideIdx].layout === 'journey_workflow') {
                                editContent.value = (presentationSlides[slideIdx].steps || []).map(s => `${s.title}: ${s.description || s.desc || ''}`).join('\n');
                            }
                        }
                    }
                    
                    // Update sorter timeline thumbnails
                    renderSlideSorterTimeline();
                }
            }
        }, true);
    }
}

function generateLocalSlides(numSlides, customPrompt, shouldShuffle) {
    let total_cust = '1,000+';
    let avg_risk_str = '26.8%';
    
    try {
        if (typeof predictionData !== 'undefined' && predictionData && predictionData.length > 0) {
            const total = predictionData.length;
            total_cust = total.toLocaleString();
            
            const sum = predictionData.reduce((acc, curr) => acc + (parseFloat(curr.predicted_probability) || 0), 0);
            const avg_risk_val = (sum / total) * 100;
            avg_risk_str = `${avg_risk_val.toFixed(1)}%`;
        } else {
            const metaTotal = document.getElementById('metaTotal');
            if (metaTotal && metaTotal.textContent !== '—' && metaTotal.textContent !== '') {
                total_cust = metaTotal.textContent;
            }
        }
    } catch (err) {
        console.error("Error reading metrics for fallback slides", err);
    }
    
    let localPool = [
        {
            "layout": "title",
            "title": customPrompt ? `Custom Profile: ${customPrompt}` : "Qiplo Executive Presentation",
            "subtitle": `Strategic Customer Churn Intelligence — ${total_cust} Accounts Evaluated`
        },
        {
            "layout": "split_metrics",
            "title": "Executive Churn & Risk Summary",
            "bullets": [
                `Overall average customer churn risk across active accounts is currently at ${avg_risk_str}.`,
                "Month-to-month contracts and non-automated payment methods represent the primary attrition drivers.",
                "Targeted proactive outreach combined with annual plan incentives will safeguard vulnerable ARR."
            ],
            "total_cust": total_cust,
            "avg_risk_str": avg_risk_str
        },
        {
            "layout": "segment_comparison",
            "title": "Priority Risk Segments & Vulnerabilities",
            "bullets": [
                "Primary risk segment: Contract 'Month-to-month' (expected loss is high).",
                "Secondary risk segment: Payment Method 'Paper check' (elevated predictive risk).",
                "Fiber Optic & paper check payment accounts exhibit heightened sensitivity requiring priority support."
            ]
        },
        {
            "layout": "prescriptive_playbook",
            "title": "Prescriptive Solutions & Action Matrix",
            "playbook": [
                {"title": "24-Hour CSM Call SLA", "desc": "Mandatory outreach within 24 hours for accounts reaching ≥65% churn risk score.", "type": "success"},
                {"title": "Annual Migration Discount", "desc": "15-20% incentive credit for switching month-to-month contracts to annual terms.", "type": "primary"},
                {"title": "Support Escalation Fast-Track", "desc": "Priority ticket routing (<2 hour response SLA) for accounts with >2 open issues.", "type": "warning"},
                {"title": "VIP Onboarding Check-Ins", "desc": "Structured 90-day milestone check-ins to eliminate early tenure drop-offs.", "type": "accent"}
            ]
        },
        {
            "layout": "journey_workflow",
            "title": "Interactive Customer Journey Workflow",
            "steps": [
                {"title": "Predictive Audit", "description": "Qiplo Copilot scans database records for risk scores."},
                {"title": "Strategy Design", "description": "Formulate billing recovery & proactive support incentives."},
                {"title": "Manager Outreach", "description": "CSMs initiate outreach using pre-compiled templates."},
                {"title": "ARR Preservation", "description": "Contracts successfully extended; customer retention maximized."}
            ]
        }
    ];
    
    if (shouldShuffle) {
        const title = localPool[0];
        let others = localPool.slice(1);
        others.sort(() => Math.random() - 0.5);
        localPool = [title, ...others];
    }
    
    let slides = [];
    while (slides.length < numSlides) {
        slides = slides.concat(localPool);
    }
    return slides.slice(0, numSlides);
}

async function generatePresentationDeck() {
    const genBtn = document.getElementById('generatePresBtn');
    const status = document.getElementById('deckStatus');
    const viewport = document.getElementById('slideViewport');
    const prevBtn = document.getElementById('prevSlideBtn');
    const nextBtn = document.getElementById('nextSlideBtn');
    const fullscreenBtn = document.getElementById('fullscreenPresBtn');
    const downloadBtn = document.getElementById('downloadPresBtn');

    genBtn.disabled = true;
    genBtn.textContent = 'Generating...';

    try {
        const customPrompt = document.getElementById('presCustomPrompt') ? document.getElementById('presCustomPrompt').value : '';
        const slideCountEl = document.getElementById('presSlideCount');
        const numSlides = slideCountEl ? parseInt(slideCountEl.value) : 5;

        // Instant dynamic client-side generation using loaded database metrics
        const fallbackSlides = generateLocalSlides(numSlides, customPrompt, true);
        presentationSlides = fallbackSlides;
        currentSlideIndex = 0;
        renderSlides(fallbackSlides);

        viewport.classList.remove('hidden');
        prevBtn.classList.remove('hidden');
        nextBtn.classList.remove('hidden');
        if (fullscreenBtn) fullscreenBtn.classList.remove('hidden');
        const printBtn = document.getElementById('printPresBtn');
        if (printBtn) printBtn.classList.remove('hidden');
        if (downloadBtn) downloadBtn.classList.remove('hidden');
        const downloadPptxBtn = document.getElementById('downloadPresPptxBtn');
        if (downloadPptxBtn) downloadPptxBtn.classList.remove('hidden');
        const editorPanel = document.getElementById('slideEditorPanel');
        if (editorPanel) editorPanel.classList.remove('hidden');
        status.classList.add('hidden');
        updateSlideView();
    } catch (e) {
        console.error("Instant presentation generation failed:", e);
    } finally {
        genBtn.disabled = false;
        genBtn.textContent = 'Generate AI Deck';
    }
}

function renderSlides(slides) {
    const viewport = document.getElementById('slideViewport');
    if (!viewport) return;

    window.imageStyles = {
        corporate: [
            "https://images.unsplash.com/photo-1557804506-669a67965ba0?auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=600&q=80"
        ],
        anime: [
            "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1578632767115-351597cf2477?auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1618336753974-aae8e04506aa?auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1601987177651-8edfe6c20009?auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1563089145-599997674d42?auto=format&fit=crop&w=600&q=80"
        ],
        minimalist: [
            "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1604871000636-074fa5117945?auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1541701494587-cb58502866ab?auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?auto=format&fit=crop&w=600&q=80"
        ],
        cyberpunk: [
            "https://images.unsplash.com/photo-1515621061946-eff1c2a352bd?auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1542831371-29b0f74f9713?auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=600&q=80",
            "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=600&q=80"
        ]
    };

    const fontSelect = document.getElementById('presFontPairing');
    const themeSelect = document.getElementById('presThemeColor');
    const transSelect = document.getElementById('presTransition');
    
    const fontClass = fontSelect ? fontSelect.value : 'inter_mono';
    const themeClass = themeSelect ? themeSelect.value : 'indigo';
    const transClass = transSelect ? transSelect.value : 'fade';
    
    const isHidden = viewport.classList.contains('hidden');
    viewport.className = `slideViewport font-${fontClass} theme-${themeClass} trans-${transClass}${isHidden ? ' hidden' : ''}`;

    const styleSelect = document.getElementById('presImageStyle');
    const selectedStyle = styleSelect ? styleSelect.value : 'corporate';
    const activeList = window.imageStyles[selectedStyle] || window.imageStyles.corporate;

    viewport.innerHTML = slides.map((slide, idx) => {
        let contentHtml = '';
        const imgUrl = slide.imgUrl || activeList[idx % activeList.length];

        if (slide.layout === 'title') {
            contentHtml = `
                <div class="slideContent layout-title">
                    <div class="slideHeader">
                        <div class="presMiniLogo">Qiplo</div>
                        <span>Never lose a customer again.</span>
                    </div>
                    <div style="display: flex; align-items: center; justify-content: space-between; width: 100%; margin: 16px 0; gap: 24px;">
                        <div style="text-align: left; flex: 1;">
                            <h1 contenteditable="true" data-slide-index="${idx}" data-field="title" style="font-size: 2.2rem; margin: 0 0 10px; line-height: 1.15; background: linear-gradient(135deg, #00F5FF, #FF007F); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">${slide.title}</h1>
                            <p class="slideSubtitle" contenteditable="true" data-slide-index="${idx}" data-field="subtitle" style="font-size: 1rem; color: var(--muted); margin: 0 0 16px; line-height: 1.5;">${slide.subtitle}</p>
                            <div style="display: inline-flex; gap: 8px; align-items: center; background: rgba(0,245,255,0.08); border: 1px solid var(--accent); padding: 6px 14px; border-radius: 20px; font-size: 0.8rem; color: var(--accent); font-weight: 600;">
                                <i data-lucide="shield-check" class="lucide-icon"></i> Executive Strategic Briefing • 100% Watermark Free
                            </div>
                        </div>
                        <div class="slideHeroPhoto" style="flex: 0 0 210px; height: 170px; border-radius: 14px; overflow: hidden; border: 1px solid var(--border); box-shadow: var(--shadow); position: relative;">
                            <img src="${imgUrl}" alt="Corporate Executive Presentation" class="zoomableImage" onclick="openMagnificZoom(this.src, this.alt)" style="width: 100%; height: 100%; object-fit: cover; filter: brightness(0.9) contrast(1.05); cursor: zoom-in;" />
                            <div style="position: absolute; bottom: 8px; left: 8px; right: 8px; background: rgba(12,15,23,0.85); backdrop-filter: blur(8px); padding: 4px 8px; border-radius: 6px; font-size: 0.68rem; color: var(--text); font-weight: 600;">
                                🏢 Executive Boardroom
                            </div>
                        </div>
                    </div>
                    <div class="slideFooter">
                        <span>Executive Churn Intelligence Briefing</span>
                        <span>Slide ${idx+1} of ${slides.length}</span>
                    </div>
                </div>
            `;
        } else if (slide.layout === 'split_metrics') {
            const listHtml = (slide.bullets || []).map((b, bIdx) => `<li contenteditable="true" data-slide-index="${idx}" data-field="bullet" data-bullet-index="${bIdx}">${b}</li>`).join('');
            contentHtml = `
                <div class="slideContent layout-split">
                    <div class="slideHeader">
                        <div class="presMiniLogo">Qiplo</div>
                        <span>Executive Churn & Risk Summary</span>
                    </div>
                    <div class="slideSplitBody" style="display: flex; gap: 24px; margin: 14px 0; align-items: center;">
                        <div class="slideLeftPane" style="flex: 0 0 220px;">
                            <div style="height: 100px; border-radius: 10px; overflow: hidden; border: 1px solid var(--border); margin-bottom: 10px;">
                                <img src="${imgUrl}" alt="Financial Analytics & Revenue Exposure" class="zoomableImage" onclick="openMagnificZoom(this.src, this.alt)" style="width: 100%; height: 100%; object-fit: cover; filter: brightness(0.9); cursor: zoom-in;" />
                            </div>
                            <div class="statCallout pink" style="margin-bottom: 8px; padding: 10px; background: rgba(255,0,127,0.1); border: 1px solid var(--accent); border-radius: 10px;">
                                <span style="font-size:0.68rem; color:var(--muted); text-transform:uppercase;">Evaluated Accounts</span>
                                <h2 style="margin:2px 0 0; color:#ffffff; font-family:'JetBrains Mono', monospace; font-size:1.35rem;">${slide.total_cust || '1,000+'}</h2>
                            </div>
                            <div class="statCallout" style="padding: 10px; background: rgba(0,245,255,0.08); border: 1px solid var(--primary); border-radius: 10px;">
                                <span style="font-size:0.68rem; color:var(--muted); text-transform:uppercase;">Avg Risk Score</span>
                                <h2 style="margin:2px 0 0; color:var(--primary); font-family:'JetBrains Mono', monospace; font-size:1.35rem;">${slide.avg_risk_str || '26.8%'}</h2>
                            </div>
                        </div>
                        <div class="slideRightPane" style="flex: 1;">
                            <h2 contenteditable="true" data-slide-index="${idx}" data-field="title" style="margin-top: 0; font-size: 1.3rem; color: var(--text);">${slide.title}</h2>
                            <ul style="line-height: 1.65; font-size: 0.9rem; color: var(--muted); padding-left: 20px;">${listHtml}</ul>
                        </div>
                    </div>
                    <div class="slideFooter">
                        <span>Executive Churn Summary</span>
                        <span>Slide ${idx+1} of ${slides.length}</span>
                    </div>
                </div>
            `;
        } else if (slide.layout === 'segment_comparison') {
            const listHtml = (slide.bullets || []).map((b, bIdx) => `
                <div class="riskComparisonCard" style="display: flex; align-items: center; gap: 12px; padding: 10px 14px; background: rgba(255,255,255,0.02); border: 1px solid var(--border); border-radius: 10px;">
                    <div class="cardIcon" style="font-size:1.1rem; color: var(--accent);"><i data-lucide="target" class="lucide-icon"></i></div>
                    <div class="cardContent" style="font-size:0.88rem; color:var(--text); flex:1;">
                        <p style="margin:0;" contenteditable="true" data-slide-index="${idx}" data-field="bullet" data-bullet-index="${bIdx}">${b}</p>
                    </div>
                </div>
            `).join('');
            contentHtml = `
                <div class="slideContent layout-grid">
                    <div class="slideHeader">
                        <div class="presMiniLogo">Qiplo</div>
                        <span>Priority Risk Segments & Vulnerabilities</span>
                    </div>
                    <div style="display: flex; gap: 16px; align-items: center; margin: 8px 0;">
                        <div style="flex: 1;">
                            <h2 contenteditable="true" data-slide-index="${idx}" data-field="title" style="margin: 0 0 6px; font-size: 1.3rem;">${slide.title}</h2>
                            <div style="margin-bottom: 8px;">
                                <svg width="100%" height="38" viewBox="0 0 380 38" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <rect x="5" y="4" width="180" height="30" rx="6" fill="rgba(255,0,127,0.12)" stroke="#FF007F" stroke-width="1.2"/>
                                    <text x="15" y="22" fill="#FF007F" font-weight="800" font-size="9">HIGH SEVERITY VULNERABILITY</text>
                                    
                                    <rect x="195" y="4" width="180" height="30" rx="6" fill="rgba(0,245,255,0.1)" stroke="#00F5FF" stroke-width="1.2"/>
                                    <text x="205" y="22" fill="#00F5FF" font-weight="800" font-size="9">HIGH LOSS MRR SEGMENT</text>
                                </svg>
                            </div>
                        </div>
                        <div style="flex: 0 0 140px; height: 85px; border-radius: 8px; overflow: hidden; border: 1px solid var(--border);">
                            <img src="${imgUrl}" alt="Operations Risk Analysis" class="zoomableImage" onclick="openMagnificZoom(this.src, this.alt)" style="width: 100%; height: 100%; object-fit: cover; filter: brightness(0.9); cursor: zoom-in;" />
                        </div>
                    </div>
                    <div class="slideGridBody" style="display: flex; flex-direction: column; gap: 8px;">
                        ${listHtml}
                    </div>
                    <div class="slideFooter">
                        <span>Risk Segment Analysis</span>
                        <span>Slide ${idx+1} of ${slides.length}</span>
                    </div>
                </div>
            `;
        } else if (slide.layout === 'prescriptive_playbook') {
            const playbookCards = (slide.playbook || []).map((p, pIdx) => `
                <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); border-left: 4px solid var(--${p.type || 'primary'}); padding: 10px 12px; border-radius: 8px;">
                    <h4 contenteditable="true" data-slide-index="${idx}" data-field="playbook-title" data-playbook-index="${pIdx}" style="margin: 0 0 3px; font-size: 0.88rem; color: var(--${p.type || 'primary'}); font-family: 'Outfit', sans-serif;">${p.title}</h4>
                    <p contenteditable="true" data-slide-index="${idx}" data-field="playbook-desc" data-playbook-index="${pIdx}" style="margin: 0; font-size: 0.8rem; color: var(--muted);">${p.desc}</p>
                </div>
            `).join('');
            contentHtml = `
                <div class="slideContent layout-playbook">
                    <div class="slideHeader">
                        <div class="presMiniLogo">Qiplo</div>
                        <span>Prescriptive Solutions & Action Matrix</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin: 8px 0 6px;">
                        <h2 contenteditable="true" data-slide-index="${idx}" data-field="title" style="margin: 0; font-size: 1.3rem;">${slide.title}</h2>
                        <div style="display: flex; align-items: center; gap: 6px; font-size: 0.72rem; color: var(--accent); background: rgba(0,245,255,0.08); padding: 4px 10px; border-radius: 12px; border: 1px solid var(--border);">
                            <span style="display: inline-flex; align-items: center; gap: 4px;"><i data-lucide="users" class="lucide-icon"></i> Strategy Playbook</span>
                        </div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 8px 0;">
                        ${playbookCards}
                    </div>
                    <div class="slideFooter">
                        <span>Prescriptive Action Matrix</span>
                        <span>Slide ${idx+1} of ${slides.length}</span>
                    </div>
                </div>
            `;
        } else if (slide.layout === 'journey_workflow') {
            const stepsHtml = (slide.steps || []).map((st, sIdx) => `
                <div class="workflowStepCard" style="flex:1; background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 10px; border-radius: 8px;">
                    <div class="workflowStepNum" style="font-weight:800; color:var(--primary); font-size:0.8rem; margin-bottom:3px;">STAGE 0${sIdx+1}</div>
                    <div class="workflowStepContent">
                        <h4 contenteditable="true" data-slide-index="${idx}" data-field="step-title" data-step-index="${sIdx}" style="margin:0 0 3px; font-size:0.85rem; color:#ffffff;">${st.title}</h4>
                        <p contenteditable="true" data-slide-index="${idx}" data-field="step-desc" data-step-index="${sIdx}" style="margin:0; font-size:0.78rem; color:var(--muted);">${st.description || st.desc || ''}</p>
                    </div>
                </div>
            `).join('');

            contentHtml = `
                <div class="slideContent layout-workflow">
                    <div class="slideHeader">
                        <div class="presMiniLogo">Qiplo</div>
                        <span>Interactive Customer Journey Workflow</span>
                    </div>
                    <h2 contenteditable="true" data-slide-index="${idx}" data-field="title" style="margin: 8px 0 4px; font-size: 1.3rem;">${slide.title}</h2>
                    <div style="margin-bottom: 8px;">
                        <svg width="100%" height="30" viewBox="0 0 540 30" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <line x1="50" y1="15" x2="490" y2="15" stroke="url(#gradTitle0)" stroke-width="2" stroke-dasharray="6 4" />
                            <circle cx="80" cy="15" r="10" fill="#111827" stroke="#00F5FF" stroke-width="2" />
                            <text x="80" y="18" text-anchor="middle" fill="#00F5FF" font-weight="800" font-size="9">1</text>
                            
                            <circle cx="210" cy="15" r="10" fill="#111827" stroke="#00F5FF" stroke-width="2" />
                            <text x="210" y="18" text-anchor="middle" fill="#00F5FF" font-weight="800" font-size="9">2</text>
                            
                            <circle cx="340" cy="15" r="10" fill="#111827" stroke="#FF007F" stroke-width="2" />
                            <text x="340" y="18" text-anchor="middle" fill="#FF007F" font-weight="800" font-size="9">3</text>
                            
                            <circle cx="470" cy="15" r="10" fill="#111827" stroke="#10B981" stroke-width="2" />
                            <text x="470" y="18" text-anchor="middle" fill="#10B981" font-weight="800" font-size="9">4</text>
                        </svg>
                    </div>
                    <div class="slideWorkflowBody" style="display: flex; gap: 8px;">
                        ${stepsHtml}
                    </div>
                    <div class="slideFooter">
                        <span>Retention Journey Roadmap</span>
                        <span>Slide ${idx+1} of ${slides.length}</span>
                    </div>
                </div>
            `;
        }

        return `
            <div class="slide" id="slide-${idx}">
                ${contentHtml}
            </div>
        `;
    }).join('');

    try {
        if (window.lucide) window.lucide.createIcons();
    } catch (err) {
        console.error("Lucide render failed:", err);
    }
}

function changeSlide(direction) {
    if (!presentationSlides.length) return;
    currentSlideIndex = (currentSlideIndex + direction + presentationSlides.length) % presentationSlides.length;
    updateSlideView();
}

function updateSlideView() {
    document.querySelectorAll('.slide').forEach((slide, idx) => {
        slide.classList.remove('active', 'previous', 'next');
        if (idx === currentSlideIndex) {
            slide.classList.add('active');
        } else if (idx === currentSlideIndex - 1) {
            slide.classList.add('previous');
        } else if (idx === currentSlideIndex + 1) {
            slide.classList.add('next');
        }
    });

    const indicator = document.getElementById('presIndicator');
    if (indicator) {
        indicator.innerHTML = presentationSlides.map((_, idx) => {
            const activeClass = idx === currentSlideIndex ? 'active' : '';
            return `<span class="indicatorDot ${activeClass}" onclick="jumpToSlide(${idx})"></span>`;
        }).join('') + `<span class="indicatorText">Slide ${currentSlideIndex + 1} of ${presentationSlides.length}</span>`;
    }
    populateSlideEditor();
    renderSlideSorterTimeline();
}

function populateSlideEditor() {
    const slide = presentationSlides[currentSlideIndex];
    if (!slide) return;
    
    const titleInput = document.getElementById('editSlideTitle');
    const subtitleInput = document.getElementById('editSlideSubtitle');
    const layoutSelect = document.getElementById('editSlideLayout');
    const contentTextarea = document.getElementById('editSlideContent');
    const label = document.getElementById('editContentLabel');
    
    if (!titleInput || !subtitleInput || !contentTextarea || !label) return;

    titleInput.value = slide.title || '';
    subtitleInput.value = slide.subtitle || '';
    if (layoutSelect) layoutSelect.value = slide.layout || 'split_metrics';

    if (slide.layout === 'title') {
        contentTextarea.value = '';
        contentTextarea.disabled = true;
        label.textContent = 'Slide Copy (Not applicable for Title Slide)';
    } else if (slide.layout === 'split_metrics' || slide.layout === 'segment_comparison') {
        contentTextarea.value = (slide.bullets || []).join('\n');
        contentTextarea.disabled = false;
        label.textContent = 'Bullet Points (one per line)';
    } else if (slide.layout === 'prescriptive_playbook') {
        contentTextarea.value = (slide.playbook || []).map(p => `${p.title}: ${p.desc}`).join('\n');
        contentTextarea.disabled = false;
        label.textContent = 'Playbook Items (one per line, Format: Title: Description)';
    } else if (slide.layout === 'journey_workflow') {
        contentTextarea.value = (slide.steps || []).map(s => `${s.title}: ${s.description || s.desc || ''}`).join('\n');
        contentTextarea.disabled = false;
        label.textContent = 'Workflow Steps (one per line, Format: Stage Title: Description)';
    }
}

function renderSlideSorterTimeline() {
    const timeline = document.getElementById('slideSorterTimeline');
    const controls = document.getElementById('slideLevelControls');
    if (!timeline) return;
    
    if (!presentationSlides || !presentationSlides.length) {
        timeline.classList.add('hidden');
        if (controls) controls.classList.add('hidden');
        return;
    }
    
    timeline.classList.remove('hidden');
    if (controls) controls.classList.remove('hidden');
    
    timeline.innerHTML = presentationSlides.map((slide, idx) => {
        const isActive = idx === currentSlideIndex;
        const borderStyle = isActive ? 'border: 2px solid var(--accent);' : 'border: 1px solid var(--border);';
        const backgroundStyle = isActive ? 'background: rgba(0, 245, 255, 0.05);' : 'background: var(--surface);';
        
        return `
            <div onclick="selectSlide(${idx})" style="flex: 0 0 140px; height: 95px; border-radius: 6px; padding: 8px; cursor: pointer; display: flex; flex-direction: column; justify-content: space-between; transition: all 0.2s; position: relative; ${borderStyle} ${backgroundStyle}">
                <div style="font-size: 0.65rem; color: var(--muted); font-weight: 700; display: flex; justify-content: space-between;">
                    <span>SLIDE ${idx + 1}</span>
                    <span style="text-transform: uppercase; font-size: 0.58rem; color: var(--accent);">${slide.layout.replace('_', ' ')}</span>
                </div>
                <div style="font-size: 0.72rem; color: var(--text); font-weight: 600; text-overflow: ellipsis; overflow: hidden; white-space: nowrap; margin-bottom: auto; margin-top: 4px;">
                    ${slide.title || 'Untitled Slide'}
                </div>
                <div style="font-size: 0.65rem; color: var(--muted); text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">
                    ${slide.subtitle || ''}
                </div>
            </div>
        `;
    }).join('');
}

window.selectSlide = function(idx) {
    if (idx >= 0 && idx < presentationSlides.length) {
        currentSlideIndex = idx;
        updateSlideView();
    }
};

window.addNewBlankSlide = function() {
    const newSlide = {
        title: 'New Blank Slide Title',
        subtitle: 'Click to edit subtitle text',
        layout: 'title',
        bullets: ['Point 1', 'Point 2'],
        imgUrl: ''
    };
    presentationSlides.splice(currentSlideIndex + 1, 0, newSlide);
    currentSlideIndex++;
    renderSlides(presentationSlides);
    updateSlideView();
};

window.duplicateCurrentSlide = function() {
    if (!presentationSlides.length) return;
    const current = presentationSlides[currentSlideIndex];
    const clone = JSON.parse(JSON.stringify(current));
    presentationSlides.splice(currentSlideIndex + 1, 0, clone);
    currentSlideIndex++;
    renderSlides(presentationSlides);
    updateSlideView();
};

window.deleteCurrentSlide = function() {
    if (!presentationSlides.length) return;
    presentationSlides.splice(currentSlideIndex, 1);
    currentSlideIndex = Math.max(0, Math.min(currentSlideIndex, presentationSlides.length - 1));
    renderSlides(presentationSlides);
    updateSlideView();
};

window.addNewBulletPoint = function() {
    if (!presentationSlides.length) return;
    const current = presentationSlides[currentSlideIndex];
    if (!current.bullets) current.bullets = [];
    current.bullets.push('Click to type new bullet point');
    renderSlides(presentationSlides);
    updateSlideView();
};

window.deleteLastBulletPoint = function() {
    if (!presentationSlides.length) return;
    const current = presentationSlides[currentSlideIndex];
    if (current.bullets && current.bullets.length > 0) {
        current.bullets.pop();
        renderSlides(presentationSlides);
        updateSlideView();
    }
};

function jumpToSlide(idx) {
    currentSlideIndex = idx;
    updateSlideView();
}

async function downloadPresentationAsPptx() {
    if (!presentationSlides || !presentationSlides.length) {
        alert("No presentation slides available to export.");
        return;
    }

    const theme = document.getElementById('presThemeColor') ? document.getElementById('presThemeColor').value : 'indigo';
    const customPrompt = document.getElementById('presCustomPrompt') ? document.getElementById('presCustomPrompt').value : 'Qiplo Slide Deck';

    const styleSelect = document.getElementById('presImageStyle');
    const selectedStyle = styleSelect ? styleSelect.value : 'corporate';
    const activeList = window.imageStyles ? (window.imageStyles[selectedStyle] || window.imageStyles.corporate) : [];

    const enrichedSlides = presentationSlides.map((s, idx) => ({
        ...s,
        imgUrl: s.imgUrl || activeList[idx % activeList.length]
    }));

    try {
        const downloadPptxBtn = document.getElementById('downloadPresPptxBtn');
        const oldText = downloadPptxBtn.innerHTML;
        downloadPptxBtn.disabled = true;
        downloadPptxBtn.innerHTML = 'Compiling PPTX...';

        const res = await safeFetch('/api/presentation/download-pptx', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                slides: enrichedSlides,
                theme: theme,
                title: customPrompt
            })
        });

        const payload = await res.json();
        downloadPptxBtn.disabled = false;
        downloadPptxBtn.innerHTML = oldText;

        if (payload.status === 'ok' && payload.download_url) {
            window.open(payload.download_url, '_blank');
        } else {
            alert(payload.error || 'Failed to download PPTX.');
        }
    } catch (err) {
        alert('PPTX export error: ' + err);
        const downloadPptxBtn = document.getElementById('downloadPresPptxBtn');
        if (downloadPptxBtn) {
            downloadPptxBtn.disabled = false;
            downloadPptxBtn.innerHTML = '<i data-lucide="file-presentation" class="lucide-icon"></i> Download PPTX Deck';
            if (window.lucide) window.lucide.createIcons();
        }
    }
}

function enterFullscreenPresentation() {
    const container = document.querySelector('.presContainer');
    if (!container) return;

    if (container.requestFullscreen) {
        container.requestFullscreen();
    } else if (container.webkitRequestFullscreen) {
        container.webkitRequestFullscreen();
    }
}

function downloadStandalonePresentation() {
    if (!presentationSlides.length) return;

    const slidesHtml = document.getElementById('slideViewport').innerHTML;
    const fontSelect = document.getElementById('presFontPairing');
    const themeSelect = document.getElementById('presThemeColor');
    const transSelect = document.getElementById('presTransition');
    
    const fontClass = fontSelect ? fontSelect.value : 'inter_mono';
    const themeClass = themeSelect ? themeSelect.value : 'indigo';
    const transClass = transSelect ? transSelect.value : 'fade';

    const standaloneHtml = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Qiplo Executive Slide Deck</title>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@400;700&family=Montserrat:wght@400;700&family=Outfit:wght@400;700&family=Plus+Jakarta+Sans:wght@400;700&family=Playfair+Display:ital,wght@0,700;1,400&family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #0C0E12;
            --surface: #171A21;
            --surface-2: #202530;
            --text: #E2E3E9;
            --muted: #9094A0;
            --accent: #3DDC84;
            --accent-2: #84F3B5;
            --accent-soft: rgba(61, 220, 132, 0.12);
            --border: rgba(61, 220, 132, 0.15);
            --shadow: 0 4px 20px rgba(61, 220, 132, 0.08);
            --radius: 28px;
            --radius-sm: 16px;
            --font: 'Google Sans', 'Segoe UI', Roboto, system-ui, Arial, sans-serif;
        }

        body {
            margin: 0;
            padding: 0;
            background: var(--bg);
            color: var(--text);
            font-family: var(--font);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
        }

        .presContainer {
            width: 90vw;
            height: 50.625vw;
            max-width: 1280px;
            max-height: 720px;
            position: relative;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            box-shadow: 0 12px 48px rgba(0,0,0,0.5);
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .slideViewport {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
        }

        .slide {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            opacity: 0;
            pointer-events: none;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 40px 60px;
            box-sizing: border-box;
        }

        .slide.active {
            opacity: 1;
            pointer-events: auto;
            z-index: 10;
        }

        .slideContent {
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            position: relative;
        }

        .layout-title {
            justify-content: center;
            align-items: center;
            text-align: center;
        }

        .slideHeader {
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding-bottom: 12px;
            font-size: 0.8rem;
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .presMiniLogo {
            font-weight: 800;
            color: var(--accent-2);
        }

        .slideFooter {
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            padding-top: 12px;
            font-size: 0.78rem;
            color: var(--muted);
        }

        /* Font classes */
        .font-inter_mono {
            --pres-heading-font: 'Inter', sans-serif;
            --pres-body-font: 'JetBrains Mono', monospace;
        }
        .font-outfit_jakarta {
            --pres-heading-font: 'Outfit', sans-serif;
            --pres-body-font: 'Plus Jakarta Sans', sans-serif;
        }
        .font-playfair_roboto {
            --pres-heading-font: 'Playfair Display', serif;
            --pres-body-font: 'Roboto', sans-serif;
        }
        .font-montserrat_fira {
            --pres-heading-font: 'Montserrat', sans-serif;
            --pres-body-font: 'Fira Code', monospace;
        }

        /* Palette classes */
        .theme-indigo {
            --pres-accent: #4F46E5;
            --pres-accent-soft: rgba(79, 70, 229, 0.1);
        }
        .theme-emerald {
            --pres-accent: #10B981;
            --pres-accent-soft: rgba(16, 185, 129, 0.1);
        }
        .theme-amber {
            --pres-accent: #F59E0B;
            --pres-accent-soft: rgba(245, 158, 11, 0.1);
        }
        .theme-crimson {
            --pres-accent: #E11D48;
            --pres-accent-soft: rgba(225, 29, 72, 0.1);
        }
        .theme-cyan {
            --pres-accent: #06B6D4;
            --pres-accent-soft: rgba(6, 182, 212, 0.1);
        }

        .slideViewport[class*="font-"] h1,
        .slideViewport[class*="font-"] h2,
        .slideViewport[class*="font-"] h3,
        .slideViewport[class*="font-"] h4 {
            font-family: var(--pres-heading-font) !important;
        }
        .slideViewport[class*="font-"] .slideContent,
        .slideViewport[class*="font-"] p,
        .slideViewport[class*="font-"] li,
        .slideViewport[class*="font-"] span,
        .slideViewport[class*="font-"] div {
            font-family: var(--pres-body-font) !important;
        }

        .slideViewport[class*="theme-"] .statCallout.pink {
            background: var(--pres-accent-soft) !important;
            border-color: var(--pres-accent) !important;
        }
        .slideViewport[class*="theme-"] .statCallout.pink h2 {
            color: var(--pres-accent) !important;
        }
        .slideViewport[class*="theme-"] .presMiniLogo {
            color: var(--pres-accent) !important;
        }

        /* Transition Animations styling */
        .slideViewport[class*="trans-"] .slide {
            transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.6s ease !important;
        }
        .trans-fade .slide {
            transform: none !important;
        }
        .trans-slide .slide {
            transform: translateX(100%) !important;
        }
        .trans-slide .slide.active {
            transform: translateX(0) !important;
        }
        .trans-slide .slide.previous {
            transform: translateX(-100%) !important;
        }
        .trans-slide .slide.next {
            transform: translateX(100%) !important;
        }
        .trans-zoom .slide {
            transform: scale(0.85) !important;
        }
        .trans-zoom .slide.active {
            transform: scale(1) !important;
        }
        .trans-flip {
            perspective: 1200px;
        }
        .trans-flip .slide {
            transform: rotateY(90deg) !important;
            transform-origin: center !important;
            backface-visibility: hidden;
        }
        .trans-flip .slide.active {
            transform: rotateY(0deg) !important;
        }
        .trans-flip .slide.previous {
            transform: rotateY(-90deg) !important;
        }

        /* Lightbox Image Zoom style */
        .zoom-overlay {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(10, 11, 14, 0.95);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.35s ease;
        }
        .zoom-overlay.active {
            opacity: 1;
            pointer-events: auto;
        }
        .zoom-overlay img {
            max-width: 90vw;
            max-height: 90vh;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 10px 40px rgba(0,0,0,0.6);
        }

        .controls {
            position: absolute;
            bottom: 24px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 12px;
            align-items: center;
            background: rgba(10, 11, 14, 0.85);
            backdrop-filter: blur(8px);
            padding: 8px 16px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            z-index: 100;
        }

        .controlBtn {
            background: transparent;
            border: none;
            color: var(--text);
            font-size: 1.5rem;
            cursor: pointer;
            padding: 0 8px;
            line-height: 1;
            transition: color 0.2s ease;
        }

        .controlBtn:hover {
            color: var(--accent);
        }

        .slideNum {
            font-size: 0.84rem;
            color: var(--muted);
            min-width: 80px;
            text-align: center;
        }
        
        .helpText {
            position: absolute;
            bottom: 24px;
            right: 24px;
            font-size: 0.72rem;
            color: var(--muted);
            z-index: 100;
            background: rgba(0,0,0,0.5);
            padding: 4px 8px;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="presContainer">
        <div class="slideViewport font-${fontClass} theme-${themeClass} trans-${transClass}">
            ${slidesHtml}
        </div>

        <div class="controls">
            <button class="controlBtn" onclick="changeSlide(-1)">&lsaquo;</button>
            <span class="slideNum" id="slideNum">Slide 1 of 3</span>
            <button class="controlBtn" onclick="changeSlide(1)">&rsaquo;</button>
        </div>
        
        <div class="helpText">Use Left/Right arrow keys to navigate</div>
    </div>

    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <script>
        let currentSlide = 0;
        const slides = document.querySelectorAll('.slide');

        function updateSlides() {
            slides.forEach((slide, idx) => {
                slide.classList.remove('active', 'previous', 'next');
                if (idx === currentSlide) {
                    slide.classList.add('active');
                } else if (idx === currentSlide - 1) {
                    slide.classList.add('previous');
                } else if (idx === currentSlide + 1) {
                    slide.classList.add('next');
                }
            });
            document.getElementById('slideNum').textContent = "Slide " + (currentSlide + 1) + " of " + slides.length;
        }

        function changeSlide(direction) {
            currentSlide = (currentSlide + direction + slides.length) % slides.length;
            updateSlides();
        }

        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') {
                changeSlide(-1);
            } else if (e.key === 'ArrowRight') {
                changeSlide(1);
            }
        });

        // Image Zoom lightbox implementation
        const overlay = document.createElement('div');
        overlay.className = 'zoom-overlay';
        overlay.innerHTML = '<img src="" id="zoomImg" alt="Slide Image" />';
        document.body.appendChild(overlay);
        overlay.addEventListener('click', () => overlay.classList.remove('active'));

        window.openMagnificZoom = function(src) {
            document.getElementById('zoomImg').src = src;
            overlay.classList.add('active');
        };

        updateSlides();
        if (window.lucide) {
            lucide.createIcons();
        }
    </script>
</body>
</html>`;

    const blob = new Blob([standaloneHtml], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'Qiplo_Executive_Presentation.html';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

async function triggerQuickQA(question) {
    const box = document.getElementById('qaResponseBox');
    if (!box) return;

    box.classList.remove('hidden');
    box.innerHTML = `<div class="qaLoading">Data Scientist processing metrics for presentation Q&A...</div>`;

    try {
        const apiKey = localStorage.getItem('at_ai_model_key') || localStorage.getItem('show_ai_model_key') || '';
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: question, model_key: apiKey, history: [] })
        });
        const payload = await res.json();

        if (res.ok && payload.response) {
            const htmlContent = marked.parse ? marked.parse(payload.response) : payload.response;
            box.innerHTML = `
                <div class="qaSlideCard">
                    <div class="qaSlideHeader">
                        <span class="qaTag">Presentation Q&A Response</span>
                        <span>Factual Data Science Verification</span>
                    </div>
                    <div class="qaSlideBody">
                        <h3>Query: "${question}"</h3>
                        <div class="qaSlideText">${htmlContent}</div>
                    </div>
                    <div class="qaSlideFooter">
                        <span>Qiplo Corporate Presentation Suite</span>
                    </div>
                </div>
            `;
        } else {
            box.innerHTML = `<div class="status error">Failed to process Q&A query: ${payload.error || 'Unknown error'}</div>`;
        }
    } catch (e) {
        box.innerHTML = `<div class="status error">Could not connect to database analyst: ${e}</div>`;
    }
}

setupCopilot();

// 5. Business Guide Controller
function setupBusinessGuide() {
    const searchInput = document.getElementById('guideSearchInput');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase().trim();
            document.querySelectorAll('.guideSectionCard, .termBox').forEach(card => {
                const text = card.textContent.toLowerCase();
                const searchTerm = card.getAttribute('data-search-term') || '';
                if (!query || text.includes(query) || searchTerm.includes(query)) {
                    card.style.display = '';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }

    const guideNavBtn = document.getElementById('guideNavBtn');
    if (guideNavBtn) {
        guideNavBtn.addEventListener('click', () => {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tabBody').forEach(b => b.classList.add('hidden'));
            const guideTab = document.querySelector('.tab[data-tab="guide"]');
            const guideBody = document.getElementById('tab-guide');
            if (guideTab) guideTab.classList.add('active');
            if (guideBody) guideBody.classList.remove('hidden');
        });
    }
}

function setupThemeToggle() {
    const toggleBtn = document.getElementById('themeToggleBtn');
    if (!toggleBtn) return;

    const savedTheme = localStorage.getItem('theme') || 'dark';
    if (savedTheme === 'light') {
        document.body.classList.remove('dark-theme');
        document.body.classList.add('light-theme');
        toggleBtn.innerHTML = '<i data-lucide="moon" class="lucide-icon"></i>';
    } else {
        document.body.classList.remove('light-theme');
        document.body.classList.add('dark-theme');
        toggleBtn.innerHTML = '<i data-lucide="sun" class="lucide-icon"></i>';
    }

    toggleBtn.addEventListener('click', () => {
        if (document.body.classList.contains('light-theme')) {
            document.body.classList.remove('light-theme');
            document.body.classList.add('dark-theme');
            localStorage.setItem('theme', 'dark');
            toggleBtn.innerHTML = '<i data-lucide="sun" class="lucide-icon"></i>';
        } else {
            document.body.classList.remove('dark-theme');
            document.body.classList.add('light-theme');
            localStorage.setItem('theme', 'light');
            toggleBtn.innerHTML = '<i data-lucide="moon" class="lucide-icon"></i>';
        }
        if (window.lucide) lucide.createIcons();
        if (typeof lastChartsData !== 'undefined' && lastChartsData) {
            renderCharts(lastChartsData);
        }
    });
}

// Magnific Lightbox Zoom Functions
window.openMagnificZoom = function(url, caption) {
    const modal = document.getElementById('magnificZoomModal');
    const img = document.getElementById('magnificZoomImg');
    const captionEl = document.getElementById('magnificZoomCaption');
    
    if (modal && img) {
        img.src = url;
        if (captionEl) {
            captionEl.textContent = caption || 'Qiplo Presentation Deck Image View';
        }
        modal.classList.remove('hidden');
    }
};

window.closeMagnificZoom = function() {
    const modal = document.getElementById('magnificZoomModal');
    if (modal) {
        modal.classList.add('hidden');
    }
};

window.openToolInfo = function() {
    const modal = document.getElementById('toolInfoModal');
    if (modal) {
        modal.classList.remove('hidden');
        if (window.lucide) window.lucide.createIcons();
    }
};

window.closeToolInfo = function() {
    const modal = document.getElementById('toolInfoModal');
    if (modal) {
        modal.classList.add('hidden');
    }
};

// -------------------------------------------------------------
// Enterprise Features Logic
// -------------------------------------------------------------

function applyRolePermissions(role) {
    const tabAccess = {
        executive: ['overview', 'actions', 'customers', 'business', 'presentation', 'guide', 'copilot'],
        manager: ['overview', 'actions', 'customers', 'business', 'presentation', 'guide', 'copilot'],
        sales: ['overview', 'customers', 'business', 'presentation', 'copilot'],
        support: ['overview', 'actions', 'customers', 'guide', 'copilot']
    };
    const routeMap = {
        '/dashboard': 'overview',
        '/actions': 'actions',
        '/business': 'business',
        '/presentation': 'presentation',
        '/guide': 'guide'
    };
    const currentPath = window.location.pathname;
    const allowed = tabAccess[role.toLowerCase()] || tabAccess['executive'];
    let activeTab = routeMap[currentPath] || localStorage.getItem('active_tab') || 'overview';
    
    document.querySelectorAll('.studioTabs .tab').forEach(tab => {
        const tabName = tab.dataset.tab;
        const isAllowed = allowed.includes(tabName);
        tab.classList.toggle('hidden', !isAllowed);
        if (!isAllowed && tab.classList.contains('active')) {
            tab.classList.remove('active');
            const tabBody = document.getElementById(`tab-${tabName}`);
            if (tabBody) tabBody.classList.add('hidden');
            activeTab = 'overview';
        }
    });
    
    const targetTab = document.querySelector(`.studioTabs .tab[data-tab="${activeTab}"]`);
    if (targetTab) {
        targetTab.classList.add('active');
        const tabBody = document.getElementById(`tab-${activeTab}`);
        if (tabBody) tabBody.classList.remove('hidden');
    }
    localStorage.setItem('active_tab', activeTab);
}

async function loadEnterpriseFeatures() {
    try {
        const select = document.getElementById('assignCustomerSelect');
        if (select) {
            const currentSelected = select.value;
            select.innerHTML = predictionData.length 
                ? predictionData.map(c => `<option value="${c.customer_id}">${c.customer_id} (Risk: ${Math.round((c.predicted_probability || 0) * 100)}%)</option>`).join('')
                : '<option value="">No accounts available</option>';
            if (currentSelected && predictionData.some(c => c.customer_id === currentSelected)) {
                select.value = currentSelected;
            }
        }

        const assRes = await safeFetch('/api/assignments/status');
        const assData = await assRes.json();
        const assignments = assData.assignments || [];
        
        window.csmAssignments = {};
        assignments.forEach(a => {
            window.csmAssignments[a.customer_id] = a;
        });

        if (select) {
            const customerId = select.value;
            const assignment = window.csmAssignments[customerId] || null;
            const csmInput = document.getElementById('assignCsmName');
            const statusSelect = document.getElementById('assignStatusSelect');
            const notesInput = document.getElementById('assignNotes');
            if (assignment) {
                if (csmInput) csmInput.value = assignment.csm_name || '';
                if (statusSelect) statusSelect.value = assignment.status || 'unassigned';
                if (notesInput) notesInput.value = assignment.notes || '';
            } else {
                if (csmInput) csmInput.value = '';
                if (statusSelect) statusSelect.value = 'unassigned';
                if (notesInput) notesInput.value = '';
            }
        }

        try {
            const alertsRes = await safeFetch('/api/alerts/config');
            const alertsData = await alertsRes.json();
            const slackInput = document.getElementById('alertSlackWebhook');
            const emailInput = document.getElementById('alertEmailRecipient');
            if (slackInput) slackInput.value = alertsData.slack_webhook_url || '';
            if (emailInput) emailInput.value = alertsData.alert_email_recipient || '';
        } catch (e) {
            console.error('Failed to load alert channel settings:', e);
        }

        const abRes = await safeFetch('/api/abtests/list');
        const abData = await abRes.json();
        const campaigns = abData.campaigns || [];
        const abContainer = document.getElementById('abTestList');
        if (abContainer) {
            abContainer.innerHTML = campaigns.length
                ? campaigns.map(c => `
                    <div style="border-bottom: 1px solid var(--border); padding: 6px 0; display: flex; justify-content: space-between; align-items: center; gap: 10px;">
                        <div>
                            <strong>${c.campaign_name}</strong>
                            <div style="font-size: 0.7rem; color: var(--muted);">Size: ${c.sample_size} | Date: ${c.start_date}</div>
                        </div>
                        <div style="text-align: right;">
                            <span class="badge ${c.actual_churn_rate < c.predicted_churn_rate ? 'success' : 'warning'}" style="font-size: 0.72rem; padding: 2px 6px;">
                                ${Math.round(c.actual_churn_rate * 100)}% vs ${Math.round(c.predicted_churn_rate * 100)}%
                            </span>
                            <div style="font-size: 0.72rem; color: var(--accent); font-weight: 700;">${c.outcome}</div>
                        </div>
                    </div>
                `).join('')
                : '<div style="color: var(--muted); font-size: 0.8rem; text-align: center;">No logged campaigns yet.</div>';
        }

        const auditRes = await safeFetch('/api/audit/logs');
        const auditData = await auditRes.json();
        const logs = auditData.logs || [];
        const logContainer = document.getElementById('auditLogContainer');
        if (logContainer) {
            logContainer.innerHTML = logs.length
                ? logs.map(l => `
                    <div style="border-left: 2px solid var(--accent); padding-left: 8px; margin-bottom: 4px;">
                        <span style="color: var(--accent-2); font-weight: 700;">[${l.user_role}]</span> 
                        <span>${l.action}</span>
                        ${l.target_customer ? `<span style="color: var(--warning); font-weight: 700;">(Target: ${l.target_customer})</span>` : ''}
                        <div style="font-size: 0.65rem; color: var(--muted);">${new Date(l.timestamp).toLocaleTimeString()} | ${new Date(l.timestamp).toLocaleDateString()}</div>
                    </div>
                `).join('')
                : '<div style="color: var(--muted);">No compliance records found.</div>';
        }
        
        const crmRes = await safeFetch('/api/crm/status');
        const crmData = await crmRes.json();
        const activeCrms = (crmData.integrations || []).map(i => i.platform.toUpperCase()).join(', ');
        const activeLabel = document.getElementById('activeCrmStreams');
        if (activeLabel) {
            activeLabel.innerHTML = activeCrms ? `<span class="badge success" style="padding: 2px 8px;">${activeCrms} Connected (Active API Stream)</span>` : 'None (Manual CSV uploads default)';
        }

    } catch (err) {
        console.error('Failed to load enterprise dashboard components:', err);
    }
}

function setupEnterpriseListeners() {
    const tabCrm = document.getElementById('intTabCrm');
    const tabReport = document.getElementById('intTabReport');
    const tabAlerts = document.getElementById('intTabAlerts');
    const subCrm = document.getElementById('crmSubTabBody');
    const subReport = document.getElementById('schedulerSubTabBody');
    const subAlerts = document.getElementById('alertsSubTabBody');
    
    if (tabCrm && tabReport && tabAlerts && subCrm && subReport && subAlerts) {
        tabCrm.addEventListener('click', () => {
            tabCrm.style.color = 'var(--accent-2)';
            tabReport.style.color = 'var(--muted)';
            tabAlerts.style.color = 'var(--muted)';
            subCrm.classList.remove('hidden');
            subReport.classList.add('hidden');
            subAlerts.classList.add('hidden');
        });
        tabReport.addEventListener('click', () => {
            tabReport.style.color = 'var(--accent-2)';
            tabCrm.style.color = 'var(--muted)';
            tabAlerts.style.color = 'var(--muted)';
            subReport.classList.remove('hidden');
            subCrm.classList.add('hidden');
            subAlerts.classList.add('hidden');
        });
        tabAlerts.addEventListener('click', () => {
            tabAlerts.style.color = 'var(--accent-2)';
            tabCrm.style.color = 'var(--muted)';
            tabReport.style.color = 'var(--muted)';
            subAlerts.classList.remove('hidden');
            subCrm.classList.add('hidden');
            subReport.classList.add('hidden');
        });
    }

    const assignCustomerSelect = document.getElementById('assignCustomerSelect');
    if (assignCustomerSelect) {
        assignCustomerSelect.addEventListener('change', () => {
            const customerId = assignCustomerSelect.value;
            const assignment = (window.csmAssignments && window.csmAssignments[customerId]) || null;
            const csmInput = document.getElementById('assignCsmName');
            const statusSelect = document.getElementById('assignStatusSelect');
            const notesInput = document.getElementById('assignNotes');
            if (assignment) {
                if (csmInput) csmInput.value = assignment.csm_name || '';
                if (statusSelect) statusSelect.value = assignment.status || 'unassigned';
                if (notesInput) notesInput.value = assignment.notes || '';
            } else {
                if (csmInput) csmInput.value = '';
                if (statusSelect) statusSelect.value = 'unassigned';
                if (notesInput) notesInput.value = '';
            }
        });
    }

    const assignForm = document.getElementById('csmAssignForm');
    if (assignForm) {
        assignForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            AudioFeedback.click();
            const customer_id = document.getElementById('assignCustomerSelect').value;
            const csm_name = document.getElementById('assignCsmName').value;
            const status = document.getElementById('assignStatusSelect').value;
            const notes = document.getElementById('assignNotes').value;
            
            try {
                const res = await safeFetch('/api/assignments/assign', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ customer_id, csm_name, status, notes })
                });
                const payload = await res.json();
                if (payload.status === 'ok') {
                    alert('Assignment saved and logged to Compliance Audit Trails successfully.');
                    await loadEnterpriseFeatures();
                    renderRows();
                } else {
                    alert(payload.error || 'Failed to save notes.');
                }
            } catch (err) {
                alert('Save failed: ' + err);
            }
        });
    }

    const triggerSlaBtn = document.getElementById('triggerSlaAlertBtn');
    if (triggerSlaBtn) {
        triggerSlaBtn.addEventListener('click', async () => {
            AudioFeedback.click();
            const customer_id = document.getElementById('assignCustomerSelect').value;
            const csm_name = document.getElementById('assignCsmName').value || 'Customer Success Bot';
            
            if (!customer_id) {
                alert('Select an active customer first.');
                return;
            }

            try {
                const res = await safeFetch('/api/alerts/fire', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ customer_id, csm_name })
                });
                const payload = await res.json();
                if (payload.status === 'ok') {
                    alert(`🚨 SLA Webhook Fired Successfully!\n\nPayload:\n${JSON.stringify(payload.payload, null, 2)}`);
                    await loadEnterpriseFeatures();
                } else {
                    alert(payload.error || 'Failed to fire SLA Alert.');
                }
            } catch (err) {
                alert('Webhook fire failed: ' + err);
            }
        });
    }

    const crmConnectBtn = document.getElementById('crmConnectBtn');
    if (crmConnectBtn) {
        crmConnectBtn.addEventListener('click', async () => {
            AudioFeedback.click();
            const platform = document.getElementById('crmPlatformSelect').value;
            const api_key = document.getElementById('crmApiKey').value;
            
            if (!api_key) {
                alert('Please enter your API Key or connection token.');
                return;
            }

            try {
                const res = await safeFetch('/api/crm/integrate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ platform, api_key })
                });
                const payload = await res.json();
                if (payload.status === 'ok') {
                    alert(payload.message || 'CRM synchronized.');
                    await loadDashboard();
                } else {
                    alert(payload.error || 'Connection failed.');
                }
            } catch (err) {
                alert('Connection failed: ' + err);
            }
        });
    }

    const schedulerBtn = document.getElementById('schedulerBtn');
    if (schedulerBtn) {
        schedulerBtn.addEventListener('click', async () => {
            AudioFeedback.click();
            const email = document.getElementById('reportEmail').value;
            const frequency = document.getElementById('reportFreq').value;
            const format = document.getElementById('reportFormat').value;
            
            if (!email || !email.includes('@')) {
                alert('Please enter a valid recipient email address.');
                return;
            }

            try {
                const res = await safeFetch('/api/reports/schedule', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, frequency, format })
                });
                const payload = await res.json();
                if (payload.status === 'ok') {
                    alert(payload.message || 'Report scheduled.');
                    await loadEnterpriseFeatures();
                } else {
                    alert(payload.error || 'Failed to schedule.');
                }
            } catch (err) {
                alert('Scheduling failed: ' + err);
            }
        });
    }

    const saveAlertChannelsBtn = document.getElementById('saveAlertChannelsBtn');
    if (saveAlertChannelsBtn) {
        saveAlertChannelsBtn.addEventListener('click', async () => {
            AudioFeedback.click();
            const slack_webhook_url = document.getElementById('alertSlackWebhook').value;
            const alert_email_recipient = document.getElementById('alertEmailRecipient').value;
            
            try {
                const res = await safeFetch('/api/alerts/config', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ slack_webhook_url, alert_email_recipient })
                });
                const payload = await res.json();
                if (payload.status === 'ok') {
                    alert(payload.message || 'Alert configurations saved.');
                    await loadEnterpriseFeatures();
                } else {
                    alert(payload.error || 'Failed to save alert settings.');
                }
            } catch (err) {
                alert('Save failed: ' + err);
            }
        });
    }

    const abForm = document.getElementById('abTestForm');
    if (abForm) {
        abForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            AudioFeedback.click();
            const campaign_name = document.getElementById('abCampaignName').value;
            const sample_size = document.getElementById('abSampleSize').value;
            const predicted_churn_rate = document.getElementById('abPredRate').value;
            const actual_churn_rate = document.getElementById('abActRate').value;
            const outcome = Number(actual_churn_rate) < Number(predicted_churn_rate) ? 'Outperformed Predictions' : 'Met Expectations';

            try {
                const res = await safeFetch('/api/abtests/log', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ campaign_name, sample_size, predicted_churn_rate, actual_churn_rate, outcome })
                });
                const payload = await res.json();
                if (payload.status === 'ok') {
                    alert('A/B campaign outcome logged successfully.');
                    abForm.reset();
                    await loadEnterpriseFeatures();
                } else {
                    alert(payload.error || 'Failed to log campaign.');
                }
            } catch (err) {
                alert('Submit failed: ' + err);
            }
        });
    }
}

function setupDemoToggle() {
    const toggleDemoBtn = document.getElementById('toggleDemoBtn');
    const toggleCustomBtn = document.getElementById('toggleCustomBtn');

    if (toggleDemoBtn && toggleCustomBtn) {
        toggleDemoBtn.addEventListener('click', async () => {
            AudioFeedback.click();
            toggleDemoBtn.classList.add('active');
            toggleCustomBtn.classList.remove('active');
            try {
                const res = await safeFetch('/api/demo/set-mode', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ mode: 'demo' })
                });
                if (res.ok) {
                    await loadDashboard();
                    await fetchSources();
                }
            } catch (err) {
                console.error('Failed to set demo mode:', err);
            }
        });

        toggleCustomBtn.addEventListener('click', async () => {
            AudioFeedback.click();
            toggleDemoBtn.classList.remove('active');
            toggleCustomBtn.classList.add('active');
            try {
                const res = await safeFetch('/api/demo/set-mode', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ mode: 'custom' })
                });
                if (res.ok) {
                    await loadDashboard();
                    await fetchSources();
                }
            } catch (err) {
                console.error('Failed to set custom mode:', err);
            }
        });
    }
}

window.exportAuditLogs = function() {
    window.location.href = `/api/compliance/audit/export?role=${currentAuthorizedRole}`;
};

document.addEventListener('DOMContentLoaded', () => {
    const rs = document.getElementById('roleSelect');
    if (rs) rs.value = currentAuthorizedRole;

    setupThemeToggle();
    setupBusinessGuide();
    setupEnterpriseListeners();
    setupDemoToggle();
    if (window.lucide) lucide.createIcons();
});
