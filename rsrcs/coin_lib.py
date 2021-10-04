import threading

from config import kc_client
from kucoin.client import Client

from pynput.keyboard import Listener, KeyCode


def sell_on_target(coin_name, target_price, coin_amount, time_to_check):
    """
    coin name example: 'BTC'
    entry price is the price of the succeeded order
    sell_target_percentage is the target percentage we want to sell on as soon as we hit it. IE: 100% means we want 2x
    profit time_to_check is in second.  it will check for target each n seconds. a good default value is 0.8
    """

    my_timer = threading.Timer(time_to_check, sell_on_target,
                               args=[coin_name, target_price, coin_amount, time_to_check])
    my_timer.start()

    cur_price = kc_client.get_order_book(coin_name + '-USDT')['bids'][0][0]
    if target_price < cur_price:
        order = kc_client.create_limit_order(coin_name + "-USDT", Client.SIDE_SELL, price=target_price,
                                             size=coin_amount)
        print(f"{order} happened! selling on target price {str(target_price)}")
        my_timer.cancel()


def keyboard_sell(coin_name, coin_amount):
    """This function sells with keyboard presses
    press 'm' to sell on market
    press 'l' to sell on limit (which will be the highest buy bid for the coin)
    usually the optimal time to sell is twenty seconds after a pump, or around one minute after new listing """

    def sell_keypress(*key):  ## prints key that is pressed
        # key is a tuple, so access the key(char) from key[1]
        try:
            if key[0] == KeyCode.from_char('l'):
                print('\nlimit sell!')
                cur_price = kc_client.get_order_book(coin_name + '-USDT')['bids'][0][0]
                order = kc_client.create_limit_order(coin_name + "-USDT", Client.SIDE_SELL, price=cur_price,
                                                     size=coin_amount)
                print(f"limit sell order {order} happened!")

            elif key[0] == KeyCode.from_char('m'):
                print('\nmarket sell!')
                order = kc_client.create_market_order(coin_name + '-USDT', Client.SIDE_SELL, size=coin_amount)
                print(f"market sell order {order} happened!")
        except():
            print("ORDER FAILED")

    def key():  ## starts listener module
        with Listener(on_press=sell_keypress) as listener:
            listener.join()

    my_timer = threading.Timer(0, key)
    my_timer.start()
