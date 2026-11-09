import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update HTML Form
old_dni = """            <div class="form-group">
                <label for="dni">DNI</label>
                <input type="text" id="dni">
            </div>"""
new_dni = """            <div class="form-group">
                <label for="dni">DNI DEL TITULAR</label>
                <input type="text" id="dni" placeholder="DNI Principal">
            </div>
            
            <div style="background: rgba(0,0,0,0.02); border: 1px dashed var(--border-color); padding: 10px; border-radius: 6px; margin-bottom: 15px;">
                <label style="font-weight: bold; font-size: 11px; color: #666; margin-bottom: 5px; display: block;">👥 CÓNYUGE / AVAL / GARANTE (Opcional)</label>
                <div style="display: flex; gap: 8px; margin-bottom: 8px;">
                    <input type="text" id="aval1_nombre" placeholder="Nombre (Ej: Esposa / Aval 1)" style="flex: 2; padding: 8px; font-size: 13px;">
                    <input type="text" id="aval1_dni" placeholder="DNI Adicional 1" style="flex: 1; padding: 8px; font-size: 13px;">
                </div>
                <div style="display: flex; gap: 8px;">
                    <input type="text" id="aval2_nombre" placeholder="Nombre (Ej: Aval 2 / Garante)" style="flex: 2; padding: 8px; font-size: 13px;">
                    <input type="text" id="aval2_dni" placeholder="DNI Adicional 2" style="flex: 1; padding: 8px; font-size: 13px;">
                </div>
            </div>"""
html = html.replace(old_dni, new_dni)

# 2. Update JS DOM Variables
old_dom = """    const dniInput = document.getElementById('dni');"""
new_dom = """    const dniInput = document.getElementById('dni');
    const aval1Nombre = document.getElementById('aval1_nombre');
    const aval1Dni = document.getElementById('aval1_dni');
    const aval2Nombre = document.getElementById('aval2_nombre');
    const aval2Dni = document.getElementById('aval2_dni');"""
html = html.replace(old_dom, new_dom)

# 3. Update Save Data
old_save = """            dni: dniInput.value.trim() || '-',"""
new_save = """            dni: dniInput.value.trim() || '-',
            aval1_nombre: aval1Nombre.value.trim(),
            aval1_dni: aval1Dni.value.trim(),
            aval2_nombre: aval2Nombre.value.trim(),
            aval2_dni: aval2Dni.value.trim(),"""
html = html.replace(old_save, new_save)

# 4. Update Load Data
old_load = """            dniInput.value = client.dni === '-' ? '' : client.dni;"""
new_load = """            dniInput.value = client.dni === '-' ? '' : client.dni;
            aval1Nombre.value = client.aval1_nombre || '';
            aval1Dni.value = client.aval1_dni || '';
            aval2Nombre.value = client.aval2_nombre || '';
            aval2Dni.value = client.aval2_dni || '';"""
html = html.replace(old_load, new_load)

# 5. Reset inputs
old_reset = """            dniInput.value = '';"""
new_reset = """            dniInput.value = '';
            aval1Nombre.value = '';
            aval1Dni.value = '';
            aval2Nombre.value = '';
            aval2Dni.value = '';"""
html = html.replace(old_reset, new_reset)
html = html.replace(old_reset, new_reset)

# 6. Table Cell Render
old_td = """                    <td>${c.dni || '-'}</td>"""
new_td = """                    <td>
                        <strong style="color: #333; font-size: 12px;">${c.dni || '-'}</strong>
                        ${c.aval1_dni ? `<div style="font-size:10px; color:#555; margin-top:2px;"><b>👫 ${c.aval1_nombre || 'Aval'}:</b> ${c.aval1_dni}</div>` : ''}
                        ${c.aval2_dni ? `<div style="font-size:10px; color:#555; margin-top:2px;"><b>🤝 ${c.aval2_nombre || 'Aval 2'}:</b> ${c.aval2_dni}</div>` : ''}
                    </td>"""
html = html.replace(old_td, new_td)

# 7. Search Logic
old_search = """        let filtered = clients.filter(c => {
            const matchesSearch = c.cliente.toLowerCase().includes(term) || (c.dni && c.dni.includes(term));"""
new_search = """        let filtered = clients.filter(c => {
            const matchesSearch = c.cliente.toLowerCase().includes(term) || 
                                  (c.dni && c.dni.includes(term)) ||
                                  (c.aval1_dni && c.aval1_dni.includes(term)) ||
                                  (c.aval2_dni && c.aval2_dni.includes(term)) ||
                                  (c.aval1_nombre && c.aval1_nombre.toLowerCase().includes(term));"""
html = html.replace(old_search, new_search)

# 8. Excel Export
old_excel = """            'DNI': c.dni !== '-' ? c.dni : '',"""
new_excel = """            'DNI': c.dni !== '-' ? c.dni : '',
            'CÓNYUGE/AVAL 1 (NOMBRE)': c.aval1_nombre || '',
            'CÓNYUGE/AVAL 1 (DNI)': c.aval1_dni || '',
            'GARANTE/AVAL 2 (NOMBRE)': c.aval2_nombre || '',
            'GARANTE/AVAL 2 (DNI)': c.aval2_dni || '',"""
html = html.replace(old_excel, new_excel)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
