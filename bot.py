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

headers = {
    'getjet_european_el': '🇪🇺✈️ EUROPE BADINJETSLUX.COM',
    'getjet_transatlantic_el': '🌍✈️ TRANSATLANTIC BADINJETSLUX.COM',
    'getjet_me_el': '🌴🌟 MIDDLE EAST BADINJETSLUX.COM',
    'getjet_cis_el': '🇺🇳🛫 CIS REGION BADINJETSLUX.COM'
}

def format_message(original_text, source):
    lines = original_text.strip().split('\n')
    date = ''
    departure = ''
    arrival = ''
    aircraft = ''
    seats = ''
    price = ''

    for line in lines:
        if line.startswith('Date:'):
            date = line.replace('Date:', '').strip()
        elif line.startswith('Aircraft:'):
            aircraft = line.replace('Aircraft:', '').strip()
        elif line.startswith('Seats:'):
            seats = line.replace('Seats:', '').strip()
        elif line.startswith('Price:'):
            match = re.search(r'(\d+[.,]?\d*)', line)
            if match:
                try:
                    price_val = float(match.group(1).replace(',', '.'))
                    price = f"≈ € {round(price_val * 1.05, 3)}"
                except:
                    pass
        elif '→' not in line and any(flag in line for flag in ['🇮🇹', '🇫🇷', '🇪🇸', '🇬🇧', '🇩🇪', '🇨🇿', '🇩🇰']):
            if not departure:
                departure = line.strip()
            else:
                arrival = line.strip()

    header = headers.get(source, '✈️ BADINJETSLUX.COM')

    return f"""{header}
📍 Route: {departure} → {arrival}
🗓️ Date: {date}
✈️ Aircraft: {aircraft}
👥 Seats: {seats}
💶 Price: {price}
📩 Info: info@badinjetslux.com
📲 Book now: booking@badinjetslux.com
💺 EMPTY LEG AVAILABLE
📸 Follow us on Instagram: https://instagram.com/badinjetslux
🌐 www.badinjetslux.com"""

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
