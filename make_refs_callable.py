with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_render = """                    <td>
                        <div style="font-size:10px; color:#444;"><b>Per:</b> ${c.ref_personal || '-'}</div>
                        <div style="font-size:10px; color:#444; margin-top:2px;"><b>Com:</b> ${c.ref_comercial || '-'}</div>
                    </td>"""

new_render = """                    <td>
                        <div style="font-size:11px; color:#444; margin-bottom: 4px;">
                            <strong>👤 Per:</strong> ${c.ref_personal || '-'}
                            ${(() => {
                                const m = (c.ref_personal || '').match(/\\b9\\d{8}\\b/);
                                return m ? ` <a href="tel:${m[0]}" class="btn-icon" style="padding:1px 5px; font-size:10px;" onclick="event.stopPropagation();">📞 Llamar</a>` : '';
                            })()}
                        </div>
                        <div style="font-size:11px; color:#444;">
                            <strong>🏪 Com:</strong> ${c.ref_comercial || '-'}
                            ${(() => {
                                const m = (c.ref_comercial || '').match(/\\b9\\d{8}\\b/);
                                return m ? ` <a href="tel:${m[0]}" class="btn-icon" style="padding:1px 5px; font-size:10px;" onclick="event.stopPropagation();">📞 Llamar</a>` : '';
                            })()}
                        </div>
                    </td>"""

html = html.replace(old_render, new_render)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
