import sys

from kucoin.client import Client
import config
import time

# KuCoin API values
kc_client = Client(config.api_key, config.api_secret, config.api_passphrase)
# currencies = kc_client.get_currencies(); print(currencies)

# TUNABLE PARAMETERS
DESIRED_TIME_UTC = "22:07:10"  # Put this the time in which the coin will be releasing
COIN_NAME = "BTC"
COIN_AMOUNT = '10000'  # coin amount to buy. Set this a high value to buy all of your current USDT
PRICE_OFFSET_PERCENTAGE = 1 / 4  # offset percentage to buy higher ie 1 means 1% higher. 0 means no price offset

COIN_NAME += "-USDT"


def market_order():
    while True:
        nowgmt = time.strftime("%H:%M:%S", time.gmtime())
        print(nowgmt)
        if nowgmt == DESIRED_TIME_UTC:
            order = kc_client.create_market_order(COIN_NAME, Client.SIDE_BUY, size=COIN_AMOUNT)
            print(order)
            break
        time.sleep(1)


def limit_order():
    while True:
        nowgmt = time.strftime("%H:%M:%S", time.gmtime())
        print(nowgmt)
        if nowgmt == DESIRED_TIME_UTC:
            coin_price = kc_client.get_fiat_prices(base="USD", symbol="BTC")
            coin_price += coin_price * (PRICE_OFFSET_PERCENTAGE / 100)
            order = kc_client.create_limit_order(COIN_NAME, Client.SIDE_BUY, price=coin_price, size=COIN_AMOUNT)
            print(order)
            break
        time.sleep(1)


if __name__ == "__main__":  # this shows that what we are running is a script
    market_order()