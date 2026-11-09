import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace setCalendarFilter to include the calculations and map button
old_fn = """    window.setCalendarFilter = function(date, type, textDesc) {
        window.calendarFilter = { date, type, textDesc };
        document.getElementById('status-filter').value = 'all'; // Reset general filter
        document.getElementById('search-input').value = '';     // Clear search
        document.getElementById('calendar-filter-indicator').style.display = 'flex';
        document.getElementById('cf-details').textContent = `${textDesc} (${type === 'Atendido' ? 'Ya Atendidos' : type})`;
        renderTable();
        // Scroll to table safely
        const tableEl = document.querySelector('.table-container') || document.querySelector('table');
        if (tableEl) {
            tableEl.scrollIntoView({ behavior: 'smooth' });
        }
    };"""

new_fn = """    window.setCalendarFilter = function(date, type, textDesc) {
        window.calendarFilter = { date, type, textDesc };
        document.getElementById('status-filter').value = 'all'; // Reset general filter
        document.getElementById('search-input').value = '';     // Clear search
        document.getElementById('calendar-filter-indicator').style.display = 'flex';
        document.getElementById('cf-details').textContent = `${textDesc} (${type === 'Atendido' ? 'Ya Atendidos' : type})`;
        
        // Calcular Resumen Financiero
        const filtered = clients.filter(c => {
            if (c.fecha !== date) return false;
            if (type === 'Mañana' || type === 'Tarde') {
                return c.turno === type && c.situacion !== 'Atendido';
            }
            if (type === 'Atendido') {
                return c.situacion === 'Atendido' || c.desembolso === 'Desembolsado';
            }
            return true;
        });

        let proyectado = 0;
        let desembolsado = 0;
        filtered.forEach(c => {
            let mStr = String(c.monto || '0').replace(/[^0-9.,-]/g, '');
            if (mStr.lastIndexOf(',') > mStr.lastIndexOf('.')) mStr = mStr.replace(/\\./g, '').replace(',', '.');
            else mStr = mStr.replace(/,/g, '');
            const val = parseFloat(mStr) || 0;
            
            proyectado += val;
            if(c.desembolso === 'Desembolsado' || c.situacion === 'Atendido') desembolsado += val;
        });
        
        document.getElementById('cf-proyectado').textContent = 'S/ ' + proyectado.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
        document.getElementById('cf-desembolsado').textContent = 'S/ ' + desembolsado.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
        
        // Generar Ruta
        const btnRoute = document.getElementById('btn-route-day');
        const lugares = filtered.map(c => c.lugar).filter(l => l && l.trim() !== '-');
        if (lugares.length > 0 && btnRoute) {
            btnRoute.style.display = 'block';
            const baseUrl = 'https://www.google.com/maps/dir/';
            const routeUrl = baseUrl + lugares.map(l => encodeURIComponent(l)).join('/');
            btnRoute.onclick = () => window.open(routeUrl, '_blank');
        } else if (btnRoute) {
            btnRoute.style.display = 'none';
        }
        
        renderTable();
        // Scroll to table safely
        const tableEl = document.querySelector('.table-container') || document.querySelector('table');
        if (tableEl) {
            tableEl.scrollIntoView({ behavior: 'smooth' });
        }
    };"""

if old_fn in html:
    html = html.replace(old_fn, new_fn)
    print("Replaced successfully")
else:
    print("Could not find the old function text exactly. Please check.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
