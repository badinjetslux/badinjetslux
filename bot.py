import asyncio
import re
from telethon import TelegramClient, events

# --- CREDENZIALI ---
api_id = 22972066
api_hash = '8bec75c9c484b1ca177e722523efd9d9'
bot_token = '7792512773:AAHClF1i3eUlZczvzmFM5j67gPdb8AplhOA'

# --- CANALI SORGENTE E DESTINAZIONE ---
source_channels = [
    'getjet_european_el',
    'getjet_transatlantic_el',
    'getjet_me_el',
    'getjet_cis_el'
]
destination_channel = 'badinjetslux'

# --- AVVIO CLIENT TELEGRAM ---
client = TelegramClient('badinjet_session', api_id, api_hash).start(bot_token=bot_token)

# --- FUNZIONE FORMATTAZIONE ---
def format_message(original_text, source):
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

        if "Date:" in clean:
            date_match = re.search(r'Date:\s*(\d{2}\.\d{2}\.\d{4})', clean)
            if date_match:
                date = date_match.group(1)

        if "Aircraft:" in clean:
            aircraft_match = re.search(r'Aircraft:\s*(.+)', clean)
            if aircraft_match:
                aircraft = aircraft_match.group(1).strip()

        if "Seats:" in clean:
            seats_match = re.search(r'Seats:\s*(\d+)', clean)
            if seats_match:
                seats = seats_match.group(1)

        if "Price:" in clean:
            price_match = re.search(r'([0-9]+[.,]?[0-9]*)', clean.replace(',', '').replace('€', ''))
            if price_match:
                try:
                    val = float(price_match.group(1))
                    new_val = round(val * 1.05)
                    price = f"{new_val:,}".replace(",", ".")
                except:
                    price = 'N/A'

        if any(f in clean for f in flags):
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

# --- GESTIONE MESSAGGI ---
@client.on(events.NewMessage())
async def handler(event):
    message = event.message

    try:
        if message.text and event.chat and event.chat.username:
            source = event.chat.username
            testo_formattato = format_message(message.text, source)
            await client.send_message(destination_channel, testo_formattato, file=message.media)

    except Exception as e:
        print("Errore nell'invio:", e)

print("Bot is running...")
client.run_until_disconnected()
