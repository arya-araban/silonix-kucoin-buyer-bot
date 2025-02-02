from decimal import Decimal
import math
import time
from art import tprint
from typing import Any

def round_down(num: float, to: float) -> float:
    """Round down number to be a multiple of the given value."""
    num, to = Decimal(str(num)), Decimal(str(to))
    return float(math.floor(num / to) * to)

def print_bot_name(bot_name: str = "Silonix Trading Bot") -> None:
    tprint(bot_name, font="tarty20")

def display_waiting_animation() -> None:
    symbols = ['|', '/', '--', '\\']
    while True:
        for symbol in symbols:
            print(f'\rAwaiting Coin Message.. {symbol}', end=" ")
            time.sleep(0.5)