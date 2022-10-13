import requests
import json
from config import keys


class ConvertException(Exception):
    pass


class Convert:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        try:
            quote_tiker = keys[quote]
        except KeyError:
            raise ConvertException(f'Неудалось обработать валюту {quote}')
        try:
            base_tiker = keys[base]
        except KeyError:
            raise ConvertException(f'Неудалось обработать валюту {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertException(f'Неудалось обработать количество {amount}')
        if amount <= 0:
            raise ConvertException(f'Неудалось обработать количество {amount}')
        if quote == base:
            raise ConvertException(f'Невозможно перевести одинаковые валюты {base}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_tiker}&tsyms={base_tiker}')
        data = (json.loads(r.content)[keys[base]]) * float(amount)

        return data

    @staticmethod
    def get_price_for_button(quote: str, base: str):

        quote, base = keys[quote], keys[base]
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote}&tsyms={base}')
        data = (json.loads(r.content)[base])

        return data
