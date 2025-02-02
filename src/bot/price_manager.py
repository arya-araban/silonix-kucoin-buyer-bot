import time
from config import kc_client
from src.constants import DEFAULT_REFRESH_RATE

class PriceManager:
    def __init__(self, coin_name: str, refresh_rate: float = DEFAULT_REFRESH_RATE):
        self.coin_name = coin_name
        self.refresh_rate = refresh_rate
        self.current_price = None
        self.last_update_time = 0

    def get_current_price(self) -> float:
        now = time.time()
        if now - self.last_update_time >= self.refresh_rate:
            self.current_price = float(kc_client.get_fiat_prices(symbol=self.coin_name)[self.coin_name])
            self.last_update_time = now
        return self.current_price