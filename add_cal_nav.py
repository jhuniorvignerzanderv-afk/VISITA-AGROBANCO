import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Header
header_replacement = r'''    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
        <h2 style="font-size: 16px; color: var(--primary-dark); margin: 0;">Calendario Semanal</h2>
        <div>
            <button onclick="changeCalendarWeek(-1)" class="btn" style="padding: 4px 8px; font-size: 12px; background: #eee; color: #333; border: 1px solid #ccc;">⬅️ Anterior</button>
            <button onclick="changeCalendarWeek(0)" class="btn" style="padding: 4px 8px; font-size: 12px; background: #eee; color: #333; border: 1px solid #ccc;">Hoy</button>
            <button onclick="changeCalendarWeek(1)" class="btn" style="padding: 4px 8px; font-size: 12px; background: #eee; color: #333; border: 1px solid #ccc;">Siguiente ➡️</button>
        </div>
    </div>'''

content = re.sub(r'<h2 style="font-size: 16px; color: var\(--primary-dark\); margin-bottom: 5px;">Calendario Semanal \(Lunes a Domingo\)</h2>', header_replacement, content)

# Modify renderCalendarDashboard function
js_replacement = r'''    let calendarWeekOffset = 0;

    window.changeCalendarWeek = function(direction) {
        if (direction === 0) {
            calendarWeekOffset = 0;
        } else {
            calendarWeekOffset += direction;
        }
        renderCalendarDashboard();
    };

    function renderCalendarDashboard() {
        const dashboard = document.getElementById('calendar-dashboard');
        if (!dashboard) return;

        const today = new Date();
        const currentDayOfWeek = today.getDay(); // 0 = Domingo, 1 = Lunes
        const diffToMonday = currentDayOfWeek === 0 ? -6 : 1 - currentDayOfWeek;
        
        const monday = new Date(today);
        monday.setDate(today.getDate() + diffToMonday + (calendarWeekOffset * 7));'''

content = re.sub(r'    function renderCalendarDashboard\(\) \{\s*const dashboard = document\.getElementById\(\'calendar-dashboard\'\);\s*if \(\!dashboard\) return;\s*// Obtener la semana actual \(Lunes a Domingo\)\s*const today = new Date\(\);\s*const currentDayOfWeek = today\.getDay\(\); // 0 = Domingo, 1 = Lunes\s*const diffToMonday = currentDayOfWeek === 0 \? -6 : 1 - currentDayOfWeek;\s*const monday = new Date\(today\);\s*monday\.setDate\(today\.getDate\(\) \+ diffToMonday\);', js_replacement, content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
