import sys
import socks
import asyncio

from datetime import datetime, timedelta, timezone

from telethon import events, errors
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import PeerChannel, InputMessagesFilterEmpty, User, ChannelAdminLogEventActionParticipantLeave, \
    ChannelAdminLogEventActionParticipantJoin
from telethon.tl.functions.messages import SearchRequest
from telethon.tl.functions.channels import GetFullChannelRequest

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
    hubnoticia = await client.get_input_entity('hubnoticia')
    joined = []
    left = []
    total_organic = 0
    total_buy = 0
    async for event in client.iter_admin_log(hubnoticia):
        if isinstance(event.action, ChannelAdminLogEventActionParticipantLeave):
            left.append(event.user_id)
        elif isinstance(event.action, ChannelAdminLogEventActionParticipantJoin):
            joined.append(event)
    for event in joined:
        if event.user_id not in left:
            if event.date > datetime(2021, 3, 6, 15, 6, 42, tzinfo=timezone.utc):
                total_organic += 1
                print("User: %s, joined %s" % (event.user_id, event.date))
            else:
                total_buy += 1
    resultant = [u for u in joined if u.user_id not in left]
    print("total left: %s" % len(resultant))
    print("Organic: %s, Purchased: %s" % (total_organic, total_buy))
#    print(await client(GetFullChannelRequest(hubnoticia)))

async def dull():
    subscribers = {}
    iter = client.iter_participants(hubnoticia)
    empty = False
    while not empty:
        async for u in iter:
            subscribers[u.id] = u
        for s, u in subscribers.items():
            print("User: %s, %s" % (u.id, u.first_name))
        empty = await iter._load_next_chunk()
    print("Total: %s" % len(subscribers.keys()))
    async for event in client.iter_admin_log(hubnoticia, join=True):
        print("%s \n" % event)
    print("Organic: %s, Purchased: %s" % (total_organic, total_buy))

with client:
    client.loop.run_until_complete(main())
