""" PUMP USING THE TELEGRAM API """
import multiprocessing
import time
from threading import Thread

import requests
from pyrogram import filters

from config import kc_client, tel_client
from kucoin.client import Client
from telethon import events
from rsrcs.useful_funcs import extract_coin_name, print_bot_name, awaiting_message, round_down
from rsrcs.coin_lib import sell_on_target, keyboard_sell, profit_tracker, limit_buy_token, cancel_order_sm

# ESSENTIAL TUNABLE PARAMETERS!
CHANNEL_NAME = "CryptoVIPsignalTA"  # kucoin_pumps OR MonacoPumpGroup OR kucoin_pump_group OR WSB_CryptoPumpSignal
# OR kucoinpumpswsb OR CryptoVIPsignalTA

USDT_AMOUNT = 1  # amount of USDT to put in pump. make sure you have enough USDT in your balance!
ORDER_ON_MULTIPLY_OF_OP = 2.4  # set entry limit buy order on what multiply of the original price (price before pump)
# keep this between 1.5 and 3 depending on group. good defaults: YOBI: 2.5x, JACK: 1.65x, MONACO: 1.5x,
# CryptoVIPsignalTA: 2x
# IMPORTANT: if your entry is 2x, in order to double $$ you expect 4x(300%) rise from initial price
# (if entry 1.5x, then 3x(%200)) ~~  (if entry 2.5x, then 5x(%400)) ~~ (if entry 3x, then 6x(%500))


MINUTES_BEFORE_ANNOUNCEMENT = 2  # run this script x minutes before announcement. note scraper starts 1 minute after this
# Usually 2 mins is good
# NON-ESSENTIAL
TARGET_SELL_MULTIPLIER = 3


def tel_main(sell_target=False):
    coin_prices = kc_client.get_fiat_prices()  # a dict containing the prices of all coins
    print(f"Gathered prices! awaiting {(MINUTES_BEFORE_ANNOUNCEMENT - 1)} minutes before launching message scraper...")
    time.sleep((MINUTES_BEFORE_ANNOUNCEMENT - 1) * 60)

    proc = multiprocessing.Process(target=awaiting_message)
    proc.start()

    @tel_client.on_message(filters.chat(CHANNEL_NAME))
    def from_pyrogramchat(client, message):
        c_name = extract_coin_name(message.text, pairing_type="USDT")
        # print('message')
        if not c_name:
            return

        proc.terminate()
        print(f'\r ')

        print(c_name)

        order_price = float(coin_prices[c_name]) * ORDER_ON_MULTIPLY_OF_OP
        coin_details = requests.request('GET', 'https://api.kucoin.com' + f'/api/v1/symbols/{c_name}-USDT').json()[
            'data']

        order_id = limit_buy_token(c_name, coin_details, USDT_AMOUNT, order_price)  # place limit order to buy token

        print(f"{order_id} --- {order_price}")

        Thread(target=cancel_order_sm, args=[order_id]).start()
        Thread(target=profit_tracker, args=[c_name, float(order_price)]).start()

        deal_amount = round_down(float(kc_client.get_order(order_id)['dealSize']) * 0.998,
                                 coin_details['baseIncrement'])
        keyboard_sell(coin_name=c_name, deal_amount=deal_amount,
                      pairing_type='USDT')

        if TARGET_SELL_MULTIPLIER:  # if you set target sell percentage
            target_price = round_down(order_price * TARGET_SELL_MULTIPLIER, coin_details['priceIncrement'])
            Thread(target=sell_on_target, args=[c_name, deal_amount, float(target_price), "USDT"]).start()

    tel_client.run()


if __name__ == "__main__":
    print_bot_name()
    tel_main(sell_target=False)
