import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_lugar = r'''                    <td>
                        ${c.lugar || '-'}
                        ${(c.lugar && c.lugar !== '-') ? `<br><a href="https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(c.lugar + ', Perú')}" target="_blank" class="btn-icon" style="margin-top:4px; font-size:10px; background-color:#e3f2fd; border-color:#90caf9; color:#1976d2;" onclick="event.stopPropagation();">📍 Mapa</a>` : ''}
                    </td>'''

content = content.replace("<td>${c.lugar || '-'}</td>", new_lugar)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
