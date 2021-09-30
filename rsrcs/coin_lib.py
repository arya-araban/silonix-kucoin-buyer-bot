import threading

from requests import Timeout

from pump import kc_client, COIN_AMOUNT
from kucoin.client import Client


def sell_on_target(coin_name, entry_price, sell_target_percentage, time_to_check=0.3):
    """
    coin name example: 'BTC'
    entry price is the price of the succeeded order
    sell_target_percentage is the target percentage we want to sell on as soon as we hit it. IE: 100% means we want 2x
    profit time_to_check is in second.  it will check for target each n seconds. a good default value is 0.3
    """
    my_timer = threading.Timer(time_to_check, sell_on_target)
    my_timer.start()
    target_price = entry_price * ((sell_target_percentage / 100) + 1)

    if target_price < kc_client.get_fiat_prices(symbol=coin_name):
        order = kc_client.create_limit_order(coin_name + "-USDT", Client.SIDE_SELL, price=target_price,
                                             size=COIN_AMOUNT)
        print(order)
        my_timer.cancel()
