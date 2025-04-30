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

def extract_info(text):
    lines = text.splitlines()
    date = ''
    aircraft = ''
    seats = ''
    price = ''
    locations = []

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
                val = float(match.group(1).replace(',', '').replace('€', ''))
                price = f"€ {round(val * 1.05):,.3f}".replace(',', '.')
        elif line.startswith('🇪') or line.startswith('🇫') or line.startswith('🇩') or line.startswith('🇮') or line.startswith('🇪🇸') or line.startswith('🇩🇪') or line.startswith('🇫🇷') or line.startswith('🇬🇧'):
            locations.append(line.strip())

    route = ''
    if len(locations) >= 2:
        route = f"{locations[0]} → {locations[1]}"

    return date, aircraft, seats, price, route

@client.on(events.NewMessage(chats=source_channels))
async def handler(event):
    msg = event.message
    try:
        if msg.text:
            date, aircraft, seats, price, route = extract_info(msg.text)
            header = headers.get(event.chat.username, '✈️ BADINJETSLUX.COM')
            caption = f"{header}\n" \
                      f"📍 Route: {route}\n" \
                      f"🗓️ Date: {date}\n" \
                      f"✈️ Aircraft: {aircraft}\n" \
                      f"👥 Seats: {seats}\n" \
                      f"💶 Price: ≈ {price}\n" \
                      f"📩 Info: info@badinjetslux.com\n" \
                      f"📲 Book now: booking@badinjetslux.com\n" \
                      f"💺 EMPTY LEG AVAILABLE\n" \
                      f"📸 Follow us on Instagram: https://instagram.com/badinjetslux\n" \
                      f"🌐 www.badinjetslux.com"
            await client.send_message(destination_channel, caption, file=msg.media)
    except Exception as e:
        print("Errore:", e)

print("Bot is running...")
client.run_until_disconnected()
