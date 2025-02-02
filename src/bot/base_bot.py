from abc import ABC, abstractmethod
from typing import Dict, Any
import requests
import time

class BaseBot(ABC):
    def __init__(self, channel_name: str):
        self.channel_name = channel_name

    @abstractmethod
    def run(self) -> None:
        pass

    def get_coin_details(self, coin_name: str) -> Dict[str, Any]:
        while True:
            try:
                response = requests.get(f'https://api.kucoin.com/api/v1/symbols/{coin_name}-USDT')
                return response.json()['data']
            except Exception as e:
                print(f"Error getting coin details: {e}\nRetrying...")
                time.sleep(0.25)