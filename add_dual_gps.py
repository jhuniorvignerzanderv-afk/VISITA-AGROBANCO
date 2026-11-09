import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update the Modal HTML
old_modal_lugar = """            <div class="form-group">
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
            
new_modal_lugar = """            <div class="form-group">
                <label for="lugar">LUGAR DE VISITA Y MAPAS GPS</label>
                <input type="text" id="lugar" placeholder="Nombre del lugar (Ej: Caserío San José)" style="margin-bottom: 8px;">
                
                <div style="display: flex; gap: 5px;">
                    <label for="upload-gps-dom" class="btn" style="background: #0288d1; color: white; padding: 6px; margin: 0; cursor: pointer; flex: 1; text-align: center; border-radius: 4px; font-size: 12px;">🏠 Foto Domicilio</label>
                    <input type="file" id="upload-gps-dom" accept="image/*" style="display: none;">
                    
                    <label for="upload-gps-cha" class="btn" style="background: #388e3c; color: white; padding: 6px; margin: 0; cursor: pointer; flex: 1; text-align: center; border-radius: 4px; font-size: 12px;">🌾 Foto Chacra</label>
                    <input type="file" id="upload-gps-cha" accept="image/*" style="display: none;">
                </div>
                
                <div style="display: flex; gap: 5px; margin-top: 5px;">
                    <div style="flex: 1; text-align: center;">
                        <div id="gps-status-dom" style="font-size: 11px; color: #666;"></div>
                        <a id="preview-dom" href="#" target="_blank" style="display: none; font-size: 10px; color: #0288d1; text-decoration: underline;">Ver Domicilio</a>
                    </div>
                    <div style="flex: 1; text-align: center;">
                        <div id="gps-status-cha" style="font-size: 11px; color: #666;"></div>
                        <a id="preview-cha" href="#" target="_blank" style="display: none; font-size: 10px; color: #388e3c; text-decoration: underline;">Ver Chacra</a>
                    </div>
                </div>
                
                <input type="hidden" id="gps-dom">
                <input type="hidden" id="gps-cha">
            </div>"""
html = html.replace(old_modal_lugar, new_modal_lugar)

# 2. Update JS DOM Elements
old_dom = """    const lugarInput = document.getElementById('lugar');
    const uploadGps = document.getElementById('upload-gps');
    const gpsLinkInput = document.getElementById('gps-link');
    const gpsLinkPreview = document.getElementById('gps-link-preview');
    const gpsStatus = document.getElementById('gps-status');"""
    
new_dom = """    const lugarInput = document.getElementById('lugar');
    const uploadGpsDom = document.getElementById('upload-gps-dom');
    const uploadGpsCha = document.getElementById('upload-gps-cha');
    const gpsDomInput = document.getElementById('gps-dom');
    const gpsChaInput = document.getElementById('gps-cha');
    const gpsStatusDom = document.getElementById('gps-status-dom');
    const gpsStatusCha = document.getElementById('gps-status-cha');
    const previewDom = document.getElementById('preview-dom');
    const previewCha = document.getElementById('preview-cha');"""
html = html.replace(old_dom, new_dom)

# 3. Update Save Client Data
old_save = """            lugar: lugarInput.value.trim() || '-',
            gps_link: gpsLinkInput.value.trim() || '','""
""" # Handle if there is a trailing comma or something
if "gps_link: gpsLinkInput.value.trim() || ''," in html:
    html = html.replace("gps_link: gpsLinkInput.value.trim() || '',", "gps_dom: gpsDomInput.value.trim() || '',\n            gps_cha: gpsChaInput.value.trim() || '',")
elif "gps_link: gpsLinkInput.value.trim() || ''" in html:
    html = html.replace("gps_link: gpsLinkInput.value.trim() || ''", "gps_dom: gpsDomInput.value.trim() || '',\n            gps_cha: gpsChaInput.value.trim() || ''")

# 4. Update Load Edit Client
old_load = """            lugarInput.value = client.lugar !== '-' ? client.lugar : '';
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
            
new_load = """            lugarInput.value = client.lugar !== '-' ? client.lugar : '';
            gpsDomInput.value = client.gps_dom || '';
            if (client.gps_dom) {
                previewDom.href = client.gps_dom;
                previewDom.style.display = 'inline-block';
                gpsStatusDom.textContent = "✅ OK";
                gpsStatusDom.style.color = "green";
            } else {
                previewDom.style.display = 'none';
                gpsStatusDom.textContent = "";
            }
            
            gpsChaInput.value = client.gps_cha || '';
            if (client.gps_cha) {
                previewCha.href = client.gps_cha;
                previewCha.style.display = 'inline-block';
                gpsStatusCha.textContent = "✅ OK";
                gpsStatusCha.style.color = "green";
            } else {
                previewCha.style.display = 'none';
                gpsStatusCha.textContent = "";
            }"""
html = html.replace(old_load, new_load)

# 5. Reset inputs
old_reset = """            lugarInput.value = '';
            gpsLinkInput.value = '';
            gpsLinkPreview.style.display = 'none';
            gpsStatus.textContent = "";"""
new_reset = """            lugarInput.value = '';
            gpsDomInput.value = '';
            gpsChaInput.value = '';
            previewDom.style.display = 'none';
            previewCha.style.display = 'none';
            gpsStatusDom.textContent = '';
            gpsStatusCha.textContent = '';"""
html = html.replace(old_reset, new_reset)
html = html.replace(old_reset, new_reset)

# 6. Extraction JS
old_gps_js = """    // EXIF GPS EXTRACTION
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
    }"""
    
new_gps_js = """    // EXIF GPS EXTRACTION HELPER
    function handleGPSUpload(inputElement, statusElement, linkInput, previewLink, name) {
        inputElement.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (!file) return;
            
            statusElement.textContent = "⌛ Leyendo...";
            statusElement.style.color = "#ff9800";
            
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
                        linkInput.value = mapsUrl;
                        
                        previewLink.href = mapsUrl;
                        previewLink.style.display = 'inline-block';
                        statusElement.textContent = `✅ ${name} guardado`;
                        statusElement.style.color = "#4caf50";
                        
                    } else {
                        statusElement.textContent = "❌ Sin GPS";
                        statusElement.style.color = "#f44336";
                        previewLink.style.display = 'none';
                        linkInput.value = "";
                    }
                } catch(err) {
                    statusElement.textContent = "❌ Error";
                    statusElement.style.color = "#f44336";
                }
                inputElement.value = ''; // reset
            });
        });
    }
    
    if (uploadGpsDom) handleGPSUpload(uploadGpsDom, gpsStatusDom, gpsDomInput, previewDom, "Domicilio");
    if (uploadGpsCha) handleGPSUpload(uploadGpsCha, gpsStatusCha, gpsChaInput, previewCha, "Chacra");"""
html = html.replace(old_gps_js, new_gps_js)

# 7. Render Table Output
old_table_render = """                    <td>
                        ${c.lugar !== '-' ? 
                            `<a href="${c.gps_link ? c.gps_link : 'https://www.google.com/maps/search/' + encodeURIComponent(c.lugar)}" target="_blank" style="color:${c.gps_link ? '#e91e63' : 'var(--primary-color)'}; text-decoration:none; font-weight:bold;" onclick="event.stopPropagation();">📍 ${c.lugar}</a>` 
                        : '-'}
                    </td>"""
                    
new_table_render = """                    <td>
                        <div style="font-weight: bold; font-size: 11px; margin-bottom: 4px; color: #333;">${c.lugar !== '-' ? c.lugar : ''}</div>
                        <div style="display: flex; gap: 4px; flex-wrap: wrap;">
                            ${c.gps_dom ? `<a href="${c.gps_dom}" target="_blank" style="background:#0288d1; color:white; padding:2px 6px; border-radius:4px; text-decoration:none; font-size:10px; box-shadow:0 2px 4px rgba(0,0,0,0.2);" onclick="event.stopPropagation();">🏠 Domicilio</a>` : ''}
                            ${c.gps_cha ? `<a href="${c.gps_cha}" target="_blank" style="background:#388e3c; color:white; padding:2px 6px; border-radius:4px; text-decoration:none; font-size:10px; box-shadow:0 2px 4px rgba(0,0,0,0.2);" onclick="event.stopPropagation();">🌾 Chacra</a>` : ''}
                            ${!c.gps_dom && !c.gps_cha && c.lugar !== '-' ? `<a href="https://www.google.com/maps/search/${encodeURIComponent(c.lugar)}" target="_blank" style="color:var(--primary-color); text-decoration:none; font-weight:bold;" onclick="event.stopPropagation();">📍 Ver Mapa</a>` : ''}
                        </div>
                    </td>"""
html = html.replace(old_table_render, new_table_render)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
