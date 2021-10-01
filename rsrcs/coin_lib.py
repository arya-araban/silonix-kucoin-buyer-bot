import threading

from config import kc_client
from kucoin.client import Client


def sell_on_target(coin_name, target_price, coin_amount, time_to_check=0.3):
    """
    coin name example: 'BTC'
    entry price is the price of the succeeded order
    sell_target_percentage is the target percentage we want to sell on as soon as we hit it. IE: 100% means we want 2x
    profit time_to_check is in second.  it will check for target each n seconds. a good default value is 0.3
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
