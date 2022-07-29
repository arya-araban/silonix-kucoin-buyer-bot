""" PUMP USING THE TELEGRAM API """
import multiprocessing
from threading import Thread
from config import kc_client, tel_client
from kucoin.client import Client
from telethon import events
from rsrcs.useful_funcs import extract_coin_name, time_notification, print_bot_name, awaiting_message
from rsrcs.coin_lib_pumps import sell_on_target, keyboard_sell, profit_tracker

# ESSENTIAL TUNABLE PARAMETERS!
CHANNEL_NAME = "kucoinpumpswsb"  # kucoin_pumps OR MonacoPumpGroup OR kucoin_pump_group OR WSB_CryptoPumpSignal
# OR kucoinpumpswsb

COIN_AMOUNT = '10000000'  # coin amount to buy. Set this a high value to buy all of your current USDT
COIN_PAIRING = 'USDT'  # type of pairing used for listing. either USDT or BTC

# NON-ESSENTIAL
TARGET_SELL_PERCENTAGE = 100


def tel_main(sell_target=False):
    proc = multiprocessing.Process(target=awaiting_message)
    proc.start()

    @tel_client.on(events.NewMessage(chats=CHANNEL_NAME))
    async def my_event_handler(event):
        c_name = extract_coin_name(event.raw_text, pairing_type=COIN_PAIRING)
        print('message')
        if not c_name:
            return

        proc.terminate()
        print(f'\r ')

        print(c_name)

        order = kc_client.create_market_order(c_name + f'-{COIN_PAIRING}', Client.SIDE_BUY, size=COIN_AMOUNT)
        entry_price = kc_client.get_fiat_prices(symbol=c_name)[c_name]  # or take from bid?
        print(f"{order} --- {entry_price}")

        Thread(target=profit_tracker, args=[c_name, float(entry_price)]).start()

        keyboard_sell(coin_name=c_name,
                      order_id=order['orderId'],
                      pairing_type=COIN_PAIRING)  # enable keypress sell option. "pg up" for market and "pg down" for lim

        if sell_target:
            ord_bk_fa = kc_client.get_order_book(c_name + f'-{COIN_PAIRING}')['bids'][0]  # order book first order
            num_decimals_price = ord_bk_fa[0][::-1].find('.')
            num_decimals_amount = ord_bk_fa[1][::-1].find('.')
            deal_amount = f'%.{num_decimals_amount}f' % (
                    float(kc_client.get_order(order['orderId'])['dealSize']) * 0.998)
            target_price = f'%.{num_decimals_price}f' % (float(entry_price) * ((TARGET_SELL_PERCENTAGE / 100) + 1))
            # the '%.2f' % is to limit decimals!
            sell_on_target(coin_name=c_name, target_price=target_price, coin_amount=deal_amount, time_to_check=0.8,
                           pairing_type=COIN_PAIRING)

    tel_client.start()
    tel_client.run_until_disconnected()


if __name__ == "__main__":
    print_bot_name()
    tel_main(sell_target=False)
