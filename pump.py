from config import kc_client, tel_client
import rsrcs.coin_lib
from kucoin.client import Client
from telethon import events
from rsrcs.useful_funcs import extract_coin_name
from rsrcs.coin_lib import sell_on_target

# TUNABLE PARAMETERS!
CHANNEL_NAME = 'pmptst'  # kucoin_pumps OR KucoinPumpChannel OR PumpItUp
COIN_AMOUNT = '10000'  # coin amount to buy. Set this a high value to buy all of your current USDT


def main(sell_target=False):
    @tel_client.on(events.NewMessage(chats=CHANNEL_NAME))
    async def my_event_handler(event):
        print(event.raw_text)

        c_name = extract_coin_name(event.raw_text)
        order = kc_client.create_market_order(c_name + '-USDT', Client.SIDE_BUY, size=COIN_AMOUNT)
        print(order)

        if sell_target:
            sell_on_target(coin_name=c_name, entry_price=..., sell_target_percentage=2000, time_to_check=0.3)

    tel_client.start()
    tel_client.run_until_disconnected()


if __name__ == "__main__":
    main()
