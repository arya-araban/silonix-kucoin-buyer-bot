from enum import Enum

class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"

class TradingSide(Enum):
    BUY = "buy"
    SELL = "sell"

### MARKET STRAT CONSTANTS: 
DEFAULT_COIN_AMOUNT = "10000000" # for market orders. 

### LIMIT STRAT CONSTANTS: 
CANCEL_ORDER_DELAY = 10


### COMMON CONSTANTS
DEFAULT_REFRESH_RATE = 0.35
DEFAULT_RETRY_DELAY = 0.25
MAX_RETRIES = 3



class SellType(Enum):
    MARKET = "market"
    LIMIT = "limit"

KEYBOARD_SELL_INSTRUCTIONS = """
Sell Instructions:
PAGE UP - Limit Sell
PAGE DOWN - Market Sell
"""