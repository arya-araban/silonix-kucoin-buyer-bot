import re
from typing import Optional

def extract_coin_name(text: str, pairing_type: str = 'USDT') -> Optional[str]:
    """Extract coin name from trading link or text."""
    if text.strip().isalpha() and ' ' not in text:
        return text

    start = '/trade'
    end = f'-{pairing_type}'
    
    try:
        parts = text.partition(start)[2].partition(end)[0].partition("/")
        return parts[2].partition(end)[0]
    except:
        return None