import re
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_func = r'''    function renderCalendarDashboard() {
        const dashboard = document.getElementById('calendar-dashboard');
        if (!dashboard) return;

        // Obtener la semana actual (Lunes a Domingo)
        const today = new Date();
        const currentDayOfWeek = today.getDay(); // 0 = Domingo, 1 = Lunes
        const diffToMonday = currentDayOfWeek === 0 ? -6 : 1 - currentDayOfWeek;
        
        const monday = new Date(today);
        monday.setDate(today.getDate() + diffToMonday);

        const days = [];
        for (let i = 0; i < 7; i++) {
            const d = new Date(monday);
            d.setDate(monday.getDate() + i);
            const dateString = d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
            days.push({
                date: dateString,
                obj: d
            });
        }

        dashboard.innerHTML = '';

        days.forEach(day => {
            const visits = clients.filter(c => c.fecha === day.date && c.situacion !== 'Atendido');
            const totalVisits = visits.length;
            const numManana = visits.filter(c => c.turno === 'Mañana').length;
            const numTarde = visits.filter(c => c.turno === 'Tarde').length;
            
            const localTodayStr = today.getFullYear() + '-' + String(today.getMonth() + 1).padStart(2, '0') + '-' + String(today.getDate()).padStart(2, '0');
            const isToday = day.date === localTodayStr;
            
            const daysOfWeek = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
            const dayName = daysOfWeek[day.obj.getDay()];
            const dayNum = day.obj.getDate();
            const monthName = day.obj.toLocaleString('es', { month: 'short' });

            const classManana = numManana >= 2 ? 'full' : '';
            const classTarde = numTarde >= 2 ? 'full' : '';

            const card = document.createElement('div');
            card.className = `calendar-card ${isToday ? 'today' : ''}`;
            card.innerHTML = `
                <h3>${dayName} ${dayNum} ${monthName}</h3>
                <div style="font-size: 12px; margin-bottom: 8px; color: #555; border-bottom: 1px solid #eee; padding-bottom: 5px;">
                    Total a visitar: <strong>${totalVisits}</strong>
                </div>
                <div class="shift">
                    <span>Mañana:</span>
                    <span class="count ${classManana}">${numManana}</span>
                </div>
                <div class="shift">
                    <span>Tarde:</span>
                    <span class="count ${classTarde}">${numTarde}</span>
                </div>
            `;
            dashboard.appendChild(card);
        });
    }'''

content = re.sub(r'    function renderCalendarDashboard\(\) \{.*?dashboard\.appendChild\(card\);\s*\}\);\s*\}', new_func, content, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
