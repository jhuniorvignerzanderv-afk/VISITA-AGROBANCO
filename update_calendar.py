import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update the calendar-filter-indicator HTML to hold the financial summary and route button
indicator_old = """    <div id="calendar-filter-indicator" style="display: none; background-color: #fff3e0; color: #e65100; padding: 12px; border-radius: 8px; border: 1px solid #ffcc80; margin-bottom: 15px; justify-content: space-between; align-items: center; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
        <div><strong>🔍 Filtrando desde el Calendario:</strong> Mostrando clientes para <span id="cf-details" style="font-weight: bold; color: #c2185b;">---</span></div>
        <button onclick="clearCalendarFilter()" style="background: #e65100; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer; font-weight: bold;">✕ Quitar Filtro</button>
    </div>"""

indicator_new = """    <div id="calendar-filter-indicator" style="display: none; background-color: #fff3e0; color: #e65100; padding: 12px; border-radius: 8px; border: 1px solid #ffcc80; margin-bottom: 15px; flex-wrap: wrap; gap: 10px; justify-content: space-between; align-items: center; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
        <div style="flex: 1; min-width: 250px;">
            <strong>🔍 Filtrando desde el Calendario:</strong> <span id="cf-details" style="font-weight: bold; color: #c2185b;">---</span>
            <div style="margin-top: 5px; font-size: 13px; color: #d84315;">
                💰 Proyectado: <strong id="cf-proyectado">S/ 0.00</strong> | ✅ Desembolsado: <strong id="cf-desembolsado" style="color: #2e7d32;">S/ 0.00</strong>
            </div>
        </div>
        <div style="display: flex; gap: 10px;">
            <button id="btn-route-day" style="background: #2196f3; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-weight: bold; display: none;">🗺️ Ruta del Día</button>
            <button onclick="clearCalendarFilter()" style="background: #e65100; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-weight: bold;">✕ Quitar Filtro</button>
        </div>
    </div>"""
html = html.replace(indicator_old, indicator_new)

# 2. Update renderCalendarDashboard to calculate the amounts and add it to the card.
card_html_old = """                <h3>${dayName} ${dayNum} ${monthName}</h3>
                <div style="font-size: 12px; margin-bottom: 8px; color: #555; border-bottom: 1px solid #eee; padding-bottom: 5px;">
                    Total a visitar: <strong>${totalVisits}</strong>
                </div>"""

card_html_new = """                <h3>${dayName} ${dayNum} ${monthName}</h3>
                <div style="font-size: 12px; margin-bottom: 8px; color: #555; border-bottom: 1px solid #eee; padding-bottom: 5px;">
                    Total a visitar: <strong>${totalVisits}</strong><br>
                    <span style="color: #2e7d32; font-weight: bold;">💰 S/ ${totalMontoDia.toFixed(2)}</span>
                </div>"""

logic_old = """            const numManana = visits.filter(c => c.turno === 'Mañana').length;
            const numTarde = visits.filter(c => c.turno === 'Tarde').length;"""
            
logic_new = """            const numManana = visits.filter(c => c.turno === 'Mañana').length;
            const numTarde = visits.filter(c => c.turno === 'Tarde').length;
            const totalMontoDia = visits.reduce((sum, c) => sum + (parseFloat(c.monto) || 0), 0);"""

html = html.replace(logic_old, logic_new)
html = html.replace(card_html_old, card_html_new)

# 3. Update filterByDate to calculate the daily amounts for the indicator and build the maps route.
filter_old = """    window.filterByDate = function(dateStr, formattedDate) {
        document.getElementById('search-input').value = '';
        document.getElementById('status-filter').value = 'all';
        
        const filtered = clients.filter(c => c.fecha === dateStr);
        document.getElementById('cf-details').textContent = formattedDate;
        document.getElementById('calendar-filter-indicator').style.display = 'flex';"""
        
filter_new = """    window.filterByDate = function(dateStr, formattedDate) {
        document.getElementById('search-input').value = '';
        document.getElementById('status-filter').value = 'all';
        
        const filtered = clients.filter(c => c.fecha === dateStr);
        document.getElementById('cf-details').textContent = formattedDate;
        
        // Calcular Resumen Financiero
        const proyectado = filtered.reduce((sum, c) => sum + (parseFloat(c.monto) || 0), 0);
        const desembolsado = filtered.filter(c => c.desembolso === 'Desembolsado').reduce((sum, c) => sum + (parseFloat(c.monto) || 0), 0);
        
        document.getElementById('cf-proyectado').textContent = 'S/ ' + proyectado.toFixed(2);
        document.getElementById('cf-desembolsado').textContent = 'S/ ' + desembolsado.toFixed(2);
        
        // Generar Ruta
        const btnRoute = document.getElementById('btn-route-day');
        const lugares = filtered.map(c => c.lugar).filter(l => l && l.trim() !== '-');
        if (lugares.length > 0) {
            btnRoute.style.display = 'block';
            const baseUrl = 'https://www.google.com/maps/dir/';
            const routeUrl = baseUrl + lugares.map(l => encodeURIComponent(l)).join('/');
            btnRoute.onclick = () => window.open(routeUrl, '_blank');
        } else {
            btnRoute.style.display = 'none';
        }
        
        document.getElementById('calendar-filter-indicator').style.display = 'flex';"""

html = html.replace(filter_old, filter_new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
