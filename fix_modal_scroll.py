import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace .modal CSS
content = re.sub(
    r'\.modal\s*\{[^}]*\}',
    '''.modal {
            display: none;
            position: fixed;
            z-index: 100;
            left: 0; top: 0;
            width: 100%; height: 100%;
            background-color: rgba(0,0,0,0.5);
            overflow-y: auto; /* Permite scroll nativo */
            padding: 20px;
        }''',
    content,
    count=1
)

# Replace .modal-content CSS
content = re.sub(
    r'\.modal-content\s*\{[^}]*\}',
    '''.modal-content {
            background-color: white;
            z-index: 1001;
            pointer-events: auto;
            padding: 25px;
            border-radius: 8px;
            width: 100%;
            max-width: 500px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            position: relative;
            margin: 20px auto; /* Centrado horizontal, espacio libre arriba y abajo para scrollear */
        }''',
    content,
    count=1
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
