with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make the card header / whole card clickable for the entire day
old_card_head = """            const card = document.createElement('div');
            card.className = `calendar-card ${isToday ? 'today' : ''}`;
            card.innerHTML = `
                <h3>${dayName} ${dayNum} ${monthName}</h3>"""

new_card_head = """            const card = document.createElement('div');
            card.className = `calendar-card ${isToday ? 'today' : ''}`;
            card.innerHTML = `
                <h3 style="cursor: pointer; text-decoration: underline;" onclick="setCalendarFilter('${day.date}', 'Todo', '${dayName} ${dayNum}')" title="Ver TODO el día">${dayName} ${dayNum} ${monthName}</h3>"""

html = html.replace(old_card_head, new_card_head)

# Also support type === 'Todo' in setCalendarFilter and renderTable!
# In renderTable, let's see how calendarFilter is handled.
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated card header clickability.")
