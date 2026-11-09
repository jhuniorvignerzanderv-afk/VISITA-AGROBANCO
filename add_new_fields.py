import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Table Headers
headers_old = """                    <th class="sortable" onclick="sortTable('situacion')">SITUACION ↕️</th>
                    <th>ESTADO DESEMBOLSO</th>
                    <th>ACCIONES</th>"""
headers_new = """                    <th class="sortable" onclick="sortTable('situacion')">SITUACION ↕️</th>
                    <th>ESTADO DESEMBOLSO</th>
                    <th>OBSERVACIONES</th>
                    <th>REFERENCIAS</th>
                    <th>ACCIONES</th>"""
html = html.replace(headers_old, headers_new)

# 2. Add Modal Form Fields
modal_fields_old = """            <div class="form-group">
                <label for="situacion">SITUACION</label>
                <select id="situacion">"""
modal_fields_new = """            <div class="form-group">
                <label for="observaciones">OBSERVACIONES</label>
                <textarea id="observaciones" rows="2" placeholder="Notas sobre la visita..."></textarea>
            </div>
            <div class="form-group" style="display: flex; gap: 10px;">
                <div style="flex: 1;">
                    <label>REF. PERSONAL (Nombre y Teléfono)</label>
                    <input type="text" id="ref_personal" placeholder="Ej: Juan Perez 999888777">
                </div>
                <div style="flex: 1;">
                    <label>REF. COMERCIAL (Nombre y Teléfono)</label>
                    <input type="text" id="ref_comercial" placeholder="Ej: Tienda Maria 999666333">
                </div>
            </div>
            <div class="form-group">
                <label for="situacion">SITUACION</label>
                <select id="situacion">"""
html = html.replace(modal_fields_old, modal_fields_new)

# 3. Add DOM Elements for new inputs
dom_old = """    const situacionInput = document.getElementById('situacion');
    const desembolsoInput = document.getElementById('desembolso');"""
dom_new = """    const situacionInput = document.getElementById('situacion');
    const desembolsoInput = document.getElementById('desembolso');
    const observacionesInput = document.getElementById('observaciones');
    const refPersonalInput = document.getElementById('ref_personal');
    const refComercialInput = document.getElementById('ref_comercial');"""
html = html.replace(dom_old, dom_new)

# 4. Save to clientData
save_old = """            situacion: situacionInput.value,
            desembolso: desembolsoInput.value
        };"""
save_new = """            situacion: situacionInput.value,
            desembolso: desembolsoInput.value,
            observaciones: observacionesInput.value.trim() || '',
            ref_personal: refPersonalInput.value.trim() || '',
            ref_comercial: refComercialInput.value.trim() || ''
        };"""
html = html.replace(save_old, save_new)

# 5. Load in editClient
load_old = """            situacionInput.value = client.situacion;
            desembolsoInput.value = client.desembolso || '-';
        } else {"""
load_new = """            situacionInput.value = client.situacion;
            desembolsoInput.value = client.desembolso || '-';
            observacionesInput.value = client.observaciones || '';
            refPersonalInput.value = client.ref_personal || '';
            refComercialInput.value = client.ref_comercial || '';
        } else {"""
html = html.replace(load_old, load_new)

# 6. Reset in saveAndAdd / init
reset_old = """            clientForm.reset();
            idInput.value = '';
            turnoInput.value = '-';
            situacionInput.value = 'Pendiente';
            desembolsoInput.value = '-';"""
reset_new = """            clientForm.reset();
            idInput.value = '';
            turnoInput.value = '-';
            situacionInput.value = 'Pendiente';
            desembolsoInput.value = '-';
            observacionesInput.value = '';
            refPersonalInput.value = '';
            refComercialInput.value = '';"""
html = html.replace(reset_old, reset_new)
html = html.replace(reset_old, reset_new) # Second time for btnSaveAndAdd if any

# 7. Add to Table render
table_row_old = """                    <td><span class="status-badge ${statusClass}">${situacionLabel}</span></td>
                    <td>${c.desembolso !== '-' && c.desembolso ? c.desembolso : '-'}</td>
                    <td class="action-buttons">"""
table_row_new = """                    <td><span class="status-badge ${statusClass}">${situacionLabel}</span></td>
                    <td>${c.desembolso !== '-' && c.desembolso ? c.desembolso : '-'}</td>
                    <td><div style="max-height:60px; overflow-y:auto; font-size:11px; color:#555;">${c.observaciones || '-'}</div></td>
                    <td>
                        <div style="font-size:10px; color:#444;"><b>Per:</b> ${c.ref_personal || '-'}</div>
                        <div style="font-size:10px; color:#444; margin-top:2px;"><b>Com:</b> ${c.ref_comercial || '-'}</div>
                    </td>
                    <td class="action-buttons">"""
html = html.replace(table_row_old, table_row_new)

# 8. Export to Excel
excel_old = """            'SITUACION': c.situacion,
            'ESTADO DESEMBOLSO': c.desembolso !== '-' && c.desembolso ? c.desembolso : ''
        }));"""
excel_new = """            'SITUACION': c.situacion,
            'ESTADO DESEMBOLSO': c.desembolso !== '-' && c.desembolso ? c.desembolso : '',
            'OBSERVACIONES': c.observaciones || '',
            'REF. PERSONAL': c.ref_personal || '',
            'REF. COMERCIAL': c.ref_comercial || ''
        }));"""
html = html.replace(excel_old, excel_new)

# 9. Implement Upload Excel button
upload_btn = """            <button id="btn-export-excel" class="btn" style="background-color: #107c41; color: white;">Descargar Excel</button>
            <label for="btn-import-excel" class="btn" style="background-color: #217346; color: white; cursor: pointer; margin: 0; padding: 10px;">Subir Excel</label>
            <input type="file" id="btn-import-excel" style="display: none;" accept=".xlsx, .xls">"""
html = html.replace('            <button id="btn-export-excel" class="btn" style="background-color: #107c41; color: white;">Descargar Excel</button>', upload_btn)

import_js = """
    // IMPORTAR EXCEL
    const btnImportExcel = document.getElementById('btn-import-excel');
    if (btnImportExcel) {
        btnImportExcel.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (!file) return;
            
            const reader = new FileReader();
            reader.onload = function(e) {
                const data = new Uint8Array(e.target.result);
                const workbook = XLSX.read(data, {type: 'array'});
                const sheetName = workbook.SheetNames[0];
                const worksheet = workbook.Sheets[sheetName];
                const json = XLSX.utils.sheet_to_json(worksheet, {raw: false});
                
                let imported = 0;
                json.forEach(row => {
                    if (row['CLIENTE'] || row['Cliente'] || row['cliente']) {
                        clients.push({
                            id: 'c_' + Date.now() + Math.random().toString(36).substr(2, 5),
                            cliente: row['CLIENTE'] || row['Cliente'] || row['cliente'] || '',
                            dni: row['DNI'] || row['Dni'] || row['dni'] || '-',
                            telefono: row['N° DE TELEFONO'] || row['Teléfono'] || row['Telefono'] || row['telefono'] || '-',
                            producto: row['PRODUCTO'] || row['Producto'] || row['producto'] || '-',
                            monto: row['MONTO'] || row['Monto'] || row['monto'] || '-',
                            lugar: row['LUGAR DE VISITA'] || row['Lugar'] || row['lugar'] || '-',
                            fecha: row['FECHA DE VISITA'] || row['Fecha'] || row['fecha'] || '-',
                            turno: row['TURNO'] || row['Turno'] || row['turno'] || '-',
                            situacion: row['SITUACION'] || row['Situacion'] || row['situacion'] || 'Pendiente',
                            desembolso: row['ESTADO DESEMBOLSO'] || row['Desembolso'] || '-',
                            observaciones: row['OBSERVACIONES'] || row['Observaciones'] || '',
                            ref_personal: row['REF. PERSONAL'] || row['Ref. Personal'] || '',
                            ref_comercial: row['REF. COMERCIAL'] || row['Ref. Comercial'] || ''
                        });
                        imported++;
                    }
                });
                
                if (imported > 0) {
                    alert('Se importaron ' + imported + ' clientes exitosamente.');
                    saveAndRender();
                } else {
                    alert('No se encontraron clientes válidos en el archivo Excel.');
                }
                btnImportExcel.value = ''; // reset
            };
            reader.readAsArrayBuffer(file);
        });
    }
"""
html = html.replace('// --- NUEVAS MEJORAS JS ---', import_js + '\n    // --- NUEVAS MEJORAS JS ---')

# 10. Offline mode wrapper for saveAndRender()
# Replace fetch save with fallback to localStorage
save_render_old = """    async function saveAndRender() {
        renderTable();
        // Fire and forget to Google Sheets (simple POST to a web app if supported, but usually it requires CORS setup)
        // Since we are not strictly awaiting, we just assume it works.
        try {
            fetch(API_URL, {
                method: 'POST',
                mode: 'no-cors',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(clients)
            });
        } catch (e) {
            console.error('Error saving data:', e);
        }
    }"""
save_render_new = """    async function saveAndRender() {
        renderTable();
        
        // Guardado Local para modo Offline
        localStorage.setItem('agrobanco_clients_offline', JSON.stringify(clients));
        document.getElementById('sync-status').textContent = 'Guardado localmente... sincronizando...';
        document.getElementById('sync-status').style.color = '#ff9800';
        
        try {
            fetch(API_URL, {
                method: 'POST',
                mode: 'no-cors',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(clients)
            }).then(() => {
                document.getElementById('sync-status').textContent = '✅ Sincronizado en la nube';
                document.getElementById('sync-status').style.color = '#4caf50';
                setTimeout(() => document.getElementById('sync-status').textContent = '', 3000);
            }).catch(e => {
                document.getElementById('sync-status').textContent = '⚠️ Modo sin conexión (Se guardó localmente)';
                document.getElementById('sync-status').style.color = '#f44336';
            });
        } catch (e) {
            document.getElementById('sync-status').textContent = '⚠️ Modo sin conexión (Se guardó localmente)';
            document.getElementById('sync-status').style.color = '#f44336';
        }
    }"""
# Inject a sync-status indicator next to meta
html = html.replace('<h3 style="color: var(--primary-dark); font-size: 16px; margin: 0;">🎯 Mi Meta Mensual (Desembolsos)</h3>', '<h3 style="color: var(--primary-dark); font-size: 16px; margin: 0;">🎯 Mi Meta Mensual <span id="sync-status" style="font-size:12px; margin-left:15px;"></span></h3>')

if save_render_old in html:
    html = html.replace(save_render_old, save_render_new)
else:
    # It might be written differently
    html = html.replace("fetch(API_URL, {", "localStorage.setItem('agrobanco_clients_offline', JSON.stringify(clients));\n            fetch(API_URL, {")


# 11. Initial Load Offline Fallback
init_data_old = """    async function initData() {
        loadingIndicator.style.display = 'block';
        loadingIndicator.textContent = 'Cargando datos desde Google Sheets...';
        
        try {
            const response = await fetch(API_URL);"""
init_data_new = """    async function initData() {
        loadingIndicator.style.display = 'block';
        loadingIndicator.textContent = 'Cargando datos...';
        
        // Load from local storage first for instant display
        const localData = localStorage.getItem('agrobanco_clients_offline');
        if (localData) {
            clients = JSON.parse(localData);
            renderTable();
        }
        
        try {
            const response = await fetch(API_URL);"""
html = html.replace(init_data_old, init_data_new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
