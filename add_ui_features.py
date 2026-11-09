import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add quick call widget
quick_widget = """
    <div style="background: #e8f5e9; padding: 15px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #4caf50;">
        <h3 style="color: var(--primary-dark); font-size: 16px; margin-bottom: 10px;">Llamar / WhatsApp Rápido</h3>
        <div style="display: flex; gap: 10px; flex-wrap: wrap;">
            <input type="tel" id="quick-phone" placeholder="Ingresa un número (ej: 999123456)" style="flex: 1; min-width: 200px; padding: 10px; border: 1px solid #ccc; border-radius: 4px; font-size: 16px;">
            <button onclick="quickCall()" class="btn btn-primary" style="display: flex; align-items: center; gap: 5px;">📞 Llamar</button>
            <button onclick="quickWhatsApp()" class="btn" style="background-color: #25D366; color: white; display: flex; align-items: center; gap: 5px;">🟢 WhatsApp</button>
        </div>
        <script>
            function getCleanPhone() {
                return document.getElementById('quick-phone').value.replace(/\\s+/g, '');
            }
            function quickCall() {
                const phone = getCleanPhone();
                if (phone) window.location.href = 'tel:' + phone;
                else alert('Por favor, ingresa un número de teléfono');
            }
            function quickWhatsApp() {
                const phone = getCleanPhone();
                if (phone) window.open('https://wa.me/51' + phone, '_blank');
                else alert('Por favor, ingresa un número de teléfono');
            }
        </script>
    </div>
"""

content = content.replace('</header>', '</header>\n' + quick_widget)


# Add responsive table CSS
mobile_css = """
        @media (max-width: 768px) {
            table, thead, tbody, th, td, tr { 
                display: block; 
            }
            thead tr { 
                position: absolute;
                top: -9999px;
                left: -9999px;
            }
            tr { 
                border: 1px solid #ccc; 
                margin-bottom: 15px; 
                border-radius: 8px;
                background: white;
                box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            }
            td { 
                border: none;
                border-bottom: 1px solid #eee; 
                position: relative;
                padding-left: 50%; 
                text-align: right;
                min-height: 40px;
            }
            td:before { 
                position: absolute;
                top: 12px;
                left: 15px;
                width: 45%; 
                padding-right: 10px; 
                white-space: nowrap;
                text-align: left;
                font-weight: bold;
                color: var(--primary-dark);
            }
            /* Labeling the data */
            td:nth-of-type(1):before { content: "CLIENTE"; }
            td:nth-of-type(2):before { content: "DNI"; }
            td:nth-of-type(3):before { content: "TELÉFONO"; }
            td:nth-of-type(4):before { content: "PRODUCTO"; }
            td:nth-of-type(5):before { content: "MONTO"; }
            td:nth-of-type(6):before { content: "LUGAR"; }
            td:nth-of-type(7):before { content: "FECHA"; }
            td:nth-of-type(8):before { content: "TURNO"; }
            td:nth-of-type(9):before { content: "SITUACIÓN"; }
            td:nth-of-type(10):before { content: "ESTADO DESEMBOLSO"; }
            td:nth-of-type(11):before { content: "ACCIONES"; }
        }
"""

content = content.replace('</style>', mobile_css + '\n    </style>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
