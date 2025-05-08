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
    'getjet_cis_el']

destination_channel = 'badinjetslux'

# --- AVVIO CLIENT TELEGRAM ---
client = TelegramClient('badinjet_session', api_id, api_hash).start(bot_token=bot_token)

# --- FUNZIONE FORMATTAZIONE POST ---
def format_message(original_text, source):
    print("DEBUG: Inizio format_message")
    print(f"DEBUG: Source = {source}")
    print(f"DEBUG: Original Text = {original_text}")

    lines = original_text.strip().split('\n')
    date = 'N/A'
    aircraft = 'N/A'
    seats = 'N/A'
    price = 'N/A'
    departure = ''
    arrival = ''
    flags = ['🇦🇫','🇦🇱','🇩🇿','🇦🇸','🇦🇩','🇦🇴','🇦🇮','🇦🇶','🇦🇬','🇦🇷','🇦🇲','🇦🇼','🇦🇺','🇦🇹','🇦🇿',
    '🇧🇸','🇧🇭','🇧🇩','🇧🇧','🇧🇾','🇧🇪','🇧🇿','🇧🇯','🇧🇲','🇧🇹','🇧🇴','🇧🇦','🇧🇼','🇧🇷','🇻🇬','🇧🇳',
    '🇧🇬','🇧🇫','🇲🇲','🇧🇮','🇰🇭','🇨🇲','🇨🇦','🇨🇻','🇰🇾','🇨🇫','🇹🇩','🇨🇱','🇨🇳','🇨🇴','🇰🇲','🇨🇬',
    '🇨🇩','🇨🇷','🇭🇷','🇨🇺','🇨🇾','🇨🇿','🇩🇰','🇩🇯','🇩🇲','🇩🇴','🇪🇨','🇪🇬','🇸🇻','🇬🇶','🇪🇷','🇪🇪',
    '🇸🇿','🇪🇹','🇪🇺','🇫🇰','🇫🇴','🇫🇯','🇫🇮','🇫🇷','🇬🇫','🇵🇫','🇬🇦','🇬🇲','🇬🇪','🇩🇪','🇬🇭','🇬🇮',
    '🇬🇷','🇬🇱','🇬🇩','🇬🇵','🇬🇺','🇬🇹','🇬🇬','🇬🇳','🇬🇼','🇬🇾','🇭🇹','🇭🇳','🇭🇰','🇭🇺','🇮🇸','🇮🇳',
    '🇮🇩','🇮🇷','🇮🇶','🇮🇪','🇮🇲','🇮🇱','🇮🇹','🇨🇮','🇯🇲','🇯🇵','🇯🇪','🇯🇴','🇰🇿','🇰🇪','🇰🇮','🇽🇰',
    '🇰🇼','🇰🇬','🇱🇦','🇱🇻','🇱🇧','🇱🇸','🇱🇷','🇱🇾','🇱🇮','🇱🇹','🇱🇺','🇲🇴','🇲🇰','🇲🇬','🇲🇼','🇲🇾',
    '🇲🇻','🇲🇱','🇲🇹','🇲🇶','🇲🇷','🇲🇺','🇾🇹','🇲🇽','🇫🇲','🇲🇩','🇲🇨','🇲🇳','🇲🇪','🇲🇸','🇲🇦','🇲🇿',
    '🇲🇲','🇳🇦','🇳🇷','🇳🇵','🇳🇱','🇳🇨','🇳🇿','🇳🇮','🇳🇪','🇳🇬','🇳🇺','🇰🇵','🇲🇵','🇳🇴','🇴🇲','🇵🇰',
    '🇵🇼','🇰🇿','🇵🇸','🇵🇦','🇵🇬','🇵🇾','🇵🇪','🇵🇭','🇵🇱','🇵🇹','🇵🇷','🇶🇦','🇷🇪','🇷🇴','🇷🇺','🇷🇼','🇰🇳',
    '🇱🇨','🇻🇨','🇼🇸','🇸🇲','🇸🇹','🇸🇦','🇸🇳','🇷🇸','🇸🇨','🇸🇱','🇸🇬','🇸🇽','🇸🇰','🇸🇮','🇸🇧','🇸🇴',
    '🇿🇦','🇰🇷','🇸🇸','🇪🇸','🇱🇰','🇸🇩','🇸🇷','🇸🇿','🇸🇪','🇨🇭','🇸🇾','🇹🇼','🇹🇯','🇹🇿','🇹🇭','🇹🇱',
    '🇹🇬','🇹🇴','🇹🇹','🇹🇳','🇹🇷','🇹🇲','🇹🇻','🇺🇬','🇺🇦','🇦🇪','🇬🇧','🇺🇸','🇺🇾','🇺🇿','🇻🇺','🇻🇦',
    '🇻🇪','🇻🇳','🇾🇪','🇿🇲','🇿🇼']

    headers = {
        'getjet_european_el': '🇪🇺✈️ EUROPE BADINJETSLUX.COM',
        'getjet_transatlantic_el': '🌍✈️ TRANSATLANTIC BADINJETSLUX.COM',
        'getjet_me_el': '🌴🌟 MIDDLE EAST BADINJETSLUX.COM',
        'getjet_cis_el': '🇺🇳🛫 CIS REGION BADINJETSLUX.COM'}
    

    header = headers.get(source, '✈️ BADINJETSLUX.COM')

    for line in lines:
        clean = line.strip()

        if "Date:" in clean:
            match = re.search(r'Date:\s*(\d{2}\.\d{2}\.\d{4})', clean)
            if match:
                date = match.group(1)
                print(f"DEBUG: Estratto date = {date}")

        if "Aircraft:" in clean:
            match = re.search(r'Aircraft:\s*\**\s*(.+)', clean)
            if match:
                aircraft = match.group(1).strip()
                print(f"DEBUG: Estratto aircraft = {aircraft}")

        if "Seats:" in clean:
            match = re.search(r'Seats:\s*\**\s*(\d+)', clean)
            if match:
                seats = match.group(1)
                print(f"DEBUG: Estratto seats = {seats}")

        if "Price:" in clean:
            match = re.search(r'([0-9]+[.,]?[0-9]*)', clean.replace(',', '').replace('€', ''))
            if match:
                try:
                    val = float(match.group(1))
                    new_val = round(val * 1.10)
                    price = f"{new_val:,}".replace(",", ".")
                    print(f"DEBUG: Prezzo originale {val}, con incremento = {price}")
                except Exception as e:
                    print(f"ERROR: Errore parsing price - {e}")

        if any(flag in clean for flag in flags):
            if not departure:
                departure = clean
                print(f"DEBUG: Estratto departure = {departure}")
            elif not arrival:
                arrival = clean
                print(f"DEBUG: Estratto arrival = {arrival}")

    formatted = f"""✈️ EMPTY LEG
{header}
📍 Route: {departure} → {arrival}
🗓️ Date: {date}
✈️ Aircraft: {aircraft}
👥 Seats: {seats}
💶 Price: estimated total jet € {price}
👤 YOU CAN BUY YOUR SINGLE SEAT
📩 Info: info@badinjetslux.com
📲 Book now: booking@badinjetslux.com
💺 EMPTY LEG AVAILABLE
📸 Follow us on Instagram: https://instagram.com/badinjetslux
🌐 www.badinjetslux.com
"""
    print("DEBUG: Messaggio formattato completato.")
    return formatted

# --- EVENTO: NUOVO MESSAGGIO DA CANALI SORGENTE ---
@client.on(events.NewMessage(chats=source_channels))
async def handler(event):
    message = event.message

    try:
        content = message.text or (message.media and message.message)

        if content:
            testo_formattato = format_message(content, event.chat.username)
            await client.send_message(destination_channel, testo_formattato, file=message.media)
            print("DEBUG: Messaggio inviato al canale.")
        else:
            print("DEBUG: Nessun contenuto testuale o caption trovata, messaggio ignorato.")

    except Exception as e:
        print("ERRORE nell'invio:", e)

# --- AVVIO DEL BOT ---
print("Bot is running...")
client.run_until_disconnected()
