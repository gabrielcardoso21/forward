import sys
import socks
import asyncio

from telethon import events, errors
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import PeerChannel

api_id = 3873854
api_hash = 'ed5ad4bb6de4c5c2bc9a139e9ce30a1e'
proxy = (socks.SOCKS5, '192.111.138.29', 4145)

client = TelegramClient('hub_noticias', api_id, api_hash)


chats_noticias = ('ValorEco', 'Correio24Horas', 'nexojornalbot', 'otempo', 'ForbesBra', 'VejaNoTelegram', 'FolhadeSPaulo', 'folhanotelegram',
                    'noticiasuol', 'ExameBr', 'CNNBRASIL', 'spcoronavirus', 'g1noticias', 'boatosorgtl', 'Poder360_mv', 'Poder360',
                    'infomoney_noticias', 'SputnikBrasil', 'brasil247oficial', 'boatosefarsas', 'fakenao', 'FatoouBoato', 'TheInterceptBr',
                    'AosFatosOrg', 'senadonoticias', 'bbcbrasil', 'gazeta_do_povo', 'estadao', 'ConjurOficial', 'efarsas', 'listadapublica',
                    'midianinja', 'conjur', 'elpais_brasil')
chat_ids = []

async def main():
    connected = await client.connect()
    assert connected != False
    dialogs = await client.get_dialogs()
    for name in chats_noticias:
        chat = await client.get_input_entity(name)
        chat_ids.append(chat)
    print(chat_ids)

with client:
    client.loop.run_until_complete(main())
