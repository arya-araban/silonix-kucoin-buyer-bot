from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple
from src.trading.order_manager import OrderManager

class BaseTradeStrategy(ABC):
    def __init__(self):
        self.order_manager = OrderManager()

    @abstractmethod
    def execute_trade(self, coin_name: str, coin_details: Dict[str, Any], **kwargs) -> Tuple[float, float]:
        """Returns (entry_price, deal_amount)"""
        pass


    