import math
import time
from decimal import Decimal

from art import tprint
from sty import fg


def extract_coin_name(txt, pairing_type='USDT'):
    """extract coin name from KuCoin trading link using partitioning.
    finds text between ".com" and "-{pairing_type}"[usually USDT] which is the coin name we are looking for """
    start = '/trade'
    end = f'-{pairing_type}'
    return txt.partition(start)[2].partition(end)[0].partition("/")[2].partition(end)[0]


def round_down(num: float, to: float) -> float:
    """ round down 'num' to be a multiple of 'to' """
    num, to = Decimal(str(num)), Decimal(str(to))
    return float(math.floor(num / to) * to)


def awaiting_message():
    symb = ['|', '/', '--', '\\']
    while True:
        for s in symb:
            print(f'\rAwaiting Coin Message.. {s}', end=" ")
            time.sleep(0.5)


def print_bot_name(bot_name=f"Silonix Trading Bot"):
    tprint(bot_name, font="tarty20")  # tarty3,tarty10, tarty20 chunky,small,ogre
