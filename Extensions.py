import requests
import json
from Config_file import currency


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base_cur=str, quote_cur=str, amount=int):
        if base_cur == quote_cur:
            raise APIException(f'Конвертация {base_cur} в {quote_cur} невозможна.')
        try:
            base_cur == currency[base_cur]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base_cur}!\n'
                               'Доступная для конвертации валюта указана в списке /values')
        try:
            quote_cur == currency[quote_cur]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote_cur}!\n'
                               'Доступная для конвертации валюта указана в списке /values')
        try:
            amount == int(amount)
        except ValueError:
            raise APIException('Сумму необходимо ввести как целое число!')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={currency[base_cur]}'
                         f'&tsyms={currency[quote_cur]}')
        currency_rate = json.loads(r.content)[currency[quote_cur]]

        return currency_rate
