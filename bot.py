def format_message(original_text, source):
    import re

    lines = original_text.strip().split('\n')
    date = 'N/A'
    aircraft = 'N/A'
    seats = 'N/A'
    price = 'N/A'
    departure = ''
    arrival = ''
    flags = ['🇮🇹', '🇫🇷', '🇪🇸', '🇩🇪', '🇬🇧', '🇺🇸', '🇬🇷', '🇨🇭', '🇳🇱', '🇵🇹', '🇦🇹', '🇱🇺', '🇨🇿']

    headers = {
        'getjet_european_el': '🇪🇺✈️ EUROPE BADINJETSLUX.COM',
        'getjet_transatlantic_el': '🌍✈️ TRANSATLANTIC BADINJETSLUX.COM',
        'getjet_me_el': '🌴🌟 MIDDLE EAST BADINJETSLUX.COM',
        'getjet_cis_el': '🇺🇳🛫 CIS REGION BADINJETSLUX.COM'
    }

    header = headers.get(source, '✈️ BADINJETSLUX.COM')

    for line in lines:
        clean = line.strip()

        # Estrai Data
        if "Date:" in clean:
            date_match = re.search(r'Date:\s*(\d{2}\.\d{2}\.\d{4})', clean)
            if date_match:
                date = date_match.group(1)

        # Estrai Aircraft (elimina eventuali simboli extra)
        if "Aircraft:" in clean:
            aircraft_match = re.search(r'Aircraft:\s*\**\s*(.+)', clean)
            if aircraft_match:
                aircraft = aircraft_match.group(1).strip()

        # Estrai Seats
        if "Seats:" in clean:
            seats_match = re.search(r'Seats:\s*\**\s*(\d+)', clean)
            if seats_match:
                seats = seats_match.group(1)

        # Estrai Prezzo e incrementa del 5%
        if "Price:" in clean:
            price_match = re.search(r'([0-9]+[.,]?[0-9]*)', clean.replace(',', '').replace('€', ''))
            if price_match:
                try:
                    val = float(price_match.group(1))
                    new_val = round(val * 1.05)
                    price = f"{new_val:,}".replace(",", ".")
                except:
                    price = 'N/A'

        # Estrai partenza e arrivo
        if any(flag in clean for flag in flags):
            if not departure:
                departure = clean
            elif not arrival:
                arrival = clean

    return f"""✈️ EMPTY LEG
{header}
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
