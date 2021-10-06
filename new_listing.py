from config import kc_client
from kucoin.client import Client
import time
from rsrcs.coin_lib import keyboard_buy

# TUNABLE PARAMETERS
DESIRED_TIME_UTC = "16:54:00"  # Put this the time in which the coin will be releasing
COIN_NAME = "ROUTE"
COIN_AMOUNT = '10000'  # coin amount to buy. Set this a high value to buy all of your current USDT

USDT_AMOUNT = 40  # amount of usdt to buy with. make sure this is less than your current USDT balance
PRICE_OFFSET_PERCENTAGE = 0.25  # offset percentage to buy higher ie 1 means 1% higher. 0 means no price offset


# around 5 to 10 percent for world premiers, and 1 to 5 for normal new listings.


def market_order():
    while True:
        nowgmt = time.strftime("%H:%M:%S", time.gmtime())
        print(nowgmt)
        if nowgmt == DESIRED_TIME_UTC:
            order = kc_client.create_market_order(COIN_NAME + "-USDT", Client.SIDE_BUY, size=COIN_AMOUNT)
            print(order)
            break
        time.sleep(1)


def main():
    while True:
        nowgmt = time.strftime("%H:%M:%S", time.gmtime())
        print(nowgmt)
        if nowgmt == DESIRED_TIME_UTC:
            print("buying open! press 'b' to buy!")
            keyboard_buy(COIN_NAME, USDT=USDT_AMOUNT, offset=PRICE_OFFSET_PERCENTAGE)
            break
        time.sleep(1)


if __name__ == "__main__":
    main()
