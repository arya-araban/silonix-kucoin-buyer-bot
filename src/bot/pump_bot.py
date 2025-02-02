import multiprocessing
from typing import Dict, Any
from config import kc_client, tel_client
from pyrogram import filters
from src.utils.formatters import round_down, display_waiting_animation
from src.utils.telegram_utils import extract_coin_name
from src.constants import OrderType
from src.bot.price_manager import PriceManager
from src.trading.profit_tracker import ProfitTracker
from src.bot.trade_strategies.market_strategy import MarketTradeStrategy
from src.bot.trade_strategies.limit_strategy import LimitTradeStrategy
from src.bot.sell_handlers.keyboard_sell_handler import KeyboardSellHandler
from src.bot.sell_handlers.target_sell_handler import TargetSellHandler
from .base_bot import BaseBot

class PumpBot(BaseBot):
    def __init__(self, channel_name: str, strategy: str = OrderType.MARKET.value, **kwargs):
        super().__init__(channel_name)
        self.strategy = strategy
        self.target_sell_multiplier = kwargs.get('target_sell_multiplier', 0)
        self.prepump_prices = None
        
        if strategy == OrderType.LIMIT.value:
            self.trade_strategy = LimitTradeStrategy(
                usdt_amount=kwargs['usdt_amount'],
                order_multiplier=kwargs['order_multiplier']
            )
            self.prepump_prices = None
        else:
            self.trade_strategy = MarketTradeStrategy()

    def run(self) -> None:
        proc = multiprocessing.Process(target=display_waiting_animation)
        proc.start()

        if self.strategy == OrderType.LIMIT.value:
            self.prepump_prices = kc_client.get_fiat_prices()
            print("Gathered prepump prices! Launching message scraper...")
            
        self._run_telegram(proc)

    def _handle_trade(self, coin_name: str):
        coin_details = self.get_coin_details(coin_name)
        
        if self.strategy == OrderType.MARKET.value:
            entry_price, deal_amount = self.trade_strategy.execute_trade(coin_name, coin_details)
        else:
            initial_price = float(self.prepump_prices[coin_name])
            entry_price, deal_amount = self.trade_strategy.execute_trade(
                coin_name, 
                coin_details, 
                initial_price=initial_price
            )

        price_manager = PriceManager(coin_name)
        ProfitTracker.track_profit(price_manager.get_current_price, entry_price)

        self._setup_sell_handlers(coin_name, deal_amount, entry_price, coin_details, price_manager)

    def _setup_sell_handlers(
        self,
        coin_name: str,
        deal_amount: float,
        entry_price: float,
        coin_details: Dict[str, Any],
        price_manager: PriceManager
    ) -> None:
        keyboard_handler = KeyboardSellHandler(coin_name, deal_amount)
        keyboard_handler.start()

        if self.target_sell_multiplier:
            target_price = round_down(
                entry_price * self.target_sell_multiplier,
                coin_details['priceIncrement']
            )
            print(f"AutoTarget active on {self.target_sell_multiplier}x | Target price: {target_price}")
            
            target_handler = TargetSellHandler(coin_name, deal_amount, target_price, price_manager)
            target_handler.start()

    def _run_telegram(self, proc: multiprocessing.Process) -> None:
        @tel_client.on_message(filters.chat(self.channel_name))
        def handle_message(client, message):
            coin_name = extract_coin_name(message.text, pairing_type="USDT")
            if not coin_name:
                return

            proc.terminate()
            print(f'\r')
            
            self._handle_trade(coin_name)

        tel_client.run()