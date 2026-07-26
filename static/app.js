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
let labelMapping = { high_risk: 'high_risk', low_risk: 'low_risk' };
let lastChartsData = null;

async function loadDashboard() {
    try {
        const role = document.getElementById('roleSelect').value;
        const apiKey = localStorage.getItem('at_ai_model_key') || localStorage.getItem('show_ai_model_key') || '';
        const response = await safeFetch(`/api/dashboard-state?role=${role}&model_key=${encodeURIComponent(apiKey)}`);
        const payload = await response.json();

        const summaryData = { summary: payload.summary };
        const predictionsPayload = { predictions: payload.predictions };
        const chartsData = payload.charts;
        const insightsData = payload.insights;
        const aiData = payload.ai_insights;
        const brandingData = payload.branding;

        predictionData = predictionsPayload.predictions || [];
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

        renderSourceMeta();
        renderRows();
        lastChartsData = chartsData;
        renderCharts(chartsData);
        renderInsights(insightsData);
        renderExecutiveSummary(insightsData);
        renderAiPanel(aiData);
        
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

    const filtered = filterValue === 'all'
        ? predictionData
        : predictionData.filter(item => item.prediction_label === filterValue);

    if (!filtered.length) {
        rows.innerHTML = `<tr><td colspan="${headers.length}" class="empty">No records to display yet. Upload a file to begin.</td></tr>`;
        return;
    }

    const cell = (value) => value === null || value === undefined || value === '' ? 'n/a' : value;
    filtered.forEach(item => {
        const probability = Number(item.predicted_probability || 0).toFixed(3);
        const labelClass = item.prediction_label === labelMapping.high_risk ? 'high' : 'low';
        const idVal = idCol ? cell(item[idCol]) : cell(item.customer_id);

        const tds = [`<td>${idVal}</td>`,
            `<td><span class="badge ${labelClass}">${item.prediction_label.replace('_', ' ')}</span></td>`,
            `<td>${probability}</td>`,
            ...extra.map(c => `<td>${cell(item[c])}</td>`)].join('');

        const row = document.createElement('tr');
        row.innerHTML = tds;
        rows.appendChild(row);
    });
}

function renderCharts(chartPayload) {
    const riskLabels = (chartPayload.charts || []).map(item => item.label);
    const riskValues = (chartPayload.charts || []).map(item => item.value);
    const signalLabels = (chartPayload.signals || []).map(item => item.label);
    const signalValues = (chartPayload.signals || []).map(item => item.value);

    if (riskChart) riskChart.destroy();
    if (signalChart) signalChart.destroy();

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

function renderInsights(insightsData) {
    const panel = document.getElementById('insightPanel');
    const recommendations = insightsData.recommendations || [];
    panel.innerHTML = recommendations.length
        ? recommendations.map(item => `<p>${item}</p>`).join('')
        : '<p>No insights available yet.</p>';
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
            await loadDashboard();
            await fetchSources();
        } else {
            if (status) {
                status.textContent = payload.message || 'Upload failed. Please try again.';
                status.className = 'status error';
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
    const savedTab = localStorage.getItem('active_tab') || 'overview';
    document.querySelectorAll('.tab').forEach(tab => {
        const isTarget = tab.dataset.tab === savedTab;
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
document.getElementById('roleSelect').addEventListener('change', loadDashboard);
document.getElementById('exportTableauBtn').addEventListener('click', () => {
    if (!predictionData || !predictionData.length) {
        alert("No prediction data available to export. Please upload a customer file first.");
        return;
    }
    window.open('/api/export/tableau', '_blank');
});
document.getElementById('exportPowerBiBtn').addEventListener('click', () => {
    if (!predictionData || !predictionData.length) {
        alert("No prediction data available to export. Please upload a customer file first.");
        return;
    }
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
                if (mediaSource === 'pixabay') {
                    const apiKey = '43875323-8c4d284adab817454f7623a88';
                    const res = await fetch(`https://pixabay.com/api/?key=${apiKey}&q=${encodeURIComponent(keyword)}&image_type=photo&per_page=5`);
                    const data = await res.json();
                    if (data.hits && data.hits.length > 0) {
                        urls = data.hits.slice(0, 4).map(h => h.webformatURL);
                    } else {
                        urls = [
                            `https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=600&q=80`,
                            `https://images.unsplash.com/photo-1579546929518-9e396f3cc809?auto=format&fit=crop&w=600&q=80`
                        ];
                    }
                } else if (mediaSource === 'pexels') {
                    urls = [
                        `https://images.pexels.com/photos/3183150/pexels-photo-3183150.jpeg?auto=compress&cs=tinysrgb&w=400`,
                        `https://images.pexels.com/photos/3183197/pexels-photo-3183197.jpeg?auto=compress&cs=tinysrgb&w=400`,
                        `https://images.pexels.com/photos/3182781/pexels-photo-3182781.jpeg?auto=compress&cs=tinysrgb&w=400`,
                        `https://images.pexels.com/photos/3183153/pexels-photo-3183153.jpeg?auto=compress&cs=tinysrgb&w=400`
                    ];
                } else if (mediaSource === 'openverse') {
                    const res = await fetch(`https://api.openverse.org/v1/images/?q=${encodeURIComponent(keyword)}`);
                    const data = await res.json();
                    if (data.results && data.results.length > 0) {
                        urls = data.results.slice(0, 4).map(r => r.url);
                    } else {
                        urls = [
                            `https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=600&q=80`,
                            `https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=600&q=80`
                        ];
                    }
                } else if (mediaSource === 'lottie') {
                    urls = [
                        `https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=600&q=80`,
                        `https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=600&q=80`,
                        `https://images.unsplash.com/photo-1542831371-29b0f74f9713?auto=format&fit=crop&w=600&q=80`,
                        `https://images.unsplash.com/photo-1515621061946-eff1c2a352bd?auto=format&fit=crop&w=600&q=80`
                    ];
                } else {
                    urls = [
                        `https://images.unsplash.com/featured/300x200?sig=${Math.floor(Math.random()*1000)}&${encodeURIComponent(keyword)}`,
                        `https://images.unsplash.com/featured/300x200?sig=${Math.floor(Math.random()*1000)}&${encodeURIComponent(keyword)}`,
                        `https://images.unsplash.com/featured/300x200?sig=${Math.floor(Math.random()*1000)}&${encodeURIComponent(keyword)}`,
                        `https://images.unsplash.com/featured/300x200?sig=${Math.floor(Math.random()*1000)}&${encodeURIComponent(keyword)}`
                    ];
                }
            } catch (err) {
                console.error("Media search error, falling back to Unsplash", err);
                urls = [
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
    genBtn.textContent = 'Compiling...';
    status.textContent = 'Analyzing active data sources and formatting professional slide templates...';

    try {
        const apiKey = localStorage.getItem('gemini_api_key') || '';
        const customPrompt = document.getElementById('presCustomPrompt') ? document.getElementById('presCustomPrompt').value : '';
        const slideCountEl = document.getElementById('presSlideCount');
        const numSlides = slideCountEl ? parseInt(slideCountEl.value) : 5;

        const res = await fetch('/api/presentation', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ api_key: apiKey, custom_prompt: customPrompt, num_slides: numSlides })
        });
        const payload = await res.json();

        if (res.ok && payload.slides) {
            presentationSlides = payload.slides;
            currentSlideIndex = 0;

            renderSlides(payload.slides);

            viewport.classList.remove('hidden');
            prevBtn.classList.remove('hidden');
            nextBtn.classList.remove('hidden');
            if (fullscreenBtn) fullscreenBtn.classList.remove('hidden');
            const printBtn = document.getElementById('printPresBtn');
            if (printBtn) printBtn.classList.remove('hidden');
            if (downloadBtn) downloadBtn.classList.remove('hidden');
            const editorPanel = document.getElementById('slideEditorPanel');
            if (editorPanel) editorPanel.classList.remove('hidden');
            status.classList.add('hidden');

            updateSlideView();
        } else {
            status.textContent = 'Failed to generate presentation deck: ' + (payload.error || 'Unknown error');
            genBtn.disabled = false;
            genBtn.textContent = 'Generate Deck';
        }
    } catch (e) {
        status.textContent = 'Could not reach server to generate presentation.';
        genBtn.disabled = false;
        genBtn.textContent = 'Generate Deck';
    } finally {
        genBtn.disabled = false;
    }
}

function renderSlides(slides) {
    const viewport = document.getElementById('slideViewport');
    if (!viewport) return;

    const imageStyles = {
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

    const styleSelect = document.getElementById('presImageStyle');
    const selectedStyle = styleSelect ? styleSelect.value : 'corporate';
    const activeList = imageStyles[selectedStyle] || imageStyles.corporate;

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
                            <h1 style="font-size: 2.2rem; margin: 0 0 10px; line-height: 1.15; background: linear-gradient(135deg, #00F5FF, #FF007F); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">${slide.title}</h1>
                            <p class="slideSubtitle" style="font-size: 1rem; color: var(--muted); margin: 0 0 16px; line-height: 1.5;">${slide.subtitle}</p>
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
            const listHtml = (slide.bullets || []).map(b => `<li>${b}</li>`).join('');
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
                            <h2 style="margin-top: 0; font-size: 1.3rem; color: var(--text);">${slide.title}</h2>
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
            const listHtml = (slide.bullets || []).map(b => `
                <div class="riskComparisonCard" style="display: flex; align-items: center; gap: 12px; padding: 10px 14px; background: rgba(255,255,255,0.02); border: 1px solid var(--border); border-radius: 10px;">
                    <div class="cardIcon" style="font-size:1.1rem; color: var(--accent);"><i data-lucide="target" class="lucide-icon"></i></div>
                    <div class="cardContent" style="font-size:0.88rem; color:var(--text);">
                        <p style="margin:0;">${b}</p>
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
                            <h2 style="margin: 0 0 6px; font-size: 1.3rem;">${slide.title}</h2>
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
            const playbookCards = (slide.playbook || []).map(p => `
                <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); border-left: 4px solid var(--${p.type || 'primary'}); padding: 10px 12px; border-radius: 8px;">
                    <h4 style="margin: 0 0 3px; font-size: 0.88rem; color: var(--${p.type || 'primary'}); font-family: 'Outfit', sans-serif;">${p.title}</h4>
                    <p style="margin: 0; font-size: 0.8rem; color: var(--muted);">${p.desc}</p>
                </div>
            `).join('');
            contentHtml = `
                <div class="slideContent layout-playbook">
                    <div class="slideHeader">
                        <div class="presMiniLogo">Qiplo</div>
                        <span>Prescriptive Solutions & Action Matrix</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin: 8px 0 6px;">
                        <h2 style="margin: 0; font-size: 1.3rem;">${slide.title}</h2>
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
            const stepsHtml = (slide.steps || []).map((st, i) => `
                <div class="workflowStepCard" style="flex:1; background: rgba(255,255,255,0.02); border: 1px solid var(--border); padding: 10px; border-radius: 8px;">
                    <div class="workflowStepNum" style="font-weight:800; color:var(--primary); font-size:0.8rem; margin-bottom:3px;">STAGE 0${i+1}</div>
                    <div class="workflowStepContent">
                        <h4 style="margin:0 0 3px; font-size:0.85rem; color:#ffffff;">${st.title}</h4>
                        <p style="margin:0; font-size:0.78rem; color:var(--muted);">${st.description || st.desc || ''}</p>
                    </div>
                </div>
            `).join('');

            contentHtml = `
                <div class="slideContent layout-workflow">
                    <div class="slideHeader">
                        <div class="presMiniLogo">Qiplo</div>
                        <span>Interactive Customer Journey Workflow</span>
                    </div>
                    <h2 style="margin: 8px 0 4px; font-size: 1.3rem;">${slide.title}</h2>
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

function jumpToSlide(idx) {
    currentSlideIndex = idx;
    updateSlideView();
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

    const standaloneHtml = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Qiplo Executive Slide Deck</title>
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
            box-shadow: 0 12px 48px rgba(219, 39, 119, 0.2);
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
            transform: scale(0.95) translateY(10px);
            transition: opacity 0.5s ease, transform 0.5s ease;
            pointer-events: none;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 40px 60px;
            box-sizing: border-box;
        }

        .slide.active {
            opacity: 1;
            transform: scale(1) translateY(0);
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

        .layout-title h1 {
            font-size: 2.8rem;
            margin: 0 0 16px;
            color: #ffffff;
            font-weight: 800;
            background: linear-gradient(135deg, #ffffff, var(--accent-2));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .layout-title .slideSubtitle {
            font-size: 1.25rem;
            color: var(--muted);
            margin: 0;
            max-width: 700px;
        }

        .slideDecor {
            position: absolute;
            width: 120px;
            height: 4px;
            background: linear-gradient(90deg, var(--accent), var(--accent-2));
            bottom: calc(50% + 80px);
            border-radius: 2px;
        }

        .slideHeader {
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(61, 220, 132, 0.1);
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
            border-top: 1px solid rgba(61, 220, 132, 0.05);
            padding-top: 12px;
            font-size: 0.78rem;
            color: var(--muted);
        }

        .slideSplitBody {
            display: flex;
            gap: 40px;
            flex: 1;
            align-items: center;
            margin: 20px 0;
        }

        .slideLeftPane {
            flex: 0 0 260px;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .statCallout {
            background: var(--surface-2);
            border: 1px solid rgba(61, 220, 132, 0.1);
            padding: 16px;
            border-radius: var(--radius-sm);
            text-align: center;
        }

        .statCallout span {
            font-size: 0.7rem;
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            display: block;
            margin-bottom: 4px;
        }

        .statCallout h2 {
            margin: 0;
            font-size: 1.8rem;
            color: var(--accent-2);
        }

        .statCallout h4 {
            margin: 0;
            font-size: 1.1rem;
            color: #ffffff;
        }

        .slideRightPane {
            flex: 1;
        }

        .slideRightPane h2 {
            margin: 0 0 16px;
            font-size: 1.4rem;
            color: #ffffff;
        }

        .slideRightPane ul {
            margin: 0;
            padding-left: 20px;
        }

        .slideRightPane li {
            margin-bottom: 12px;
            font-size: 1rem;
            line-height: 1.5;
            color: var(--text);
        }

        .layout-grid h2 {
            margin: 20px 0 16px;
            font-size: 1.4rem;
            color: #ffffff;
        }

        .slideGridBody {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            flex: 1;
            margin-bottom: 20px;
        }

        .riskComparisonCard {
            background: var(--surface-2);
            border: 1px solid rgba(61, 220, 132, 0.1);
            border-radius: var(--radius-sm);
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .cardIcon {
            font-size: 1.5rem;
        }

        .cardContent p {
            margin: 0;
            font-size: 0.88rem;
            line-height: 1.55;
            color: var(--text);
        }

        .layout-workflow {
            display: flex;
            flex-direction: column;
            gap: 20px;
            justify-content: space-between;
        }
        .slideWorkflowBody {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            margin: 20px 0;
            width: 100%;
        }
        .workflowStepCard {
            flex: 1;
            background: var(--surface-2);
            border: 1px solid var(--border);
            border-radius: var(--radius-sm);
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            position: relative;
            box-shadow: var(--shadow);
            transition: all 0.3s ease;
        }
        .workflowStepNum {
            font-size: 1.5rem;
            font-weight: 800;
            color: var(--accent);
            line-height: 1;
        }
        .workflowStepContent h4 {
            margin: 0 0 6px;
            font-size: 0.95rem;
            color: #ffffff;
        }
        .workflowStepContent p {
            margin: 0;
            font-size: 0.8rem;
            line-height: 1.4;
            color: var(--muted);
        }
        .workflowConnector {
            font-size: 1.4rem;
            color: var(--accent-2);
        }

        .controls {
            position: absolute;
            bottom: 24px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 12px;
            align-items: center;
            background: rgba(10, 11, 14, 0.8);
            backdrop-filter: blur(8px);
            padding: 8px 16px;
            border-radius: 20px;
            border: 1px solid rgba(61, 220, 132, 0.15);
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
        }

        .controlBtn:hover {
            color: var(--accent-2);
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
        <div class="slideViewport">
            ${slidesHtml}
        </div>

        <div class="controls">
            <button class="controlBtn" onclick="changeSlide(-1)">&lsaquo;</button>
            <span class="slideNum" id="slideNum">Slide 1 of 3</span>
            <button class="controlBtn" onclick="changeSlide(1)">&rsaquo;</button>
        </div>
        
        <div class="helpText">Use Left/Right arrow keys to navigate</div>
    </div>

    <script>
        let currentSlide = 0;
        const slides = document.querySelectorAll('.slide');

        function updateSlides() {
            slides.forEach((slide, idx) => {
                slide.classList.remove('active');
                if (idx === currentSlide) {
                    slide.classList.add('active');
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

        updateSlides();
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

document.addEventListener('DOMContentLoaded', () => {
    setupThemeToggle();
    setupBusinessGuide();
    if (window.lucide) lucide.createIcons();
});
