import sys

from kucoin.client import Client
import config
import time

# KuCoin API values
kc_client = Client(config.api_key, config.api_secret, config.api_passphrase)
# currencies = kc_client.get_currencies(); print(currencies)

# TUNABLE PARAMETERS
DESIRED_TIME_UTC = "19:00:00"  # Put this the time in which the coin will be releasing
COIN_NAME = "BTC"
COIN_AMOUNT = 10000  # coin amount to buy. Set this a high value to buy all of your current USDT
OFFSET_PERCENTAGE = 1 / 4  # offset percentage to buy higher ie 1 means 1% higher

COIN_NAME += "-USDT"


def main():
    while True:
        nowgmt = time.strftime("%H:%M:%S", time.gmtime())
        print(nowgmt)
        if nowgmt == DESIRED_TIME_UTC:
            order = kc_client.create_market_order(COIN_NAME, Client.SIDE_BUY, size=COIN_AMOUNT)
            print(order)
            break
        time.sleep(1)


if __name__ == "__main__":  # this shows that what we are running is a script
    main()
