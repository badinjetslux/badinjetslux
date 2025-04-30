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
    date, departure, arrival, aircraft, seats, price = '', '', '', '', '', ''
    lines = original_text.splitlines()

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
            date = line.split(":", 1)[-1].strip()
        elif re.match(r"^[🇦-🇿]{1,2}", line) and not departure:
            departure = line
        elif re.match(r"^[🇦-🇿]{1,2}", line) and departure and not arrival:
            arrival = line
        elif line.lower().startswith("aircraft:"):
            aircraft = line.split(":", 1)[-1].strip()
        elif line.lower().startswith("seats:"):
            seats = line.split(":", 1)[-1].strip()
        elif line.lower().startswith("price:"):
            match = re.search(r"([\d.,]+)", line)
            if match:
                base_price = float(match.group(1).replace(',', '').replace('€', ''))
                price = f"€ {round(base_price * 1.05, 2):,.3f}".replace(',', '.')

    return f"""{header}
📍 Route: {departure} → {arrival}
🗓️ Date: {date}
✈️ Jet: {aircraft}
👥 Seats: {seats}
💶 Estimated Price: {price}
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
            formatted = format_message(message.text, event.chat.username)
            await client.send_message(destination_channel, formatted, file=message.media)
    except Exception as e:
        print("Errore:", e)

print("Bot is running...")
client.run_until_disconnected()