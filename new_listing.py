import time

from config import kc_client
from rsrcs.coin_lib_listings import limit_buy_token, keyboard_buy
from rsrcs.coin_lib_pumps import keyboard_sell

COIN_NAME = 'HAWK'
DELAY = 0.45  # delay(in Milliseconds) to get coin price again as soon as listing. 0 means no update

USDT_AMOUNT = 15

OFFSET = 15  # percentage added to OG order price. ie: if price 100 retrieved and offset is 1, order price will be 101


# good numbers for offset: around 5 to 30 percent for world premiers, and 1 to 5 for normal new listings.


def main():
    while True:  # keep getting coin until it has been listed!
        coin = kc_client.get_fiat_prices(symbol=COIN_NAME)
        if not coin:  # if coin hasn't been listed yet, go on next iteration
            print('*')
            continue
        break

    cur_price = float(coin[COIN_NAME])

    if DELAY != 0:
        time.sleep(DELAY)
        cur_price = 0  # with cur_price 0, cur_price will be updated in the start of limit_buy_token

    order_id = limit_buy_token(COIN_NAME, USDT_AMOUNT, OFFSET, cur_price)

    keyboard_sell(COIN_NAME, order_id, 'USDT')  # page-up -- limit sell, page-down -- market sell

    '''
    Uncomment the following line to enable keyboard buying, this will only be used for cases where limit order hasn't 
    been successfully executed. 
    
    MAKE SURE TO CANCEL CURRENT ORDER WITH 'c', then you will be able to place a new limit order with 'b'
    '''

    # keyboard_buy(COIN_NAME, USDT_AMOUNT, OFFSET, order_id)


if __name__ == '__main__':
    main()
