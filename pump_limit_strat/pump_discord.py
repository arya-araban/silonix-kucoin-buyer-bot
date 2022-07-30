""" PUMP USING THE DISCORD API """
import multiprocessing
import time
from threading import Thread
import requests
import config
from config import kc_client
from rsrcs.coin_lib import limit_buy_token, extract_discord_coin_name, keyboard_sell, profit_tracker
from rsrcs.useful_funcs import print_bot_name, awaiting_message

# ESSENTIAL TUNABLE PARAMETERS!
CHANNEL_NAME = 'pmp_tst'  # kucoin_pumps OR MonacoPumpGroup OR kucoin_pump_group or pmp-tst

USDT_AMOUNT = 2  # amount of USDT to put in pump. make sure you have enough USDT in your balance!
ORDER_ON_MULTIPLY_OF_OP = 1  # set limit order on what multiply of the original price (price before pump)
# keep this between 1.5 and 3 depending on group. good defaults: YOBI: 3x, JACK: 2x, MONACO: 2x


MINUTES_BEFORE_ANNOUNCEMENT = 1.1  # run this script x minutes before announcement

# NON-ESSENTIAL
TARGET_SELL_PERCENTAGE = 0

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

    order_price = coin_prices[c_name] * ORDER_ON_MULTIPLY_OF_OP
    coin_details = requests.request('GET', 'https://api.kucoin.com' + f'/api/v1/symbols/{c_name}-USDT').json()[
        'data']

    order_id = limit_buy_token(c_name, coin_details, USDT_AMOUNT, order_price)  # place limit order to buy token

    print(f"{order_id} --- {order_price}")

    # Thread(target=time_notification, args=[1]).start()  # starting a thread which prints time elapsed every n secs
    Thread(target=profit_tracker, args=[c_name, float(order_price)]).start()

    keyboard_sell(coin_name=c_name, coin_details=coin_details,
                  order_id=order_id,
                  pairing_type='USDT')  # enable keypress sell option. "pg up" for limit and "pg down" for market

    # if TARGET_SELL_PERCENTAGE:  # if you set target sell percentage
    #     ord_bk_fa = kc_client.get_order_book(c_name + f'-{COIN_PAIRING}')['bids'][0]  # order book first order
    #     num_decimals_price = ord_bk_fa[0][::-1].find('.')
    #     num_decimals_amount = ord_bk_fa[1][::-1].find('.')
    #     deal_amount = f'%.{num_decimals_amount}f' % (float(kc_client.get_order(order['orderId'])['dealSize']) * 0.998)
    #     target_price = f'%.{num_decimals_price}f' % (float(entry_price) * ((TARGET_SELL_PERCENTAGE / 100) + 1))
    #     # the '%.2f' % is to limit decimals!
    #     sell_on_target(coin_name=c_name, target_price=target_price, coin_amount=deal_amount, time_to_check=0.8,
    #                    pairing_type=COIN_PAIRING)


if __name__ == "__main__":
    print_bot_name()
    discord_main()
