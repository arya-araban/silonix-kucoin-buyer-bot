""" PUMP USING THE DISCORD API """
import multiprocessing
import time
from threading import Thread
import requests
import config
from config import kc_client
from rsrcs.coin_lib import limit_buy_token, extract_discord_coin_name, keyboard_sell, profit_tracker, sell_on_target
from rsrcs.useful_funcs import print_bot_name, awaiting_message, round_down

# ESSENTIAL TUNABLE PARAMETERS!
CHANNEL_NAME = 'kucoin_pump_group'  # kucoin_pumps OR MonacoPumpGroup OR kucoin_pump_group or pmp-tst

USDT_AMOUNT = 75  # amount of USDT to put in pump. make sure you have enough USDT in your balance!
ORDER_ON_MULTIPLY_OF_OP = 2  # set entry limit buy order on what multiply of the original price (price before pump)
# keep this between 1.5 and 3 depending on group. good defaults: YOBI: 2.5x, JACK: 1.65x, MONACO: 1.5x
# IMPORTANT: if your entry is 2x, in order to double $$ you expect 4x(300%) rise from initial price
# (if entry 3x, then 6x(%500))

MINUTES_BEFORE_ANNOUNCEMENT = 2  # run this script x minutes before announcement

# NON-ESSENTIAL
TARGET_SELL_MULTIPLIER = 2  # after reaching what multiple of your entry price should sell order be placed (0 for not activating)

discord_channel_ids = {
    'kucoin_pumps': 957295933446565978,
    "MonacoPumpGroup": 884033922873323540,
    "kucoin_pump_group": 840108367594782760,
    "pmp_tst": 895686940563738685
}


def discord_main():
    coin_prices = kc_client.get_fiat_prices()  # a dict containing the prices of all coins
    print(f"Gathered prices! awaiting {(MINUTES_BEFORE_ANNOUNCEMENT - 1)} minutes before launching message scraper...")
    time.sleep((MINUTES_BEFORE_ANNOUNCEMENT - 1) * 60)
    proc = multiprocessing.Process(target=awaiting_message)
    proc.start()

    c_name = extract_discord_coin_name(channel_id=discord_channel_ids[CHANNEL_NAME], headers=config.discord_headers)

    proc.terminate()
    print(f'\r ')

    print(c_name)

    order_price = float(coin_prices[c_name]) * ORDER_ON_MULTIPLY_OF_OP
    coin_details = requests.request('GET', 'https://api.kucoin.com' + f'/api/v1/symbols/{c_name}-USDT').json()[
        'data']

    order_id = limit_buy_token(c_name, coin_details, USDT_AMOUNT, order_price)  # place limit order to buy token

    print(f"{order_id} --- {order_price}")

    Thread(target=profit_tracker, args=[c_name, float(order_price)]).start()

    deal_amount = round_down(float(kc_client.get_order(order_id)['dealSize']) * 0.998, coin_details['baseIncrement'])
    keyboard_sell(coin_name=c_name, deal_amount=deal_amount,
                  pairing_type='USDT')  # enable keypress sell option. "pg up" for limit and "pg down" for market

    if TARGET_SELL_MULTIPLIER:  # if you set target sell percentage
        target_price = round_down(order_price * TARGET_SELL_MULTIPLIER, coin_details['priceIncrement'])
        Thread(target=sell_on_target, args=[c_name, deal_amount, float(target_price), "USDT"]).start()


if __name__ == "__main__":
    print_bot_name()
    discord_main()
