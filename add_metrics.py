import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# HTML to insert
metrics_html = """
    <div style="display: flex; gap: 15px; margin-bottom: 20px; flex-wrap: wrap;">
        <div style="flex: 1; min-width: 200px; background: #e3f2fd; padding: 15px; border-radius: 8px; border: 1px solid #90caf9;">
            <h3 style="color: #1565c0; font-size: 14px; margin-bottom: 5px;">Total Desembolsado (Atendidos)</h3>
            <div id="total-desembolsado" style="font-size: 24px; font-weight: bold; color: #0d47a1;">S/ 0.00</div>
        </div>
        <div style="flex: 1; min-width: 200px; background: #fff3e0; padding: 15px; border-radius: 8px; border: 1px solid #ffcc80;">
            <h3 style="color: #e65100; font-size: 14px; margin-bottom: 5px;">Proyección (Pendientes)</h3>
            <div id="total-pendiente" style="font-size: 24px; font-weight: bold; color: #e65100;">S/ 0.00</div>
        </div>
    </div>
"""

# Insert HTML before CALENDARIO INTERACTIVO
content = content.replace('<!-- CALENDARIO INTERACTIVO -->', metrics_html + '\n    <!-- CALENDARIO INTERACTIVO -->')

# JS to insert
metrics_js = """
        let sumAtendidos = 0;
        let sumPendientes = 0;
        clients.forEach(c => {
            let mStr = String(c.monto).replace(/[^0-9.-]+/g, "");
            let m = parseFloat(mStr) || 0;
            if (c.situacion === 'Atendido') sumAtendidos += m;
            else sumPendientes += m;
        });
        
        const elDesembolsado = document.getElementById('total-desembolsado');
        const elPendiente = document.getElementById('total-pendiente');
        if (elDesembolsado) elDesembolsado.textContent = 'S/ ' + sumAtendidos.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
        if (elPendiente) elPendiente.textContent = 'S/ ' + sumPendientes.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
"""

# Insert JS inside renderTable, right after tbody.innerHTML = '';
content = content.replace("tbody.innerHTML = '';", "tbody.innerHTML = '';\n" + metrics_js)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
