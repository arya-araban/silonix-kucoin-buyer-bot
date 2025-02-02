from threading import Thread
import time
from kucoin.client import Client
from src.trading.order_manager import OrderManager
from src.bot.price_manager import PriceManager

class TargetSellHandler:
    def __init__(self, coin_name: str, deal_amount: float, target_price: float, price_manager: PriceManager):
        self.coin_name = coin_name
        self.deal_amount = deal_amount
        self.target_price = target_price
        self.price_manager = price_manager
        self.order_manager = OrderManager()

    def start(self):
        Thread(target=self._monitor_target_price).start()

    def _monitor_target_price(self):
        while True:
            current_price = self.price_manager.get_current_price()
            if self.target_price <= current_price:
                order = self.order_manager.create_limit_order(
                    symbol=f'{self.coin_name}-USDT',
                    side=Client.SIDE_SELL,
                    price=self.target_price,
                    size=self.deal_amount
                )
                print(f"target price reached! placing limit order at price {str(self.target_price)}")
                break
            time.sleep(self.price_manager.refresh_rate)