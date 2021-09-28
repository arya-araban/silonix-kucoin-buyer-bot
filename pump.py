import sys

from kucoin.client import Client
from telethon import TelegramClient, events, sync
import config

# Telegram API values
tel_api_id = config.api_id
tel_api_hash = config.api_hash
tel_client = TelegramClient('anon', tel_api_id, tel_api_hash)

# KuCoin API values
kc_api_key = config.api_key
kc_api_secret = config.api_secret
kc_api_passphrase = config.api_passphrase
kc_client = Client(kc_api_key, kc_api_secret, kc_api_passphrase)

# TUNABLE PARAMETERS
CHANNEL_NAME = 'KucoinPumpChannel'  # kucoin_pumps OR KucoinPumpChannel
COIN_AMOUNT = sys.maxsize  # coin amount to buy. Set this a high value to buy all of your current USDT


def extract_coin_name(txt):
    start = '.com/'
    end = '-USDT'
    coin_name = txt[txt.find(start) + len(start):txt.rfind(end)] + end
    return coin_name


@tel_client.on(events.NewMessage(chats=CHANNEL_NAME))
async def my_event_handler(event):
    coin_name = extract_coin_name(event.raw_text)
    print(event.raw_text)
    order = kc_client.create_market_order(coin_name, Client.SIDE_BUY, size=20000)
    print(order)


tel_client.start()
tel_client.run_until_disconnected()
