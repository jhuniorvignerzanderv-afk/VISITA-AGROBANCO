import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_code = """
            const visits = clients.filter(c => c.fecha === day.date && c.situacion !== 'Atendido');
            const totalVisits = visits.length;
            const numManana = visits.filter(c => c.turno === 'Mañana').length;
            const numTarde = visits.filter(c => c.turno === 'Tarde').length;
"""

new_code = """
            const visits = clients.filter(c => c.fecha === day.date && c.situacion !== 'Atendido');
            const totalVisits = visits.length;
            let dailySum = 0;
            visits.forEach(c => {
                let mStr = String(c.monto || '0').replace(/[^0-9.,-]/g, '');
                if (mStr.lastIndexOf(',') > mStr.lastIndexOf('.')) {
                    mStr = mStr.replace(/\\./g, '').replace(',', '.');
                } else {
                    mStr = mStr.replace(/,/g, '');
                }
                dailySum += parseFloat(mStr) || 0;
            });
            const numManana = visits.filter(c => c.turno === 'Mañana').length;
            const numTarde = visits.filter(c => c.turno === 'Tarde').length;
"""

content = content.replace(old_code.strip(), new_code.strip())

old_html = """
                <h3>${dayName} ${dayNum} ${monthName}</h3>
                <div style="font-size: 12px; margin-bottom: 8px; color: #555; border-bottom: 1px solid #eee; padding-bottom: 5px;">
                    Total a visitar: <strong>${totalVisits}</strong>
                </div>
"""

new_html = """
                <h3>${dayName} ${dayNum} ${monthName}</h3>
                <div style="font-size: 12px; margin-bottom: 8px; color: #555; border-bottom: 1px solid #eee; padding-bottom: 5px; line-height: 1.4;">
                    Total a visitar: <strong>${totalVisits}</strong> clientes<br>
                    Monto proyectado: <strong style="color: #e65100;">S/ ${dailySum.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</strong>
                </div>
"""

content = content.replace(old_html.strip(), new_html.strip())

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
