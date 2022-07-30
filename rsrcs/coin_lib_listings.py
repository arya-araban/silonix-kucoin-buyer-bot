import threading
import time

import requests

from config import kc_client
from kucoin.client import Client
from pynput.keyboard import Listener, KeyCode

from rsrcs.coin_lib_general import limit_buy_token
from rsrcs.useful_funcs import round_down


def keyboard_buy(coin_name, USDT, offset, cur_order_id=0):
    """ This function is similar to buy_on_time, except that it buys with keyboard presses - USED FOR NEW LISTINGS
    press 'B' to create LIMIT ORDER on fiat price.
    press 'm' to buy market price! note: may not work due to new listing constraint. """

    def buy_keypress(*key):
        nonlocal cur_order_id
        if key[0] == KeyCode.from_char('b'):
            cur_order_id = limit_buy_token(coin_name, USDT, offset)

        if key[0] == KeyCode.from_char('c'):
            kc_client.cancel_order(cur_order_id)

        if key[0] == KeyCode.from_char('m'):
            kc_client.create_market_order(coin_name + '-USDT', Client.SIDE_BUY, size=USDT)

    def key():  ## starts listener module
        with Listener(on_press=buy_keypress) as listener:
            listener.join()

    threading.Thread(target=key).start()


def _buy_on_time(coin_name, USDT, offset, desired_time_utc):
    """ DEPRECATED This function buys new listing on specified time - USED FOR NEW LISTINGS

        "USDT" is the amount of USDT to buy of the token. make sure you have enough USDT in balance
        "offset" is the upper bound percentage difference to place limit on
        "desired_time_utc"  is the time of the new listing, having on offset of 1 second late might be better.

         IE: fiat price is 100 and offset is 5%,  then order will be placed on 105, be careful when setting offset """
    my_timer = threading.Timer(1, _buy_on_time, args=[coin_name, USDT, offset, desired_time_utc])
    my_timer.start()

    now_gmt = time.strftime("%H:%M:%S", time.gmtime())
    print(now_gmt)
    if now_gmt == desired_time_utc:
        print('\n time buying new listing!')
        limit_buy_token(coin_name, USDT, offset)
        my_timer.cancel()
        # the order has happened on time, now stop this thread.
