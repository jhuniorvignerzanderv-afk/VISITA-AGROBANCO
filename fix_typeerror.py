import re
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("c.telefono.replace(/\\s+/g, '')", "String(c.telefono).replace(/\\s+/g, '')")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
