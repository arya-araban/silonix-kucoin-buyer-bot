import json
import threading
import time

from pynput import keyboard
from requests_futures.sessions import FuturesSession
from sty import fg

from config import kc_client
from kucoin.client import Client

from pynput.keyboard import Listener, KeyCode

from rsrcs.useful_funcs import extract_coin_name


def extract_discord_coin_name(channel_id, headers):
    """This function is the main code used for discord scraping. it scraps the last message of the channel with id of
     {channel_id} each few milliseconds, and checks weather there is a coin name found for pumping or not,
     so essentially, as soon as pump message is sent out, we get the coin name - USED FOR PUMPS """
    session = FuturesSession()
    while True:

        future = session.get(f'https://discord.com/api/v9/channels/{channel_id}/messages?limit=1',
                             headers=headers)
        # print(future)

        try:
            last_msg = json.loads(future.result().text)[0]['content']
            c_name = extract_coin_name(last_msg, "USDT")
            # print(last_msg)
            if c_name:  # if c_name isn't ''
                # print(c_name)
                return c_name
        except Exception as err:
            print(f"{err.__class__} -- {err}")
            continue


def keyboard_sell(coin_name, order_id, pairing_type):
    """This function sells with keyboard presses -  USED FOR PUMPS & NEW LISTINGS!!
    press 'pg up' to sell on limit
    press 'pg down' to sell on market (which will be the highest buy ask for the coin)
    usually the optimal time to sell is twenty seconds after a pump, or around one minute after new listing """

    ord_bk_fa = kc_client.get_order_book(f"{coin_name}-{pairing_type}")['bids'][0]  # order book first order
    num_decimals_amount = ord_bk_fa[1][::-1].find('.')

    deal_amount = f'%.{num_decimals_amount}f' % (float(kc_client.get_order(order_id)['dealSize']) * 0.998)

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


def sell_on_target(coin_name, target_price, coin_amount, time_to_check, pairing_type):
    """
    USED FOR PUMPS (OPTIONALLY)

    this function places a limit order on the current price of the token being pumped as soon as it reaches the target

    coin name example: 'BTC'
    entry price is the price of the succeeded order
    sell_target_percentage is the target percentage we want to sell on as soon as we hit it. IE: 100% means we want 2x
    profit
    time_to_check is in second.  it will check for target each n seconds. a good default value is 0.8
    """

    my_timer = threading.Timer(time_to_check, sell_on_target,
                               args=[coin_name, target_price, coin_amount, time_to_check])
    my_timer.start()

    cur_price = kc_client.get_order_book(coin_name + f'-{pairing_type}')['asks'][0][0]
    if target_price < cur_price:
        order = kc_client.create_limit_order(coin_name + f'-{pairing_type}', Client.SIDE_SELL, price=target_price,
                                             size=coin_amount)
        print(f"{order} happened! selling on target price {str(target_price)}")
        my_timer.cancel()


def profit_tracker(coin_name, entry_price, refresh_rate=0.3):
    start = time.time()
    while True:
        profit = round((float(kc_client.get_fiat_prices(symbol=coin_name)[coin_name]) / entry_price * 100) - 100, 4)
        color = f'{fg.li_green}+' if profit >= 0 else f'{fg.red}'
        print(
            f'\rTime Elapsed = {fg.blue + str(int(time.time() - start)) + fg.rs} ~ Current Profit = {color + str(profit) + fg.rs}',
            end=" ")

        """below is the no time elapsed version"""
        # print(f'\rcurrent profit = {color + str(profit) + fg.rs}', end = " ")
        
        time.sleep(refresh_rate)
