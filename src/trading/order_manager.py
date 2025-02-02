import time
from threading import Thread
from typing import Dict, Any
from kucoin.client import Client
from config import kc_client
from src.utils.formatters import round_down
from src.constants import MAX_RETRIES, DEFAULT_RETRY_DELAY

from kucoin.exceptions import KucoinAPIException

class OrderManager:
    @staticmethod
    def create_market_order(symbol: str, side: str, size: str) -> Dict[str, Any]:
        return kc_client.create_market_order(
            symbol=symbol,
            side=side,
            size=size,
            clientOid=str(int(time.time() * 1000))
        )

    @staticmethod
    def create_limit_order(symbol: str, side: str, price: float, size: float, max_retries: int = MAX_RETRIES) -> Dict[str, Any]:
        
        for attempt in range(max_retries):
            try:
                return kc_client.create_limit_order(
                    symbol=symbol,
                    side=side,
                    price=price,
                    size=size
                )
            
            except KucoinAPIException as e:
                if e.code == '400201' and attempt < max_retries - 1:  # Invalid KC-API-PARTNER-SIGN
                    print(f"API signing error, retrying... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(DEFAULT_RETRY_DELAY * (attempt + 1))  # Exponential backoff
                    continue
                raise e
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Order error: {str(e)}, retrying... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(DEFAULT_RETRY_DELAY * (attempt + 1))
                    continue
                raise e


    @staticmethod
    def get_order_details(order_id: str, max_retries: int = MAX_RETRIES) -> Dict[str, Any]:
        for attempt in range(max_retries):
            try:
                return kc_client.get_order(order_id)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                time.sleep(DEFAULT_RETRY_DELAY)

    @staticmethod
    def cancel_order(order_id: str, delay: int = 10) -> None:
        def delayed_cancel():
            time.sleep(delay)
            try:
                kc_client.cancel_order(order_id)
                print("Order cancelled due to timeout")
            except:
                pass

        Thread(target=delayed_cancel).start()