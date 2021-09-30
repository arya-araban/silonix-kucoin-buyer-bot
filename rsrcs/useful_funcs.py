# USED FOR PUMPS, extract coin name from the message sent in telegram channel
def extract_coin_name(txt):
    start = '.com/'
    end = '-USDT'
    coin_name = txt[txt.find(start) + len(start):txt.rfind(end)]
    return coin_name
