document.addEventListener('DOMContentLoaded', function () {
    const proxyEnabled = document.getElementById('proxyEnabled');
    const strategySelect = document.getElementById('strategySelect');
    const proxyId = document.getElementById('proxyId');
    const proxyUrl = document.getElementById('proxyUrl');
    const proxyProtocol = document.getElementById('proxyProtocol');
    const proxyCountry = document.getElementById('proxyCountry');
    const proxyLocation = document.getElementById('proxyLocation');
    const addProxyBtn = document.getElementById('addProxyBtn');
    const refreshPoolBtn = document.getElementById('refreshPoolBtn');
    const proxyTableBody = document.getElementById('proxyTableBody');

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    function formatNumber(num) {
        if (num === null || num === undefined) return '0';
        return Number(num).toLocaleString();
    }

    function renderPool() {
        fetch('/api/proxy/pool')
            .then(function (res) { return res.json(); })
            .then(function (data) {
                const pool = data.stats || [];
                proxyTableBody.innerHTML = '';

                if (!pool.length) {
                    proxyTableBody.innerHTML = '<tr><td colspan="9" class="empty-cell">No proxies configured</td></tr>';
                    return;
                }

                for (const proxy of pool) {
                    const row = document.createElement('tr');
                    const statusBadge = proxy.active
                        ? '<span class="badge badge-success">Active</span>'
                        : '<span class="badge badge-danger">Inactive</span>';

                    row.innerHTML = `
                        <td><strong>${escapeHtml(proxy.id)}</strong></td>
                        <td><code>${escapeHtml(proxy.protocol)}</code></td>
                        <td title="${escapeHtml(proxy.url)}">${escapeHtml(proxy.url)}</td>
                        <td>${escapeHtml(proxy.country || '—')}</td>
                        <td>${escapeHtml(proxy.location || '—')}</td>
                        <td>${statusBadge}</td>
                        <td>${formatNumber(proxy.total_requests || 0)}</td>
                        <td>${proxy.last_latency_ms ? proxy.last_latency_ms + ' ms' : '—'}</td>
                        <td>
                            <button class="ghost-btn small toggle-proxy" data-id="${escapeHtml(proxy.id)}" data-active="${proxy.active}">
                                ${proxy.active ? 'Disable' : 'Enable'}
                            </button>
                            <button class="ghost-btn small test-proxy" data-id="${escapeHtml(proxy.id)}">Test</button>
                            <button class="ghost-btn small delete-proxy" data-id="${escapeHtml(proxy.id)}">Delete</button>
                        </td>
                    `;
                    proxyTableBody.appendChild(row);
                }

                document.querySelectorAll('.toggle-proxy').forEach(function (btn) {
                    btn.addEventListener('click', function () {
                        const id = btn.dataset.id;
                        const active = btn.dataset.active === 'true';
                        fetch('/api/proxy/pool/' + encodeURIComponent(id) + '/toggle', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ active: !active })
                        })
                        .then(function () { renderPool(); });
                    });
                });

                document.querySelectorAll('.test-proxy').forEach(function (btn) {
                    btn.addEventListener('click', function () {
                        const id = btn.dataset.id;
                        btn.disabled = true;
                        btn.textContent = 'Testing...';
                        fetch('/api/proxy/test', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ id: id })
                        })
                        .then(function (res) { return res.json(); })
                        .then(function (data) {
                            btn.disabled = false;
                            btn.textContent = 'Test';
                            alert(data.status === 'ok'
                                ? 'Proxy OK\nLatency: ' + data.latency_ms + 'ms\nIP: ' + (data.response || 'unknown')
                                : 'Proxy FAILED\n' + (data.error || 'unknown error'));
                        })
                        .catch(function () {
                            btn.disabled = false;
                            btn.textContent = 'Test';
                            alert('Proxy test failed');
                        });
                    });
                });

                document.querySelectorAll('.delete-proxy').forEach(function (btn) {
                    btn.addEventListener('click', function () {
                        const id = btn.dataset.id;
                        if (confirm('Remove proxy ' + id + '?')) {
                            fetch('/api/proxy/pool/' + encodeURIComponent(id), { method: 'DELETE' })
                                .then(function () { renderPool(); });
                        }
                    });
                });
            });
    }

    function loadConfig() {
        fetch('/api/proxy/config')
            .then(function (res) { return res.json(); })
            .then(function (data) {
                proxyEnabled.checked = data.enabled;
                strategySelect.value = data.strategy;
            });
    }

    proxyEnabled.addEventListener('change', function () {
        fetch('/api/proxy/toggle', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ enabled: proxyEnabled.checked })
        });
    });

    strategySelect.addEventListener('change', function () {
        fetch('/api/proxy/strategy', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ strategy: strategySelect.value })
        });
    });

    addProxyBtn.addEventListener('click', function () {
        const id = proxyId.value.trim();
        const url = proxyUrl.value.trim();
        const protocol = proxyProtocol.value;
        const country = proxyCountry.value.trim();
        const location = proxyLocation.value.trim();

        if (!id || !url) {
            alert('Proxy ID and URL are required.');
            return;
        }

        fetch('/api/proxy/pool', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: id, url: url, protocol: protocol, country: country, location: location })
        })
        .then(function (res) { return res.json(); })
        .then(function (data) {
            if (data.error) {
                alert(data.error);
                return;
            }
            proxyId.value = '';
            proxyUrl.value = '';
            proxyCountry.value = '';
            proxyLocation.value = '';
            renderPool();
        });
    });

    refreshPoolBtn.addEventListener('click', function () {
        renderPool();
    });

    loadConfig();
    renderPool();
});
