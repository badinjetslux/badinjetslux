import re
from telethon import TelegramClient, events

api_id = 22972066
api_hash = '8bec75c9c484b1ca177e722523efd9d9'

source_channels = [
    'getjet_european_el',
    'getjet_transatlantic_el',
    'getjet_me_el',
    'getjet_cis_el'
]
destination_channel = 'badinjetslux'

client = TelegramClient('badinjet_session', api_id, api_hash)

headers = {
    'getjet_european_el': '🇪🇺✈️ EUROPE BADINJETSLUX.COM',
    'getjet_transatlantic_el': '🌍✈️ TRANSATLANTIC BADINJETSLUX.COM',
    'getjet_me_el': '🌴🌟 MIDDLE EAST BADINJETSLUX.COM',
    'getjet_cis_el': '🇺🇳🛫 CIS REGION BADINJETSLUX.COM'
}

def aumenta_prezzo(test):
    pattern = re.compile(r'€\s?(\d+[.,]?\d*)')
    def incremento(match):
        numero = float(match.group(1).replace('.', '').replace(',', '').replace('€', ''))
        nuovo = round(numero * 1.05)
        return f"€ {nuovo:,}".replace(',', '.')
    return pattern.sub(incremento, test)

@client.on(events.NewMessage(chats=source_channels))
async def handler(event):
    try:
        if event.message.text:
            testo_originale = event.message.text

            # Rimuovi la riga con 'Details'
            testo_senza_details = '\n'.join([
                riga for riga in testo_originale.split('\n') if not riga.strip().lower().startswith('details')
            ])

            # Applica aumento del 5% al prezzo
            testo_modificato = aumenta_prezzo(testo_senza_details)

            # Aggiungi intestazione
            header = headers.get(event.chat.username, '✈️ BADINJETSLUX.COM')
            final_text = f"{header}\n\n{testo_modificato}\n\n📷 Follow us on Instagram: https://instagram.com/badinjetslux\n🌐 www.badinjetslux.com"

            await client.send_message(destination_channel, final_text, file=event.message.media)
    except Exception as e:
        print("Errore:", e)

print("Bot is running...")
client.start()
client.run_until_disconnected()
