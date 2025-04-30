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
    'getjet_european_el': 'EUROPE BADINJETSLUX.COM',
    'getjet_transatlantic_el': 'TRANSATLANTIC BADINJETSLUX.COM',
    'getjet_me_el': 'MIDDLE EAST BADINJETSLUX.COM',
    'getjet_cis_el': 'CIS REGION BADINJETSLUX.COM'
}

def extract_price(raw_line):
    match = re.search(r'([€$£]?[ ]?[≈]?[ ]?[0-9.,]+)', raw_line)
    if match:
        num = match.group(1)
        num_clean = re.sub(r'[^\d,.-]', '', num).replace(',', '.')
        try:
            return round(float(num_clean) * 1.05, 2)
        except:
            return ''
    return ''

def format_message(original_text, source):
    lines = original_text.strip().split('\n')
    date = ''
    departure = ''
    arrival = ''
    aircraft = ''
    seats = ''
    price = ''

    header = headers.get(source, 'BADINJETSLUX.COM')

    for line in lines:
        if line.lower().startswith('date:'):
            date = line.split(':', 1)[1].strip()
        elif any(flag in line for flag in ['🇮🇹', '🇫🇷', '🇪🇸', '🇬🇧', '🇩🇪', '🇺🇸', '🇨🇭', '🇳🇱', '🇦🇹', '🇳🇴', '🇸🇪', '🇩🇰']):
            if not departure:
                departure = line.strip()
            else:
                arrival = line.strip()
        elif line.lower().startswith('aircraft:'):
            aircraft = line.split(':', 1)[1].strip()
        elif line.lower().startswith('seats:'):
            seats = line.split(':', 1)[1].strip()
        elif line.lower().startswith('price:'):
            price = extract_price(line)

    return f"""{header}
Route: {departure} → {arrival}
Date: {date}
Aircraft: {aircraft}
Seats: {seats}
Price: € {price if price else ''}
Info: info@badinjetslux.com
Book now: booking@badinjetslux.com
EMPTY LEG AVAILABLE
Follow us on Instagram: https://instagram.com/badinjetslux
www.badinjetslux.com
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
