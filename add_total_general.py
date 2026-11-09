import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix parsing of monto (handle Peruvian commas for decimals or thousands)
# If it's like 1,500.00 -> 1500.00
# If it's like 1.500,00 -> 1500.00
new_js = """
        let sumAtendidos = 0;
        let sumPendientes = 0;
        clients.forEach(c => {
            let mStr = String(c.monto || '0');
            // Remove spaces and currency symbols
            mStr = mStr.replace(/[^0-9.,-]/g, '');
            
            // Handle European/Peruvian format vs US format
            // If comma is the last non-digit character (e.g. 1.500,50), replace dots with nothing, comma with dot
            if (mStr.lastIndexOf(',') > mStr.lastIndexOf('.')) {
                mStr = mStr.replace(/\./g, '').replace(',', '.');
            } else {
                // US format (e.g. 1,500.50), remove commas
                mStr = mStr.replace(/,/g, '');
            }
            
            let m = parseFloat(mStr) || 0;
            if (c.situacion === 'Atendido') sumAtendidos += m;
            else sumPendientes += m;
        });
        
        const elDesembolsado = document.getElementById('total-desembolsado');
        const elPendiente = document.getElementById('total-pendiente');
        const elGeneral = document.getElementById('total-general');
        
        if (elDesembolsado) elDesembolsado.textContent = 'S/ ' + sumAtendidos.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
        if (elPendiente) elPendiente.textContent = 'S/ ' + sumPendientes.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
        if (elGeneral) elGeneral.textContent = 'S/ ' + (sumAtendidos + sumPendientes).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
"""

content = re.sub(r'let sumAtendidos = 0;.*?maximumFractionDigits: 2}\);', new_js, content, flags=re.DOTALL)

# Add the 3rd box for Total General
old_html = """<div style="flex: 1; min-width: 200px; background: #fff3e0; padding: 15px; border-radius: 8px; border: 1px solid #ffcc80;">
            <h3 style="color: #e65100; font-size: 14px; margin-bottom: 5px;">Proyección (Pendientes)</h3>
            <div id="total-pendiente" style="font-size: 24px; font-weight: bold; color: #e65100;">S/ 0.00</div>
        </div>"""

new_html = """<div style="flex: 1; min-width: 200px; background: #fff3e0; padding: 15px; border-radius: 8px; border: 1px solid #ffcc80;">
            <h3 style="color: #e65100; font-size: 14px; margin-bottom: 5px;">Proyección (Pendientes)</h3>
            <div id="total-pendiente" style="font-size: 24px; font-weight: bold; color: #e65100;">S/ 0.00</div>
        </div>
        <div style="flex: 1; min-width: 200px; background: #e8f5e9; padding: 15px; border-radius: 8px; border: 1px solid #81c784;">
            <h3 style="color: #2e7d32; font-size: 14px; margin-bottom: 5px;">Total General (Suma)</h3>
            <div id="total-general" style="font-size: 24px; font-weight: bold; color: #2e7d32;">S/ 0.00</div>
        </div>"""

content = content.replace(old_html, new_html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
