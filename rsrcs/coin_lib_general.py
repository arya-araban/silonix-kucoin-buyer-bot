import threading
import time

from pynput import keyboard
from sty import fg

from config import kc_client
from rsrcs.useful_funcs import round_down
from kucoin.client import Client
from pynput.keyboard import Listener


def keyboard_sell(coin_name, coin_details, order_id, pairing_type):
    """This function sells with keyboard presses -  USED FOR PUMPS & NEW LISTINGS!!
    press 'pg up' to sell on limit
    press 'pg down' to sell on market (which will be the highest buy ask for the coin)
    usually the optimal time to sell is twenty seconds after a pump, or around one minute after new listing """

    deal_amount = round_down(float(kc_client.get_order(order_id)['dealSize']) * 0.998, coin_details['baseIncrement'])
    print(deal_amount)

    def sell_keypress(*key):
        try:
            if key[0] == keyboard.Key.page_up:
                print('\nlimit sell!')
                cur_price = kc_client.get_order_book(coin_name + f'-{pairing_type}')['asks'][0][0]
                order = kc_client.create_limit_order(coin_name + f'-{pairing_type}', Client.SIDE_SELL, price=cur_price,
                                                     size=deal_amount)
                print(f"limit sell order {order} happened!")

            if key[0] == keyboard.Key.page_down:
                print('\nmarket sell!')
                order = kc_client.create_market_order(coin_name + f'-{pairing_type}', Client.SIDE_SELL,
                                                      size=deal_amount)
                print(f"market sell order {order} happened!")

        except Exception as err:
            print("ORDER SELL FAILED")
            print(f"{err.__class__} -- {err}")

    def key():  # starts listener module
        with Listener(on_press=sell_keypress) as listener:
            listener.join()

    threading.Thread(target=key).start()


def limit_buy_token(coin_name, coin_details, USDT_AMOUNT, cur_price):
    """ sets a limit order based on the token name, USDT amount, and price to set. - USED FOR NEW LISTINGS & PUMPS
     """

    # print(coin_details)
    cur_price = round_down(cur_price, coin_details['priceIncrement'])
    buy_amount = round_down(USDT_AMOUNT / cur_price, coin_details['baseIncrement'])

    order_id = kc_client.create_limit_order(coin_name + "-USDT", Client.SIDE_BUY, price=cur_price,
                                            size=buy_amount)
    print(f"limit buy order {order_id} placed!")
    return order_id['orderId']


def sell_on_target(coin_name, coin_details, target_price, coin_amount, pairing_type, refresh_rate=0.3):
    """

    this function places a limit order on the current price of the token being pumped as soon as it reaches the target

    coin name example: 'BTC'
    entry price is the price of the succeeded order
    sell_target_percentage is the target percentage we want to sell on as soon as we hit it. IE: 100% means we want 2x
    profit
    time_to_check is in second.  it will check for target each n seconds. a good default value is 0.8
    """

    while True:

        cur_price = kc_client.get_order_book(coin_name + f'-{pairing_type}')['asks'][0][0]
        if target_price < cur_price:
            order = kc_client.create_limit_order(coin_name + f'-{pairing_type}', Client.SIDE_SELL, price=target_price,
                                                 size=coin_amount)
            print(f"{order} happened! selling on target price {str(target_price)}")


def profit_tracker(coin_name, entry_price, refresh_rate=0.3):
    start = time.time()
    while True:
        profit = round((float(kc_client.get_fiat_prices(symbol=coin_name)[coin_name]) / entry_price * 100) - 100, 4)
        color = f'{fg.li_green}+' if profit >= 0 else f'{fg.red}'
        print(
            f'\rTime Elapsed = {fg.blue + str(int(time.time() - start)) + fg.rs} ~ Current Profit = {color + str(profit) + " %" + fg.rs} ',
            end=" ")

        time.sleep(refresh_rate)
