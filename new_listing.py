import time
from rsrcs.coin_lib import keyboard_buy, buy_on_time

# TUNABLE PARAMETERS
DESIRED_TIME_UTC = "14:48:05"  # Put this the time in which the coin will be releasing
COIN_NAME = "BTC"

USDT_AMOUNT = 2  # amount of usdt to buy with. make sure this is less than your current USDT balance
PRICE_OFFSET_PERCENTAGE = 100  # offset percentage to buy higher ie 1 means 1% higher. 0 means no price offset


# around 10 to 50 percent for world premiers, and 1 to 5 for normal new listings.

def main():
    while True:
        nowgmt = time.strftime("%H:%M:%S", time.gmtime())
        print(nowgmt)
        if nowgmt == DESIRED_TIME_UTC:
            print("buying open! press 'b' to buy!")
            keyboard_buy(COIN_NAME, USDT=USDT_AMOUNT, offset=PRICE_OFFSET_PERCENTAGE)
            break
        time.sleep(1)


def main2():
    buy_on_time(COIN_NAME, USDT=USDT_AMOUNT, offset=PRICE_OFFSET_PERCENTAGE,
                desired_time_utc=DESIRED_TIME_UTC)

    keyboard_buy(COIN_NAME, USDT=USDT_AMOUNT, offset=PRICE_OFFSET_PERCENTAGE)


if __name__ == "__main__":
    main2()
