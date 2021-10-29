# USED FOR PUMPS, extract coin name from the message sent in telegram channel
import time


def extract_coin_name(txt, pairing_type):
    """extract coin name from link.
    finds text between .com and -USDT which is the coin name we are looking for """
    start = '.com/'
    end = f'-{pairing_type}'
    coin_name = txt[txt.find(start) + len(start):txt.rfind(end)]
    return coin_name


def time_notification(tm):
    """print a notification of elapsed time. run this in a thread for it to be non blocking."""
    i = 1
    while True:
        time.sleep(tm)
        print(f"{tm * i} seconds have passed since order!")
        i += 1
