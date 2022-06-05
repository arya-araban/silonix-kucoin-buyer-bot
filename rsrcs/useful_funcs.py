import time
from art import tprint
from sty import fg


def extract_coin_name(txt, pairing_type='USDT'):
    """extract coin name from link.
    finds text between ".com" and "-{pairing_type}"[usually USDT] which is the coin name we are looking for """
    start = '/trade'
    end = f'-{pairing_type}'
    return txt.partition(start)[2].partition(end)[0].partition("/")[2].partition(end)[0]


def time_notification(tm):
    """print a notification of elapsed time. run this in a thread for it to be non blocking."""
    i = 0
    while True:
        print(f'\r {fg.cyan + str(tm * i) + fg.rs} seconds have passed since order!', end=" ")
        time.sleep(tm)
        i += 1


def awaiting_message():
    symb = ['|', '/', '--', '\\']
    while True:
        for s in symb:
            print(f'\rAwaiting Coin Message.. {s}', end=" ")
            time.sleep(0.5)


def print_bot_name(bot_name=f"Silonix Trading Bot"):
    tprint(bot_name, font="tarty20")  # tarty3,tarty10, tarty20 chunky,small,ogre
