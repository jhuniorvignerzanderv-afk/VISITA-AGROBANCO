import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Change Button Text
old_btn = """onclick="toggleVIP()">⭐ VIP</button>"""
new_btn = """onclick="togglePriority()">💸 Priorizar Montos</button>"""
html = html.replace(old_btn, new_btn)

# 2. Change JS Logic
old_js = """    window.isVIPMode = false;
    window.vipThreshold = 10000;
    window.toggleVIP = function() {
        const btn = document.getElementById('btn-vip');
        if (!window.isVIPMode) {
            const amt = prompt('¿A partir de qué monto (S/) se considera un Cliente VIP?', window.vipThreshold);
            if (amt !== null && !isNaN(parseFloat(amt))) {
                window.vipThreshold = parseFloat(amt);
                window.isVIPMode = true;
                btn.style.background = '#ff9800';
                btn.innerHTML = '❌ Quitar VIP';
                btn.style.color = 'white';
            }
        } else {
            window.isVIPMode = false;
            btn.style.background = '#ffc107';
            btn.innerHTML = '⭐ VIP';
            btn.style.color = '#333';
        }
        renderTable();
    };"""

new_js = """    window.isPriorityMode = false;
    window.togglePriority = function() {
        const btn = document.getElementById('btn-vip'); // keeping the same ID for ease
        window.isPriorityMode = !window.isPriorityMode;
        if (window.isPriorityMode) {
            btn.style.background = '#4caf50';
            btn.innerHTML = '❌ Quitar Prioridad';
            btn.style.color = 'white';
        } else {
            btn.style.background = '#ffc107';
            btn.innerHTML = '💸 Priorizar Montos';
            btn.style.color = '#333';
        }
        renderTable();
    };"""
html = html.replace(old_js, new_js)

# 3. Change renderTable Logic
old_render_sort = """        // FILTRO VIP
        if (window.isVIPMode) {
            filtered = filtered.filter(c => {
                let mStr = String(c.monto || '0').replace(/[^0-9.,-]/g, '');
                if (mStr.lastIndexOf(',') > mStr.lastIndexOf('.')) mStr = mStr.replace(/\\./g, '').replace(',', '.');
                else mStr = mStr.replace(/,/g, '');
                const val = parseFloat(mStr) || 0;
                return val >= window.vipThreshold;
            });
            // Sort VIPs by amount descending automatically
            filtered.sort((a, b) => {
                let mStrA = String(a.monto || '0').replace(/[^0-9.,-]/g, '');
                if (mStrA.lastIndexOf(',') > mStrA.lastIndexOf('.')) mStrA = mStrA.replace(/\\./g, '').replace(',', '.');
                else mStrA = mStrA.replace(/,/g, '');
                const valA = parseFloat(mStrA) || 0;
                
                let mStrB = String(b.monto || '0').replace(/[^0-9.,-]/g, '');
                if (mStrB.lastIndexOf(',') > mStrB.lastIndexOf('.')) mStrB = mStrB.replace(/\\./g, '').replace(',', '.');
                else mStrB = mStrB.replace(/,/g, '');
                const valB = parseFloat(mStrB) || 0;
                
                return valB - valA;
            });
        }
        
        filtered.sort((a, b) => {
            if (window.isVIPMode) return 0; // Skip other sorting if VIP is active"""

new_render_sort = """        // PRIORIZAR MONTOS
        filtered.sort((a, b) => {
            if (window.isPriorityMode) {
                let mStrA = String(a.monto || '0').replace(/[^0-9.,-]/g, '');
                if (mStrA.lastIndexOf(',') > mStrA.lastIndexOf('.')) mStrA = mStrA.replace(/\\./g, '').replace(',', '.');
                else mStrA = mStrA.replace(/,/g, '');
                const valA = parseFloat(mStrA) || 0;
                
                let mStrB = String(b.monto || '0').replace(/[^0-9.,-]/g, '');
                if (mStrB.lastIndexOf(',') > mStrB.lastIndexOf('.')) mStrB = mStrB.replace(/\\./g, '').replace(',', '.');
                else mStrB = mStrB.replace(/,/g, '');
                const valB = parseFloat(mStrB) || 0;
                
                // Si ambos tienen montos diferentes, ordenar por mayor monto
                if (valA !== valB) return valB - valA;
            }
"""
html = html.replace(old_render_sort, new_render_sort)

# 4. Remove VIP border highlight
old_highlight = """                if (window.isVIPMode && valCheck >= window.vipThreshold) {
                    tr.style.border = '2px solid #ffc107';
                    tr.style.boxShadow = '0 0 10px rgba(255, 193, 7, 0.3)';
                }"""
new_highlight = """                // If priority mode is on and the client has a high amount, we could highlight it, but sorting is enough.
                if (window.isPriorityMode && valCheck > 0) {
                    tr.style.borderLeft = '4px solid #4caf50';
                }"""
html = html.replace(old_highlight, new_highlight)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
