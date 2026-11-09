import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Enhance the Mobile Card View CSS
# We'll replace the existing basic mobile table CSS with a much nicer card UI.
css_mobile_old = """        @media (max-width: 768px) {
            .container { padding: 10px; }
            table, thead, tbody, th, td, tr { display: block; }
            thead tr { display: none; }
            tr {
                margin-bottom: 15px;
                border: 1px solid #ddd;
                border-radius: 8px;
                background: white;
            }
            td {
                border: none;
                border-bottom: 1px solid #eee;
                position: relative;
                padding-left: 50%;
                text-align: right;
                min-height: 40px;
                display: flex;
                align-items: center;
                justify-content: flex-end;
            }
            td:before {
                position: absolute;
                top: 50%;
                left: 10px;
                transform: translateY(-50%);
                width: 45%;
                padding-right: 10px;
                white-space: nowrap;
                text-align: left;
                font-weight: bold;
                color: var(--primary-dark);
                font-size: 12px;
            }
            /* Labeling the data */
            td:nth-of-type(1):before { content: "CLIENTE"; }
            td:nth-of-type(2):before { content: "DNI"; }
            td:nth-of-type(3):before { content: "TELÉFONO"; }
            td:nth-of-type(4):before { content: "PRODUCTO"; }
            td:nth-of-type(5):before { content: "MONTO"; }
            td:nth-of-type(6):before { content: "LUGAR"; }
            td:nth-of-type(7):before { content: "FECHA"; }
            td:nth-of-type(8):before { content: "TURNO"; }
            td:nth-of-type(9):before { content: "SITUACIÓN"; }
            td:nth-of-type(10):before { content: "ESTADO DESEMBOLSO"; }
            td:nth-of-type(11):before { content: "ACCIONES"; top: 20px; }
            td:nth-of-type(11) {
                flex-direction: column;
                align-items: flex-end;
                gap: 8px;
                padding-top: 15px;
                padding-bottom: 15px;
            }
            td:nth-of-type(11) .btn {
                width: 100%;
                max-width: 150px;
                padding: 10px;
                text-align: center;
                display: block;
            }"""
            
css_mobile_new = """        @media (max-width: 768px) {
            .container { padding: 10px; }
            table, thead, tbody, th, td, tr { display: block; }
            thead tr { display: none; }
            tr {
                margin-bottom: 20px;
                border: 1px solid var(--border-color);
                border-radius: 12px;
                background: var(--container-bg, white);
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            body.dark-mode tr { box-shadow: 0 4px 10px rgba(0,0,0,0.4); }
            /* Client Name header inside card */
            td:nth-of-type(1) {
                background: var(--primary-color);
                color: white;
                font-size: 16px;
                font-weight: bold;
                text-align: center;
                padding: 12px;
                justify-content: center;
            }
            td:nth-of-type(1):before { content: ""; display: none; }
            td:nth-of-type(1) strong { color: white; }
            
            td {
                border: none;
                border-bottom: 1px solid #eee;
                position: relative;
                padding: 10px 15px 10px 45%;
                text-align: right;
                min-height: 40px;
                display: flex;
                align-items: center;
                justify-content: flex-end;
                font-size: 14px;
            }
            body.dark-mode td { border-bottom: 1px solid #333; }
            td:last-child { border-bottom: none; }
            
            td:before {
                position: absolute;
                top: 50%;
                left: 15px;
                transform: translateY(-50%);
                width: 40%;
                white-space: nowrap;
                text-align: left;
                font-weight: bold;
                color: #666;
                font-size: 12px;
                text-transform: uppercase;
            }
            body.dark-mode td:before { color: #aaa; }
            
            /* Labeling the data */
            td:nth-of-type(2):before { content: "DNI"; }
            td:nth-of-type(3):before { content: "TELÉFONO"; }
            td:nth-of-type(4):before { content: "PRODUCTO"; }
            td:nth-of-type(5):before { content: "MONTO"; }
            td:nth-of-type(6):before { content: "LUGAR"; }
            td:nth-of-type(7):before { content: "FECHA"; }
            td:nth-of-type(8):before { content: "TURNO"; }
            td:nth-of-type(9):before { content: "SITUACIÓN"; }
            td:nth-of-type(10):before { content: "DESEMBOLSO"; }
            td:nth-of-type(11):before { content: "OBSERVACIONES"; }
            td:nth-of-type(12):before { content: "REFERENCIAS"; }
            td:nth-of-type(13):before { content: ""; } /* Acciones */
            
            td:nth-of-type(13) {
                flex-direction: row;
                flex-wrap: wrap;
                align-items: center;
                justify-content: center;
                gap: 10px;
                padding: 15px;
                background: rgba(0,0,0,0.02);
            }
            body.dark-mode td:nth-of-type(13) { background: rgba(255,255,255,0.02); }
            td:nth-of-type(13) .btn {
                width: 45%;
                margin: 0 !important;
                padding: 8px;
                font-size: 13px;
            }"""
            
if 'td:nth-of-type(11):before { content: "ACCIONES";' in html:
    html = re.sub(r'@media \(max-width: 768px\) \{.*?td:nth-of-type\(11\) \.btn \{[^}]+\}', css_mobile_new, html, flags=re.DOTALL)
else:
    # If not found cleanly, just append
    html = html.replace('</style>', css_mobile_new + '\n        }\n    </style>')


# 2. Add Reprogram Modal and Buttons
# Modal HTML
reprogram_modal = """
<!-- Modal Reprogramar -->
<div id="reprogram-modal" class="modal">
    <div class="modal-content" style="max-width: 350px;">
        <span class="close" onclick="document.getElementById('reprogram-modal').style.display='none'">&times;</span>
        <h2 style="font-size: 18px; color: var(--primary-dark); margin-bottom: 15px;">📅 Reprogramar Visita</h2>
        <input type="hidden" id="reprogram-id">
        <div class="form-group">
            <label>Nueva Fecha:</label>
            <input type="date" id="reprogram-date" style="padding: 10px; width: 100%; border-radius: 4px; border: 1px solid #ccc; margin-bottom: 15px;">
        </div>
        <div class="form-group">
            <label>Nuevo Turno (Opcional):</label>
            <select id="reprogram-turno" style="padding: 10px; width: 100%; border-radius: 4px; border: 1px solid #ccc;">
                <option value="-">-</option>
                <option value="Mañana">Mañana</option>
                <option value="Tarde">Tarde</option>
            </select>
        </div>
        <button onclick="confirmReprogram()" class="btn btn-primary" style="width: 100%; padding: 12px; font-size: 16px;">Guardar Cambios</button>
    </div>
</div>
"""
html = html.replace('<!-- MODAL PARA GESTIONAR REZAGADOS / REPROGRAMACIONES -->', reprogram_modal + '\n<!-- MODAL PARA GESTIONAR REZAGADOS / REPROGRAMACIONES -->')

# Add JS for Reprogram
reprogram_js = """
    window.openReprogram = function(id) {
        const idx = clients.findIndex(c => c.id === id);
        if (idx !== -1) {
            document.getElementById('reprogram-id').value = id;
            const c = clients[idx];
            document.getElementById('reprogram-date').value = (c.fecha && c.fecha !== '-') ? c.fecha : '';
            document.getElementById('reprogram-turno').value = (c.turno && c.turno !== '-') ? c.turno : '-';
            document.getElementById('reprogram-modal').style.display = 'block';
        }
    };
    
    window.confirmReprogram = function() {
        const id = document.getElementById('reprogram-id').value;
        const newDate = document.getElementById('reprogram-date').value;
        const newTurno = document.getElementById('reprogram-turno').value;
        
        if (!newDate) {
            alert('Por favor selecciona una fecha.');
            return;
        }
        
        const idx = clients.findIndex(c => c.id === id);
        if (idx !== -1) {
            clients[idx].fecha = newDate;
            clients[idx].turno = newTurno;
            saveAndRender();
            document.getElementById('reprogram-modal').style.display = 'none';
        }
    };
"""
html = html.replace('// --- NUEVAS MEJORAS JS ---', reprogram_js + '\n    // --- NUEVAS MEJORAS JS ---')

# Inject Reprogram Button in Table Actions
html = html.replace('let quickActions = \'\';', 'let quickActions = `<button class="btn" style="background-color: #ff9800; color: white; width: 100%; margin-bottom: 5px;" onclick="event.stopPropagation(); openReprogram(\'${c.id}\')">📅 Reprogramar</button>`;')


# 3. Add Group by Location Toggle
# Add Button next to status filter
filter_controls_old = """                <select id="status-filter" style="padding: 8px; border: 1px solid #ccc; border-radius: 4px; outline: none; background: white; flex: 1; min-width: 150px;">"""
filter_controls_new = """                <button id="btn-group-location" class="btn" style="background: #607d8b; color: white; font-size: 13px; padding: 8px 12px; border-radius: 4px;" onclick="toggleGroupLocation()">🗺️ Agrupar por Zona</button>
                <select id="status-filter" style="padding: 8px; border: 1px solid #ccc; border-radius: 4px; outline: none; background: white; flex: 1; min-width: 150px;">"""
html = html.replace(filter_controls_old, filter_controls_new)

# Add Group Logic in renderTable
group_js = """
    window.isGroupedByLocation = false;
    window.toggleGroupLocation = function() {
        window.isGroupedByLocation = !window.isGroupedByLocation;
        const btn = document.getElementById('btn-group-location');
        if (window.isGroupedByLocation) {
            btn.style.background = '#e91e63'; // pink active
            btn.innerHTML = '❌ Quitar Agrupación';
        } else {
            btn.style.background = '#607d8b'; // normal
            btn.innerHTML = '🗺️ Agrupar por Zona';
        }
        renderTable();
    };
"""
html = html.replace('// --- NUEVAS MEJORAS JS ---', group_js + '\n    // --- NUEVAS MEJORAS JS ---')

# In renderTable sort logic:
sort_old = """        filtered.sort((a, b) => {
            if (a.situacion === 'Atendido' && b.situacion !== 'Atendido') return 1;
            if (a.situacion !== 'Atendido' && b.situacion === 'Atendido') return -1;
            
            if (a._isOverdue && !b._isOverdue) return -1;
            if (!a._isOverdue && b._isOverdue) return 1;
            
            const dateA = a.fecha && a.fecha !== '-' ? new Date(a.fecha + 'T00:00:00') : new Date('2099-01-01');
            const dateB = b.fecha && b.fecha !== '-' ? new Date(b.fecha + 'T00:00:00') : new Date('2099-01-01');
            return dateA - dateB;
        });"""

sort_new = """        filtered.sort((a, b) => {
            if (window.isGroupedByLocation) {
                const locA = (a.lugar || 'Z_Sin Zona').trim().toUpperCase();
                const locB = (b.lugar || 'Z_Sin Zona').trim().toUpperCase();
                if (locA < locB) return -1;
                if (locA > locB) return 1;
            }
            
            if (a.situacion === 'Atendido' && b.situacion !== 'Atendido') return 1;
            if (a.situacion !== 'Atendido' && b.situacion === 'Atendido') return -1;
            
            if (a._isOverdue && !b._isOverdue) return -1;
            if (!a._isOverdue && b._isOverdue) return 1;
            
            const dateA = a.fecha && a.fecha !== '-' ? new Date(a.fecha + 'T00:00:00') : new Date('2099-01-01');
            const dateB = b.fecha && b.fecha !== '-' ? new Date(b.fecha + 'T00:00:00') : new Date('2099-01-01');
            return dateA - dateB;
        });"""
html = html.replace(sort_old, sort_new)

# Add headers when grouping in tbody loop
render_loop_old = """            filtered.forEach(c => {
                const tr = document.createElement('tr');"""

render_loop_new = """            let currentGroupLoc = null;
            filtered.forEach(c => {
                if (window.isGroupedByLocation) {
                    const cLoc = (c.lugar || 'Sin Zona asignada').trim().toUpperCase();
                    if (cLoc !== currentGroupLoc) {
                        const trSep = document.createElement('tr');
                        trSep.innerHTML = `<td colspan="13" style="background-color: var(--primary-color, #1b5e20); color: white; font-weight: bold; padding: 12px; text-align: center; font-size: 15px; border-radius: 4px; margin-bottom: 10px;">📍 ZONA: ${cLoc}</td>`;
                        tbody.appendChild(trSep);
                        currentGroupLoc = cLoc;
                    }
                }
            
                const tr = document.createElement('tr');"""
html = html.replace(render_loop_old, render_loop_new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
