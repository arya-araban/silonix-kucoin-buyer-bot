import json
import threading
import time
from pynput.keyboard import KeyCode
from pynput import keyboard
from requests_futures.sessions import FuturesSession
from sty import fg
from config import kc_client
from rsrcs.useful_funcs import round_down, extract_coin_name
from kucoin.client import Client
from pynput.keyboard import Listener

""" GENERAL FUNCTIONS HERE (USED FOR BOTH LISTINGS & PUMPS)"""


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


""" PUMP FUNCTIONS HERE """


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


""" NEW LISTING FUNCTIONS HERE """


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
