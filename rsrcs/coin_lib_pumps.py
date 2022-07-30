import json
import threading
import time

import requests
from pynput import keyboard
from requests_futures.sessions import FuturesSession
from sty import fg

from config import kc_client
from kucoin.client import Client

from pynput.keyboard import Listener, KeyCode

from rsrcs.useful_funcs import extract_coin_name, round_down


def extract_discord_coin_name(channel_id, headers):
    """This function is the main code used for discord scraping. it scraps the last message of the channel with id of
     {channel_id} each few milliseconds, and checks weather there is a coin name found for pumping or not,
     so essentially, as soon as pump message is sent out, we get the coin name - USED FOR PUMPS """
    session = FuturesSession()
    while True:

        future = session.get(f'https://discord.com/api/v9/channels/{channel_id}/messages?limit=1',
                             headers=headers)
        # print(future)

        try:
            last_msg = json.loads(future.result().text)[0]['content']
            c_name = extract_coin_name(last_msg, "USDT")
            # print(last_msg)
            if c_name:  # if c_name isn't ''
                # print(c_name)
                return c_name
        except Exception as err:
            print(f"{err.__class__} -- {err}")
            continue



