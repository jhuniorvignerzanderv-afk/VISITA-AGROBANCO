with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("function formatDate(dateStr) {\n        if (!dateStr) return '';\n        const parts = dateStr.split('-');", "function formatDate(dateStr) {\n        if (!dateStr) return '';\n        dateStr = String(dateStr);\n        const parts = dateStr.split('-');")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
