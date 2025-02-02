#!/usr/bin/env python3
from src.utils.formatters import print_bot_name
from src.bot.pump_bot import PumpBot

def main():
    print_bot_name()
    
  
    bot = PumpBot(
        channel_name='pmptst',
        strategy='limit',
        usdt_amount=1,
        order_multiplier=1.00,
        target_sell_multiplier=0
    )

    # Example configuration for market strategy
    # bot = PumpBot(
    #     channel_name='pmptst',
    #     strategy='market',
    #     target_sell_multiplier=0
    # )

    bot.run()

if __name__ == "__main__":
    main()