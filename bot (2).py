import asyncio
import re
from telethon import TelegramClient, events

api_id = 22972066
api_hash = '8bec75c9c484b1ca177e722523efd9d9'
bot_token = '7792512773:AAHClF1i3eUlZczvzmFM5j67gPdb8AplhOA'

source_channels = [
    'getjet_european_el',
    'getjet_transatlantic_el',
    'getjet_me_el',
    'getjet_cis_el'
]
destination_channel = 'badinjetslux'

client = TelegramClient('badinjet_session', api_id, api_hash).start(bot_token=bot_token)

def format_message(original_text, source):
    lines = original_text.strip().split('\n')
    date = 'N/A'
    aircraft = 'N/A'
    seats = 'N/A'
    price = 'N/A'
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
        clean_line = line.strip()
        if clean_line.lower().startswith("date"):
            date = clean_line.split(":", 1)[-1].strip()
        elif clean_line.lower().startswith("aircraft"):
            aircraft = clean_line.split(":", 1)[-1].strip()
        elif clean_line.lower().startswith("seats"):
            seats = clean_line.split(":", 1)[-1].strip()
        elif clean_line.lower().startswith("price"):
            match = re.search(r'([0-9]+[.,]?[0-9]*)', clean_line)
            if match:
                try:
                    val = float(match.group(1).replace(',', '').replace('€', '').strip())
                    price = f"{round(val * 1.05):,}".replace(",", ".")
                except:
                    price = 'N/A'
        elif any(f in clean_line for f in flags):
            if not departure:
                departure = clean_line
            elif not arrival:
                arrival = clean_line

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

@client.on(events.NewMessage(chats=source_channels))
async def handler(event):
    message = event.message
    try:
        if message.text:
            print(f"🔔 Nuovo messaggio da {event.chat.username}")
            print("📨 Testo originale:")
            print(message.text)

            testo_formattato = format_message(message.text, event.chat.username)

            print("✅ Messaggio formattato:")
            print(testo_formattato)

            await client.send_message(destination_channel, testo_formattato, file=message.media)
    except Exception as e:
        print("❌ Errore:", e)

print("🚀 Bot is running...")
client.run_until_disconnected()
