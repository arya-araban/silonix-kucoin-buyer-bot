from config import kc_client, tel_client
import rsrcs.coin_lib
from kucoin.client import Client
from telethon import events
from rsrcs.useful_funcs import extract_coin_name
from rsrcs.coin_lib import sell_on_target

# ESSENTIAL TUNABLE PARAMETERS!
CHANNEL_NAME = 'pmptst'  # kucoin_pumps OR KucoinPumpChannel OR PumpItUp
COIN_AMOUNT = '100000'  # coin amount to buy. Set this a high value to buy all of your current USDT

# NON-ESSENTIAL
SELL_TARGET_PERCENTAGE = 200


def main(sell_target=False):
    @tel_client.on(events.NewMessage(chats=CHANNEL_NAME))
    async def my_event_handler(event):
        print(event.raw_text)

        c_name = extract_coin_name(event.raw_text)
        order = kc_client.create_market_order(c_name + '-USDT', Client.SIDE_BUY, size=COIN_AMOUNT)
        entry_price = kc_client.get_fiat_prices(symbol=c_name)[c_name]  # or take from bid?
        print(f"{order} --- {entry_price}")

        if sell_target:
            num_decimals = kc_client.get_order_book(c_name + '-USDT')['bids'][0][0][::-1].find('.')
            deal_amount = f'%.{num_decimals}f' % (float(kc_client.get_order(order['orderId'])['dealSize']))
            target_price = f'%.{num_decimals}f' % (float(entry_price) * ((SELL_TARGET_PERCENTAGE / 100) + 1))
            # the '%.2f' % is to limit decimals!
            sell_on_target(coin_name=c_name, target_price=target_price, coin_amount=deal_amount, time_to_check=1)

    tel_client.start()
    tel_client.run_until_disconnected()


if __name__ == "__main__":
    main(sell_target=True)
