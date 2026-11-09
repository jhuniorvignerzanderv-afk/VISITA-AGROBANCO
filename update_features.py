import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add CDNs
cdn_scripts = """    <script src="xlsx.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.5.28/jspdf.plugin.autotable.min.js"></script>"""
html = html.replace('    <script src="xlsx.js"></script>', cdn_scripts)

# 2. Add Dark Mode CSS & Today Row CSS
css_additions = """
        /* Dark Mode */
        body.dark-mode {
            --background-color: #121212;
            --text-color: #e0e0e0;
            --secondary-color: #2c2c2c;
            --border-color: #444;
            --container-bg: #1e1e1e;
            background-color: var(--background-color);
            color: var(--text-color);
        }
        body.dark-mode .container, body.dark-mode .calendar-card, body.dark-mode .modal-content {
            background-color: var(--container-bg);
            color: #e0e0e0;
            border-color: #333;
        }
        body.dark-mode th { background-color: #2c2c2c; color: #fff; }
        body.dark-mode tr:hover, body.dark-mode tbody tr:hover { background-color: #333; }
        body.dark-mode .btn-icon { background: #333; color: #e0e0e0; border-color: #555; }
        body.dark-mode input, body.dark-mode select { background-color: #2c2c2c; color: #fff; border-color: #555; }
        
        /* Highlight Today */
        .today-row { background-color: #fffde7 !important; border-left: 4px solid #fbc02d; }
        body.dark-mode .today-row { background-color: #3e3a24 !important; border-left: 4px solid #fbc02d; }
        
        /* Sortable Headers */
        th.sortable { cursor: pointer; user-select: none; }
        th.sortable:hover { background-color: #e0e0e0; }
        body.dark-mode th.sortable:hover { background-color: #444; }
"""
html = html.replace('    <style>', '    <style>' + css_additions)
# Update background variables usage in basic CSS
html = html.replace('background: white;', 'background: var(--container-bg, white);')
html = html.replace('background-color: #f9f9f9;', 'background-color: var(--background-color, #f9f9f9);')

# 3. Add Buttons (Dark mode, PDF)
buttons_replacement = """        <div>
            <button id="btn-toggle-dark" class="btn" style="background-color: #333; color: white;">🌙 Tema</button>
            <button id="btn-add-client" class="btn btn-primary">+ Agregar Cliente Manual</button>
            <button id="btn-export-pdf" class="btn" style="background-color: #d32f2f; color: white;">📄 PDF de Hoy</button>
            <button id="btn-export-excel" class="btn" style="background-color: #107c41; color: white;">Descargar Excel</button>
            <button id="btn-clear-all" class="btn btn-danger">Borrar Todo</button>
        </div>"""
html = re.sub(r'<div>\s*<button id="btn-add-client".*?</div>', buttons_replacement, html, flags=re.DOTALL)

# 4. Add Chart Canvas
chart_html = """
    <!-- DASHBOARD GRAFICOS -->
    <div style="display: flex; gap: 20px; margin-bottom: 20px; flex-wrap: wrap;">
        <div style="flex: 1; min-width: 300px; background: var(--container-bg, white); padding: 15px; border-radius: 8px; border: 1px solid var(--border-color, #ddd);">
            <h3 style="font-size: 14px; text-align: center; margin-bottom: 10px;">Distribución de Productos</h3>
            <canvas id="productChart" style="max-height: 250px;"></canvas>
        </div>
    </div>
    
    <div style="overflow-x: auto;">
"""
html = html.replace('    <div style="overflow-x: auto;">', chart_html, 1)

# 5. Update Table Headers for Sorting
headers_original = """                    <th>CLIENTE</th>
                    <th>DNI</th>
                    <th>N° DE TELEFONO</th>
                    <th>PRODUCTO</th>
                    <th>MONTO</th>
                    <th>LUGAR DE VISITA</th>
                    <th>FECHA DE VISITA</th>
                    <th>TURNO</th>
                    <th>SITUACION</th>
                    <th>ESTADO DESEMBOLSO</th>
                    <th>ACCIONES</th>"""
headers_new = """                    <th class="sortable" onclick="sortTable('cliente')">CLIENTE ↕️</th>
                    <th class="sortable" onclick="sortTable('dni')">DNI ↕️</th>
                    <th>N° DE TELEFONO</th>
                    <th class="sortable" onclick="sortTable('producto')">PRODUCTO ↕️</th>
                    <th class="sortable" onclick="sortTable('monto')">MONTO ↕️</th>
                    <th class="sortable" onclick="sortTable('lugar')">LUGAR DE VISITA ↕️</th>
                    <th class="sortable" onclick="sortTable('fecha')">FECHA DE VISITA ↕️</th>
                    <th class="sortable" onclick="sortTable('turno')">TURNO ↕️</th>
                    <th class="sortable" onclick="sortTable('situacion')">SITUACION ↕️</th>
                    <th>ESTADO DESEMBOLSO</th>
                    <th>ACCIONES</th>"""
html = html.replace(headers_original, headers_new)

# 6. Add JS features
js_additions = """
    // --- NUEVAS MEJORAS JS ---
    // 1. Dark Mode Toggle
    const btnToggleDark = document.getElementById('btn-toggle-dark');
    if (btnToggleDark) {
        btnToggleDark.addEventListener('click', () => {
            document.body.classList.toggle('dark-mode');
            const isDark = document.body.classList.contains('dark-mode');
            localStorage.setItem('darkMode', isDark);
            if(window.myChart) updateChart(); // Redraw chart for dark mode colors if needed
        });
        // Check saved preference
        if(localStorage.getItem('darkMode') === 'true') {
            document.body.classList.add('dark-mode');
        }
    }

    // 2. Export PDF
    const btnExportPdf = document.getElementById('btn-export-pdf');
    if (btnExportPdf) {
        btnExportPdf.addEventListener('click', () => {
            if (typeof jspdf === 'undefined') {
                alert('La librería PDF aún no ha cargado. Intenta de nuevo.');
                return;
            }
            
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF('landscape');
            
            // Filter clients for today
            const today = new Date();
            const todayStr = today.getFullYear() + '-' + String(today.getMonth() + 1).padStart(2, '0') + '-' + String(today.getDate()).padStart(2, '0');
            const todayClients = clients.filter(c => c.fecha === todayStr);
            
            if (todayClients.length === 0) {
                alert('No tienes visitas programadas para el día de hoy.');
                return;
            }
            
            doc.text(`Itinerario de Visitas - ${todayStr}`, 14, 15);
            
            const tableData = todayClients.map(c => [
                c.cliente, c.telefono, c.producto, c.lugar, c.turno, c.situacion, c.desembolso
            ]);
            
            doc.autoTable({
                head: [['CLIENTE', 'TELÉFONO', 'PRODUCTO', 'LUGAR', 'TURNO', 'SITUACIÓN', 'DESEMBOLSO']],
                body: tableData,
                startY: 20,
                styles: { fontSize: 9 }
            });
            
            doc.save(`Visitas_Hoy_${todayStr}.pdf`);
        });
    }

    // 3. Sorting logic
    let sortColumn = '';
    let sortAsc = true;
    window.sortTable = function(column) {
        if (sortColumn === column) {
            sortAsc = !sortAsc; // toggle
        } else {
            sortColumn = column;
            sortAsc = true;
        }
        
        clients.sort((a, b) => {
            let valA = a[column] ? a[column].toLowerCase() : '';
            let valB = b[column] ? b[column].toLowerCase() : '';
            
            if (column === 'monto') {
                valA = parseFloat(a[column]) || 0;
                valB = parseFloat(b[column]) || 0;
            }
            
            if (valA < valB) return sortAsc ? -1 : 1;
            if (valA > valB) return sortAsc ? 1 : -1;
            return 0;
        });
        
        saveAndRender();
    };

    // 4. Update Chart
    window.myChart = null;
    function updateChart() {
        const ctx = document.getElementById('productChart');
        if (!ctx) return;
        
        // Contar productos
        const productCounts = {};
        clients.forEach(c => {
            if(c.producto && c.producto !== '-') {
                productCounts[c.producto] = (productCounts[c.producto] || 0) + 1;
            }
        });
        
        const labels = Object.keys(productCounts);
        const data = Object.values(productCounts);
        
        if (window.myChart) {
            window.myChart.destroy();
        }
        
        const isDark = document.body.classList.contains('dark-mode');
        
        window.myChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels.length > 0 ? labels : ['Sin datos'],
                datasets: [{
                    data: data.length > 0 ? data : [1],
                    backgroundColor: data.length > 0 ? [
                        '#4caf50', '#2196f3', '#ff9800', '#f44336', '#9c27b0', '#00bcd4'
                    ] : ['#e0e0e0'],
                    borderWidth: 1,
                    borderColor: isDark ? '#1e1e1e' : '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: { color: isDark ? '#e0e0e0' : '#333' }
                    }
                }
            }
        });
    }
"""

html = html.replace('function renderTable() {', js_additions + '\n    function renderTable() {')
html = html.replace('renderCalendarDashboard();', 'renderCalendarDashboard();\n        updateChart();')

# Inject Maps Button in Table render and Today highlighting
table_row_old = """                const tr = document.createElement('tr');"""
table_row_new = """                const tr = document.createElement('tr');
                
                const todayForHighlight = new Date();
                const todayStrHighlight = todayForHighlight.getFullYear() + '-' + String(todayForHighlight.getMonth() + 1).padStart(2, '0') + '-' + String(todayForHighlight.getDate()).padStart(2, '0');
                if (c.fecha === todayStrHighlight) {
                    tr.classList.add('today-row');
                }
"""
html = html.replace(table_row_old, table_row_new)

lugar_td_old = "<td>${c.lugar || '-'}</td>"
lugar_td_new = "<td>${c.lugar || '-'}${(c.lugar && c.lugar !== '-') ? `<br><a href=\"https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(c.lugar)}\" target=\"_blank\" class=\"btn-icon\" style=\"margin-top:4px; font-size:10px;\" title=\"Ver en Maps\" onclick=\"event.stopPropagation();\">📍 Maps</a>` : ''}</td>"
html = html.replace(lugar_td_old, lugar_td_new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
