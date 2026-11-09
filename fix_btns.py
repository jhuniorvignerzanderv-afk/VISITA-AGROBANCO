import re
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'<a href="tel:[^"]*" class="btn-icon".*?</a>', r'<a href="tel:${c.telefono.replace(/\\s+/g, \'\')}" class="btn-icon" title="Llamar" onclick="event.stopPropagation();">📞 Llamar</a>', content)
content = re.sub(r'<a href="https://wa\.me/51[^"]*" target="_blank" class="btn-icon".*?</a>', r'<a href="https://wa.me/51${c.telefono.replace(/\\s+/g, \'\')}" target="_blank" class="btn-icon" title="WhatsApp" onclick="event.stopPropagation();" style="background-color: #25D366; color: white; border-color: #25D366;">🟢 WhatsApp</a>', content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
