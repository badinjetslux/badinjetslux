def format_message(original_text, source):
    import re

    lines = original_text.strip().split('\n')
    date = ''
    aircraft = ''
    seats = ''
    price = ''
    departure = ''
    arrival = ''
    flags = ['🇮🇹', '🇫🇷', '🇪🇸', '🇩🇪', '🇬🇧', '🇺🇸', '🇬🇷', '🇨🇭', '🇳🇱', '🇵🇹', '🇦🇹']

    headers = {
        'getjet_european_el': '🇪🇺✈️ EUROPE BADINJETSLUX.COM',
        'getjet_transatlantic_el': '🌍✈️ TRANSATLANTIC BADINJETSLUX.COM',
        'getjet_me_el': '🌴🌟 MIDDLE EAST BADINJETSLUX.COM',
        'getjet_cis_el': '🇺🇳🛫 CIS REGION BADINJETSLUX.COM'
    }

    header = headers.get(source, '✈️ BADINJETSLUX.COM')

    for line in lines:
        line = line.strip()
        if line.lower().startswith("date:"):
            date = line.split(":", 1)[1].strip()
        elif line.lower().startswith("aircraft:"):
            aircraft = line.split(":", 1)[1].strip()
        elif line.lower().startswith("seats:"):
            seats = line.split(":", 1)[1].strip()
        elif line.lower().startswith("price:"):
            match = re.search(r'([0-9]+[.,]?[0-9]*)', line)
            if match:
                try:
                    val = float(match.group(1).replace(',', '').replace('€', '').strip())
                    price = f"{round(val * 1.05):,}".replace(",", ".")
                except:
                    price = ''
        elif any(f in line for f in flags):
            if not departure:
                departure = line
            elif not arrival:
                arrival = line

    return f"""{header}
📍 Route: {departure} → {arrival}
🗓️ Date: {date}
✈️ Aircraft: {aircraft}
👥 Seats: {seats}
💶 Price: € {price}
📩 Info: info@badinjetslux.com
📲 Book now: booking@badinjetslux.com
💺 EMPTY LEG AVAILABLE
📸 Follow us on Instagram: https://instagram.com/badinjetslux
🌐 www.badinjetslux.com
"""
