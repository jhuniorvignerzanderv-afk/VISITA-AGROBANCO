import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("c.cliente.toLowerCase()", "String(c.cliente || '').toLowerCase()")
content = content.replace("c.dni.toLowerCase()", "String(c.dni || '').toLowerCase()")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
