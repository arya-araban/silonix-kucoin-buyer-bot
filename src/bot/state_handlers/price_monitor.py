# src/bot/price_monitor.py
from threading import Thread
import time
from sty import fg
from src.constants import DEFAULT_REFRESH_RATE
from src.trading.order_manager import OrderManager
from kucoin.client import Client
from config import kc_client

class PriceMonitor:
    """
    Monitors price and handles actions based on price changes.
    Methods:
        start():
            Starts monitoring in a separate thread.
        _monitor_price():
            Monitors price, tracks profit, and checks target price.
        _display_profit(profit: float):
            Displays current profit with color coding.
        _handle_target_reached():
            Places a limit order when target price is reached.
    """

    def __init__(self, coin_name: str, entry_price: float, deal_amount: float, target_price: float = None):
        self.coin_name = coin_name
        self.entry_price = entry_price
        self.target_price = target_price
        self.deal_amount = deal_amount
        self.start_time = time.time()
        self.order_manager = OrderManager()
        self.last_update_time = 0

    def start(self):
        Thread(target=self._monitor_price).start()


    def _monitor_price(self):
        while True:
            current_price = float(kc_client.get_fiat_prices(symbol=self.coin_name)[self.coin_name])
            # Handle profit tracking
            profit = round((current_price / self.entry_price * 100) - 100, 4)
            self._display_profit(profit)
            
            # Handle target price check
            if self.target_price and self.target_price <= current_price:
                self._handle_target_reached()
                break
                
            time.sleep(DEFAULT_REFRESH_RATE)

    def _display_profit(self, profit: float):
        color = f'{fg.li_green}+' if profit >= 0 else f'{fg.red}'
        print(
            f'\rTime Elapsed = {fg.blue + str(int(time.time() - self.start_time)) + fg.rs} ~ '
            f'Current Profit = {color + str(profit) + " %" + fg.rs}',
            end=" "
        )

    def _handle_target_reached(self):
        order = self.order_manager.create_limit_order(
            symbol=f'{self.coin_name}-USDT',
            side=Client.SIDE_SELL,
            price=self.target_price,
            size=self.deal_amount
        )
        print(f"\ntarget price reached! placing limit order at price {str(self.target_price)}")