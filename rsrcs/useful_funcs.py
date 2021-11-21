import re
import time


def extract_coin_name(txt, pairing_type):
    """extract coin name from link.
    finds text between ".com" and "-{pairing_type}"[usually USDT] which is the coin name we are looking for """
    start = '.com/'
    end = f'-{pairing_type}'

    return txt.partition(f"{start}")[2].partition(f"{end}")[0]


def time_notification(tm):
    """print a notification of elapsed time. run this in a thread for it to be non blocking."""
    i = 1
    while True:
        time.sleep(tm)
        print(f"{tm * i} seconds have passed since order!")
        i += 1
