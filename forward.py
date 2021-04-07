import sys
import socks

from telethon import events
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import PeerChannel

api_id = 3873854
api_hash = 'ed5ad4bb6de4c5c2bc9a139e9ce30a1e'
proxy = (socks.SOCKS5, '192.111.138.29', 4145)

client = TelegramClient('hub_noticias', api_id, api_hash)


chats_noticias = ('Poder360', 'spcoronavirus', 'congressoemfocotelegram',
                  'nexojornalbot', 'CNNBRASIL',  'listadapublica',
                  'SputnikBrasil', 'g1noticias', 'ForbesBra', 'ConjurOficial',
                  'boatosorgtl', 'bbcbrasil', 'brasil247oficial', 'noticiasuol',
                  'SenadoNoTelegram', 'TheInterceptBR', 'estadao',
                  'midia_ninja', 'elpaisbr', 'folha', 'vejaoficial')
chat_ids = []

async def main():
    connected = await client.connect()
    assert connected != False
    dialogs = await client.get_dialogs()
    for name in chats_noticias:
        chat = await client.get_input_entity(name)
        chat_ids.append(chat.channel_id)
    print(chat_ids)

@client.on(events.NewMessage(chats=chat_ids, incoming=True))
async def channel_message_listener(event):
    sender = await event.get_sender()
    if sender.username in chats_noticias:
        try:
            message = await client.forward_messages(entity='hubnoticia', messages=event.message)
        except ValueError as e:
            print(event)

with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()
