import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add exif-js CDN
if 'exif.js' not in html:
    html = html.replace('</head>', '    <script src="https://cdn.jsdelivr.net/npm/exif-js"></script>\n</head>')

# 2. Update Modal Form for LUGAR
lugar_old = """            <div class="form-group">
                <label for="lugar">LUGAR DE VISITA</label>
                <input type="text" id="lugar" placeholder="Ej: Caserio San Jose">
            </div>"""
lugar_new = """            <div class="form-group">
                <label for="lugar">LUGAR DE VISITA Y MAPA</label>
                <input type="text" id="lugar" placeholder="1. Escribe el lugar (Ej: Caserío San José)" style="margin-bottom: 8px;">
                
                <div style="display: flex; gap: 10px; font-size: 13px;">
                    <label for="upload-gps" class="btn" style="background: #2196f3; color: white; padding: 8px; margin: 0; cursor: pointer; flex: 1; text-align: center; border-radius: 4px;">📷 Extraer GPS de Foto</label>
                    <input type="file" id="upload-gps" accept="image/*" style="display: none;">
                    
                    <a id="gps-link-preview" href="#" target="_blank" style="display: none; background: #4caf50; color: white; padding: 8px; border-radius: 4px; text-decoration: none; text-align: center; flex: 1;">🗺️ Abrir Coordenada</a>
                </div>
                <div id="gps-status" style="font-size: 11px; color: #666; margin-top: 5px;"></div>
                <input type="hidden" id="gps-link">
            </div>"""
html = html.replace(lugar_old, lugar_new)

# 3. Add DOM Elements in init
dom_old = """    const lugarInput = document.getElementById('lugar');"""
dom_new = """    const lugarInput = document.getElementById('lugar');
    const uploadGps = document.getElementById('upload-gps');
    const gpsLinkInput = document.getElementById('gps-link');
    const gpsLinkPreview = document.getElementById('gps-link-preview');
    const gpsStatus = document.getElementById('gps-status');"""
html = html.replace(dom_old, dom_new)

# 4. Save and Load GPS Link
save_old = """            lugar: lugarInput.value.trim() || '-',"""
save_new = """            lugar: lugarInput.value.trim() || '-',
            gps_link: gpsLinkInput.value.trim() || '',"""
html = html.replace(save_old, save_new)

load_old = """            lugarInput.value = client.lugar !== '-' ? client.lugar : '';"""
load_new = """            lugarInput.value = client.lugar !== '-' ? client.lugar : '';
            gpsLinkInput.value = client.gps_link || '';
            if (client.gps_link) {
                gpsLinkPreview.href = client.gps_link;
                gpsLinkPreview.style.display = 'block';
                gpsStatus.textContent = "✅ Coordenadas guardadas";
                gpsStatus.style.color = "green";
            } else {
                gpsLinkPreview.style.display = 'none';
                gpsStatus.textContent = "";
            }"""
html = html.replace(load_old, load_new)

reset_old = """            lugarInput.value = '';"""
reset_new = """            lugarInput.value = '';
            gpsLinkInput.value = '';
            gpsLinkPreview.style.display = 'none';
            gpsStatus.textContent = "";"""
html = html.replace(reset_old, reset_new)
html = html.replace(reset_old, reset_new) # Second time for saveAndAdd


# 5. Extract GPS Logic
gps_js = """
    // EXIF GPS EXTRACTION
    if (uploadGps) {
        uploadGps.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (!file) return;
            
            gpsStatus.textContent = "⌛ Leyendo foto...";
            gpsStatus.style.color = "#ff9800";
            
            EXIF.getData(file, function() {
                try {
                    const lat = EXIF.getTag(this, "GPSLatitude");
                    const lon = EXIF.getTag(this, "GPSLongitude");
                    const latRef = EXIF.getTag(this, "GPSLatitudeRef");
                    const lonRef = EXIF.getTag(this, "GPSLongitudeRef");
                    
                    if (lat && lon) {
                        let latDec = lat[0] + lat[1]/60 + lat[2]/3600;
                        if (latRef === "S") latDec = -latDec;
                        
                        let lonDec = lon[0] + lon[1]/60 + lon[2]/3600;
                        if (lonRef === "W") lonDec = -lonDec;
                        
                        const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${latDec},${lonDec}`;
                        gpsLinkInput.value = mapsUrl;
                        
                        gpsLinkPreview.href = mapsUrl;
                        gpsLinkPreview.style.display = 'block';
                        gpsStatus.textContent = "✅ Coordenadas extraídas con éxito";
                        gpsStatus.style.color = "#4caf50";
                        
                        // Si el lugar estaba vacío, poner algo automático
                        if (!lugarInput.value.trim()) {
                            lugarInput.value = "Ubicación GPS Extraída";
                        }
                    } else {
                        gpsStatus.textContent = "❌ La foto no tiene datos de ubicación GPS.";
                        gpsStatus.style.color = "#f44336";
                        gpsLinkPreview.style.display = 'none';
                        gpsLinkInput.value = "";
                    }
                } catch(err) {
                    gpsStatus.textContent = "❌ Error leyendo la foto.";
                    gpsStatus.style.color = "#f44336";
                }
                uploadGps.value = ''; // reset
            });
        });
    }
"""
html = html.replace('// --- NUEVAS MEJORAS JS ---', gps_js + '\n    // --- NUEVAS MEJORAS JS ---')

# 6. Render Table with GPS Link
table_render_old = """                    <td>${c.lugar !== '-' ? `<a href="https://www.google.com/maps/search/${encodeURIComponent(c.lugar)}" target="_blank" style="color:var(--primary-color); text-decoration:none;" onclick="event.stopPropagation();">📍 ${c.lugar}</a>` : '-'}</td>"""
table_render_new = """                    <td>
                        ${c.lugar !== '-' ? 
                            `<a href="${c.gps_link ? c.gps_link : 'https://www.google.com/maps/search/' + encodeURIComponent(c.lugar)}" target="_blank" style="color:${c.gps_link ? '#e91e63' : 'var(--primary-color)'}; text-decoration:none; font-weight:bold;" onclick="event.stopPropagation();">📍 ${c.lugar}</a>` 
                        : '-'}
                    </td>"""
html = html.replace(table_render_old, table_render_new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
