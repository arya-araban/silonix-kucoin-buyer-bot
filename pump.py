import sys
import time
import threading
from kucoin.client import Client
from telethon import TelegramClient, events
import config

# Telegram API values
tel_client = TelegramClient('anon', config.api_id, config.api_hash)

# KuCoin API values
kc_client = Client(config.api_key, config.api_secret, config.api_passphrase)

# TUNABLE PARAMETERS ESSENTIALS!
CHANNEL_NAME = 'pmptst'  # kucoin_pumps OR KucoinPumpChannel OR PumpItUp
COIN_AMOUNT = '10000'  # coin amount to buy. Set this a high value to buy all of your current USDT


def sell_on_target(sell_target_percentage=100, time_to_check=0.3):
    """
    sell_target_percentage is the target percentage we want to sell on as soon as we hit it. IE: 100% means we want 2x
    profit time_to_check is in second.  it will check for target each n seconds. a good default value is 0.2
    """
    threading.Timer(time_to_check, sell_on_target).start()
    print("Hello, World!")


def extract_coin_name(txt):
    start = '.com/'
    end = '-USDT'
    coin_name = txt[txt.find(start) + len(start):txt.rfind(end)] + end
    return coin_name


def main(sell_target=False):
    @tel_client.on(events.NewMessage(chats=CHANNEL_NAME))
    async def my_event_handler(event):
        print(event.raw_text)

        coin_name = extract_coin_name(event.raw_text)
        order = kc_client.create_market_order(coin_name, Client.SIDE_BUY, size=COIN_AMOUNT)
        print(order)

    if sell_target:
        sell_on_target()

    tel_client.start()
    tel_client.run_until_disconnected()


if __name__ == "__main__":
    main(sell_target=True)
