import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_table_render = """                    <td>
                        <div style="font-weight: bold; font-size: 11px; margin-bottom: 4px; color: #333;">${c.lugar !== '-' ? c.lugar : ''}</div>
                        <div style="display: flex; gap: 4px; flex-wrap: wrap;">
                            ${c.gps_dom ? `<a href="${c.gps_dom}" target="_blank" style="background:#0288d1; color:white; padding:2px 6px; border-radius:4px; text-decoration:none; font-size:10px; box-shadow:0 2px 4px rgba(0,0,0,0.2);" onclick="event.stopPropagation();">🏠 Domicilio</a>` : ''}
                            ${c.gps_cha ? `<a href="${c.gps_cha}" target="_blank" style="background:#388e3c; color:white; padding:2px 6px; border-radius:4px; text-decoration:none; font-size:10px; box-shadow:0 2px 4px rgba(0,0,0,0.2);" onclick="event.stopPropagation();">🌾 Chacra</a>` : ''}
                            ${!c.gps_dom && !c.gps_cha && c.lugar !== '-' ? `<a href="https://www.google.com/maps/search/${encodeURIComponent(c.lugar)}" target="_blank" style="color:var(--primary-color); text-decoration:none; font-weight:bold;" onclick="event.stopPropagation();">📍 Ver Mapa</a>` : ''}
                        </div>
                    </td>"""
                    
new_table_render = """                    <td>
                        <div style="font-weight: bold; font-size: 11px; margin-bottom: 4px; color: #333;">
                            ${c.lugar !== '-' && c.lugar ? `<a href="https://www.google.com/maps/search/${encodeURIComponent(c.lugar)}" target="_blank" style="color:#1565c0; text-decoration:underline;" onclick="event.stopPropagation();">🔍 Buscar: ${c.lugar}</a>` : ''}
                        </div>
                        <div style="display: flex; gap: 4px; flex-wrap: wrap;">
                            ${c.gps_dom ? `<a href="${c.gps_dom}" target="_blank" style="background:#0288d1; color:white; padding:2px 6px; border-radius:4px; text-decoration:none; font-size:10px; box-shadow:0 2px 4px rgba(0,0,0,0.2);" onclick="event.stopPropagation();">🏠 GPS Domicilio</a>` : ''}
                            ${c.gps_cha ? `<a href="${c.gps_cha}" target="_blank" style="background:#388e3c; color:white; padding:2px 6px; border-radius:4px; text-decoration:none; font-size:10px; box-shadow:0 2px 4px rgba(0,0,0,0.2);" onclick="event.stopPropagation();">🌾 GPS Chacra</a>` : ''}
                        </div>
                    </td>"""
html = html.replace(old_table_render, new_table_render)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
