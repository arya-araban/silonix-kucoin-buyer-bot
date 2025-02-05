from threading import Thread
from typing import Dict, Any
from pynput import keyboard
from pynput.keyboard import Listener
from kucoin.client import Client
from src.trading.order_manager import OrderManager
from src.constants import KEYBOARD_SELL_INSTRUCTIONS

class KeyboardSellHandler:
    def __init__(self, coin_name: str, deal_amount: float):
        self.coin_name = coin_name
        self.deal_amount = deal_amount
        self.order_manager = OrderManager()
        print(KEYBOARD_SELL_INSTRUCTIONS)

    def start(self):
        Thread(target=self._key_listener).start()

    def _sell_keypress(self, *key):
        try:
            if key[0] == keyboard.Key.page_up:
                self._handle_limit_sell()
            elif key[0] == keyboard.Key.page_down:
                self._handle_market_sell()
        except Exception as err:
            print("ORDER SELL FAILED")
            print(f"{err.__class__} -- {err}")

    def _handle_limit_sell(self):
        print('\nlimit sell!')
        from config import kc_client
        cur_price = kc_client.get_order_book(f'{self.coin_name}-USDT')['asks'][0][0]
        order = self.order_manager.create_limit_order(
            symbol=f'{self.coin_name}-USDT',
            side=Client.SIDE_SELL,
            price=cur_price,
            size=self.deal_amount
        )
        print(f"limit sell order {order} happened!")

    def _handle_market_sell(self):
        print('\nmarket sell!')
        order = self.order_manager.create_market_order(
            symbol=f'{self.coin_name}-USDT',
            side=Client.SIDE_SELL,
            size=self.deal_amount
        )
        print(f"market sell order {order} happened!")

    def _key_listener(self):
        with Listener(on_press=self._sell_keypress) as listener:
            listener.join()