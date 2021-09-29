import sys

from kucoin.client import Client
from telethon import TelegramClient, events
import config

# Telegram API values
tel_client = TelegramClient('anon', config.api_id, config.api_hash)

# KuCoin API values
kc_client = Client(config.api_key, config.api_secret, config.api_passphrase)

# TUNABLE PARAMETERS
CHANNEL_NAME = 'pmptst'  # kucoin_pumps OR KucoinPumpChannel
COIN_AMOUNT = 10000  # coin amount to buy. Set this a high value to buy all of your current USDT


def extract_coin_name(txt):
    start = '.com/'
    end = '-USDT'
    coin_name = txt[txt.find(start) + len(start):txt.rfind(end)] + end
    return coin_name


def main():
    @tel_client.on(events.NewMessage(chats=CHANNEL_NAME))
    async def my_event_handler(event):
        print(event.raw_text)

        coin_name = extract_coin_name(event.raw_text)
        order = kc_client.create_market_order(coin_name, Client.SIDE_BUY, size=COIN_AMOUNT)
        print(order)

    tel_client.start()
    tel_client.run_until_disconnected()


if __name__ == "__main__":
    main()
