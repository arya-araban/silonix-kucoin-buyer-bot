""" PUMP USING THE DISCORD API """
import multiprocessing
from threading import Thread

import requests
import config
from config import kc_client
from kucoin.client import Client
from rsrcs.useful_funcs import print_bot_name, awaiting_message
from rsrcs.coin_lib import keyboard_sell, profit_tracker, extract_discord_coin_name

# ESSENTIAL TUNABLE PARAMETERS!
CHANNEL_NAME = 'kucoin_pumps'  # kucoin_pumps OR MonacoPumpGroup OR kucoin_pump_group or pmp-tst

COIN_AMOUNT = '10000000'  # coin amount to buy. Set this a high value to buy all of your current USDT
COIN_PAIRING = 'USDT'  # type of pairing used for listing. either USDT or BTC

# NON-ESSENTIAL
TARGET_SELL_PERCENTAGE = 0
DELAY = None  # a slight delay like 0.1 might be good so the bot doesn't buy on spike

discord_channel_ids = {
    'kucoin_pumps': 957295933446565978,
    "MonacoPumpGroup": 884033922873323540,
    "kucoin_pump_group": 840108367594782760,
    "pmp_tst": 895686940563738685
}


def discord_main():
    proc = multiprocessing.Process(target=awaiting_message)
    proc.start()

    c_name = extract_discord_coin_name(channel_id=discord_channel_ids[CHANNEL_NAME], headers=config.discord_headers)

    proc.terminate()
    print(f'\r ')

    print(c_name)

    # if DELAY is not None:
    #     time.sleep(DELAY)

    order = kc_client.create_market_order(c_name + f'-{COIN_PAIRING}', Client.SIDE_BUY, size=COIN_AMOUNT)
    # print(int(time.time() * 1000))
    coin_details = requests.request('GET', 'https://api.kucoin.com' + f'/api/v1/symbols/{c_name}-USDT').json()[
        'data']
    entry_price = kc_client.get_fiat_prices(symbol=c_name)[c_name]  # or take from bid?

    print(f"{order} --- {entry_price}")

    # Thread(target=time_notification, args=[1]).start()  # starting a thread which prints time elapsed every n secs
    Thread(target=profit_tracker, args=[c_name, float(entry_price)]).start()

    keyboard_sell(coin_name=c_name,
                  coin_details=coin_details,
                  order_id=order['orderId'],
                  pairing_type=COIN_PAIRING)  # enable keypress sell option. "pg up" for limit and "pg down" for market

    # if TARGET_SELL_PERCENTAGE:
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
