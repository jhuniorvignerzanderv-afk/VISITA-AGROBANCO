import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update the default products array
old_defaults = "const defaultProducts = ['Maíz', 'Arroz', 'Café', 'Cacao', 'Ganado'];"
new_defaults = "const defaultProducts = ['Espárrago', 'Maíz', 'Caña de Azúcar', 'Ganado'];"
html = html.replace(old_defaults, new_defaults)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
