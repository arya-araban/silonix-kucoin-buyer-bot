from typing import Dict, Any, Tuple
import time
from kucoin.client import Client
from config import kc_client
from src.utils.formatters import round_down
from .base_strategy import BaseTradeStrategy

class MarketTradeStrategy(BaseTradeStrategy):
    def __init__(self, coin_amount: str = '10000000'):
        super().__init__()
        self.coin_amount = coin_amount

    def execute_trade(self, coin_name: str, coin_details: Dict[str, Any], **kwargs) -> Tuple[float, float]:
        order = self.order_manager.create_market_order(
            symbol=f'{coin_name}-USDT',
            side=Client.SIDE_BUY,
            size=self.coin_amount
        )
        
        entry_price = float(kc_client.get_fiat_prices(symbol=coin_name)[coin_name])
        print(f"Order: {order} --- Entry Price: {entry_price}")

        time.sleep(1)

        order_details = self.order_manager.get_order_details(order['orderId'])
        deal_amount = round_down(
            float(order_details['dealSize']) * 0.998,
            coin_details['baseIncrement']
        )

        return entry_price, deal_amount