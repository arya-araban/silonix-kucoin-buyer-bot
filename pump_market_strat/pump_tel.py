""" PUMP USING THE TELEGRAM API """
import multiprocessing
from threading import Thread

import requests
from pyrogram import filters

from config import kc_client, tel_client
from kucoin.client import Client
from rsrcs.useful_funcs import extract_coin_name, print_bot_name, awaiting_message, round_down
from rsrcs.coin_lib import sell_on_target, keyboard_sell, profit_tracker

# ESSENTIAL TUNABLE PARAMETERS!
CHANNEL_NAME = "pmptst"  # kucoin_pumps OR MonacoPumpGroup OR kucoin_pump_group OR WSB_CryptoPumpSignal
# OR kucoinpumpswsb OR CryptoVIPsignalTA

COIN_AMOUNT = '10000000'  # coin amount to buy. Set this a high value to buy all of your current USDT
COIN_PAIRING = 'USDT'  # type of pairing used for listing. either USDT or BTC

# NON-ESSENTIAL
TARGET_SELL_MULTIPLIER = 0  # after reaching what multiple of your entry price should sell order be placed (0 for not activating)
DELAY = None  # a slight delay like 0.1 might be good so the bot doesn't buy on spike


def tel_main(sell_target=False):
    proc = multiprocessing.Process(target=awaiting_message)
    proc.start()

    @tel_client.on_message(filters.chat(CHANNEL_NAME))
    def from_pyrogramchat(client, message):
        c_name = extract_coin_name(message.text, pairing_type=COIN_PAIRING)
        # print('message')
        if not c_name:
            return

        proc.terminate()
        print(f'\r ')

        print(c_name)

        order = kc_client.create_market_order(c_name + f'-{COIN_PAIRING}', Client.SIDE_BUY, size=COIN_AMOUNT)
        entry_price = kc_client.get_fiat_prices(symbol=c_name)[c_name]  # or take from bid?
        print(f"{order} --- {entry_price}")

        Thread(target=profit_tracker, args=[c_name, float(entry_price)]).start()

        coin_details = requests.request('GET', 'https://api.kucoin.com' + f'/api/v1/symbols/{c_name}-USDT').json()[
            'data']
        deal_amount = round_down(float(kc_client.get_order(order['orderId'])['dealSize']) * 0.998,
                                 coin_details['baseIncrement'])

        keyboard_sell(coin_name=c_name,
                      deal_amount=deal_amount,
                      pairing_type=COIN_PAIRING)  # enable keypress sell option. "pg up" for limit and "pg down" for market

        if TARGET_SELL_MULTIPLIER:  # if you set target sell percentage
            target_price = round_down(float(entry_price) * TARGET_SELL_MULTIPLIER, coin_details['priceIncrement'])
            Thread(target=sell_on_target, args=[c_name, deal_amount, float(target_price), "USDT"]).start()

    tel_client.run()


if __name__ == "__main__":
    print_bot_name()
    tel_main(sell_target=False)
