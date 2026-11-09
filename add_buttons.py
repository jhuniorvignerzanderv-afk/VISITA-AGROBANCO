import re
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace table HTML logic
new_td = r'''                    <td>
                        ${c.telefono}
                        ${(c.telefono && c.telefono !== '-') ? `
                            <div style="margin-top: 5px; display: flex; gap: 5px;">
                                <a href="tel:${c.telefono.replace(/\s+/g, '')}" class="btn-icon" title="Llamar" onclick="event.stopPropagation();">📞 Llamar</a>
                                <a href="https://wa.me/51${c.telefono.replace(/\s+/g, '')}" target="_blank" class="btn-icon" title="WhatsApp" onclick="event.stopPropagation();" style="background-color: #25D366; color: white; border-color: #25D366;">🟢 WhatsApp</a>
                            </div>
                        ` : ''}
                    </td>'''

content = content.replace('<td>${c.telefono}</td>', new_td)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
