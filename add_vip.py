import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add VIP Button
controls_old = """                <button id="btn-group-location" class="btn" style="background: #607d8b; color: white; font-size: 13px; padding: 8px 12px; border-radius: 4px;" onclick="toggleGroupLocation()">🗺️ Agrupar por Zona</button>
                <select id="status-filter" style="padding: 8px; border: 1px solid #ccc; border-radius: 4px; outline: none; background: white; flex: 1; min-width: 150px;">"""
controls_new = """                <button id="btn-vip" class="btn" style="background: #ffc107; color: #333; font-weight: bold; font-size: 13px; padding: 8px 12px; border-radius: 4px;" onclick="toggleVIP()">⭐ VIP</button>
                <button id="btn-group-location" class="btn" style="background: #607d8b; color: white; font-size: 13px; padding: 8px 12px; border-radius: 4px;" onclick="toggleGroupLocation()">🗺️ Agrupar por Zona</button>
                <select id="status-filter" style="padding: 8px; border: 1px solid #ccc; border-radius: 4px; outline: none; background: white; flex: 1; min-width: 150px;">"""
html = html.replace(controls_old, controls_new)

# 2. Add VIP Logic in JS
vip_js = """
    window.isVIPMode = false;
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
    };
"""
html = html.replace('// --- NUEVAS MEJORAS JS ---', vip_js + '\n    // --- NUEVAS MEJORAS JS ---')

# 3. Add VIP filter in renderTable
render_sort_old = """        filtered.sort((a, b) => {"""

vip_filter = """        // FILTRO VIP
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
            if (window.isVIPMode) return 0; // Skip other sorting if VIP is active
"""
html = html.replace(render_sort_old, vip_filter)


# 4. Highlight VIP rows in table
row_render_old = """                const tr = document.createElement('tr');
                
                const todayForHighlight = new Date();"""
                
row_render_new = """                const tr = document.createElement('tr');
                
                // VIP Highlight
                let mStrCheck = String(c.monto || '0').replace(/[^0-9.,-]/g, '');
                if (mStrCheck.lastIndexOf(',') > mStrCheck.lastIndexOf('.')) mStrCheck = mStrCheck.replace(/\\./g, '').replace(',', '.');
                else mStrCheck = mStrCheck.replace(/,/g, '');
                const valCheck = parseFloat(mStrCheck) || 0;
                
                if (window.isVIPMode && valCheck >= window.vipThreshold) {
                    tr.style.border = '2px solid #ffc107';
                    tr.style.boxShadow = '0 0 10px rgba(255, 193, 7, 0.3)';
                }
                
                const todayForHighlight = new Date();"""
html = html.replace(row_render_old, row_render_new)


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
