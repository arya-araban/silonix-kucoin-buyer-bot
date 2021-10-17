import threading

from config import kc_client
from kucoin.client import Client

from pynput.keyboard import Listener, KeyCode


def keyboard_sell(coin_name, coin_amount):
    """This function sells with keyboard presses -  USED FOR PUMPS!
    press 'm' to sell on market
    press 'l' to sell on limit (which will be the highest buy ask for the coin)
    usually the optimal time to sell is twenty seconds after a pump, or around one minute after new listing """

    def sell_keypress(*key):
        try:
            if key[0] == KeyCode.from_char('l'):
                print('\nlimit sell!')
                cur_price = kc_client.get_order_book(coin_name + '-USDT')['asks'][0][0]
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


def keyboard_buy(coin_name, USDT, offset):
    """ This function buys with keyboard presses - USED FOR NEW LISTINGS
    press 'B' to create LIMIT ORDER on fiat price.

    "USDT" is the amount of USDT to buy of the token. make sure you have enough USDT in balance
    "offset" is the upper bound percentage difference to place limit on

     IE: fiat price is 100 and offset is 5%,  then order will be placed on 105, be careful when setting offset """

    def buy_keypress(*key):
        if key[0] == KeyCode.from_char('b'):

            print('\nlimit buy new listing!')
            cur_price = float(kc_client.get_fiat_prices(symbol=coin_name)[coin_name])  # get fiat or use asks
            cur_price += cur_price * (offset / 100)
            num_decimals = kc_client.get_order_book(coin_name + '-USDT')['bids'][0][0][::-1].find('.')
            buy_amount = f'%.{num_decimals}f' % (USDT / cur_price)
            cur_price = f'%.{num_decimals}f' % cur_price
            order_id = kc_client.create_limit_order(coin_name + "-USDT", Client.SIDE_BUY, price=cur_price,
                                                    size=buy_amount)
            print(f"limit buy order {order_id} happened!")

        if key[0] == KeyCode.from_char('m'):

            print('\nmarket buy new listing!')
            cur_price = float(kc_client.get_fiat_prices(symbol=coin_name)[coin_name])
            num_decimals = kc_client.get_order_book(coin_name + '-USDT')['bids'][0][0][::-1].find('.')
            buy_amount = f'%.{num_decimals}f' % (USDT / cur_price)
            order_id = kc_client.create_market_order(coin_name + "-USDT", Client.SIDE_BUY,
                                                    size=buy_amount)
            print(f"market buy order {order_id} happened!")

    def key():  ## starts listener module
        with Listener(on_press=buy_keypress) as listener:
            listener.join()

    my_timer = threading.Timer(0, key)
    my_timer.start()


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

    cur_price = kc_client.get_order_book(coin_name + '-USDT')['asks'][0][0]
    if target_price < cur_price:
        order = kc_client.create_limit_order(coin_name + "-USDT", Client.SIDE_SELL, price=target_price,
                                             size=coin_amount)
        print(f"{order} happened! selling on target price {str(target_price)}")
        my_timer.cancel()
