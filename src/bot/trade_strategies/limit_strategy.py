from typing import Dict, Any, Tuple
import time
from kucoin.client import Client
from src.constants import CANCEL_ORDER_DELAY
from src.utils.formatters import round_down
from .base_strategy import BaseTradeStrategy

class LimitTradeStrategy(BaseTradeStrategy):
    def __init__(self, usdt_amount: float, order_multiplier: float):
        super().__init__()
        self.usdt_amount = usdt_amount
        self.order_multiplier = order_multiplier

    def execute_trade(self, coin_name: str, coin_details: Dict[str, Any], initial_price: float) -> Tuple[float, float]:
        order_price = initial_price * self.order_multiplier
        order_price = round_down(order_price, coin_details['priceIncrement'])
        buy_amount = round_down(self.usdt_amount / order_price, coin_details['baseIncrement'])

        order = self.order_manager.create_limit_order(
            symbol=f"{coin_name}-USDT",
            side=Client.SIDE_BUY,
            price=order_price,
            size=buy_amount
        )
        print(f"limit buy order {order} placed at price {order_price}!")
        
        self.order_manager.cancel_order(order['orderId'], delay= CANCEL_ORDER_DELAY)
        time.sleep(1)

        order_details = self.order_manager.get_order_details(order['orderId'])
        deal_amount = round_down(
            float(order_details['dealSize']) * 0.998,
            coin_details['baseIncrement']
        )

        return order_price, deal_amount