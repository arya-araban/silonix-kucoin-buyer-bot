import threading
import time
from config import kc_client
from kucoin.client import Client
from pynput.keyboard import Listener, KeyCode


def buy_on_time(coin_name, USDT, offset, desired_time_utc):
    """ This function buys new listing on specified time - USED FOR NEW LISTINGS

        "USDT" is the amount of USDT to buy of the token. make sure you have enough USDT in balance
        "offset" is the upper bound percentage difference to place limit on
        "desired_time_utc"  is the time of the new listing, having on offset of 1 second late might be better.

         IE: fiat price is 100 and offset is 5%,  then order will be placed on 105, be careful when setting offset """
    my_timer = threading.Timer(1, buy_on_time, args=[coin_name, USDT, offset, desired_time_utc])
    my_timer.start()

    now_gmt = time.strftime("%H:%M:%S", time.gmtime())
    print(now_gmt)
    if now_gmt == desired_time_utc:
        print('\n time buying new listing!')
        __limit_buy_token(coin_name, USDT, offset)
        my_timer.cancel()
        # the order has happened on time, now stop this thread. we will enable


def keyboard_buy(coin_name, USDT, offset):
    """ This function is similar to buy_on_time, except that it buys with keyboard presses - USED FOR NEW LISTINGS
    press 'B' to create LIMIT ORDER on fiat price.
    press 'm' to buy market price! note: may not work due to new listing constraint. """

    def buy_keypress(*key):
        cur_order_id = 0
        if key[0] == KeyCode.from_char('b'):
            cur_order_id = __limit_buy_token(coin_name, USDT, offset)

        if key[0] == KeyCode.from_char('c'):
            kc_client.cancel_order(cur_order_id)

        if key[0] == KeyCode.from_char('m'):
            kc_client.create_market_order(coin_name + '-USDT', Client.SIDE_BUY, size=USDT)

    def key():  ## starts listener module
        with Listener(on_press=buy_keypress) as listener:
            listener.join()

    threading.Thread(target=key).start()


def __limit_buy_token(coin_name, USDT, offset):
    """ sets a limit order based on the token name, USDT amount, and offset to the amount. - USED FOR NEW LISTINGS
    This functions is private, and used in the above functions.
     """
    cur_price = float(kc_client.get_fiat_prices(symbol=coin_name)[coin_name])  # get fiat or use asks
    cur_price += cur_price * (offset / 100)

    ord_bk_fa = kc_client.get_order_book(coin_name + '-USDT')['bids'][
        0]  # order book first order used to find decimal count
    num_decimals_price = ord_bk_fa[0][::-1].find('.')
    num_decimals_amount = ord_bk_fa[1][::-1].find('.')
    cur_price = float(f'%.{num_decimals_price}f' % cur_price)  # note cur_price always has to be float
    buy_amount = f'%.{num_decimals_amount}f' % (
            USDT / cur_price)
    order_id = kc_client.create_limit_order(coin_name + "-USDT", Client.SIDE_BUY, price=cur_price,
                                            size=buy_amount)
    print(f"limit buy order {order_id} happened!")
    return order_id
