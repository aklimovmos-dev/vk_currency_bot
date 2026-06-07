import json
import requests


class APIException(Exception):
    pass


class CurrencyConverter:
    currencies = {
        "евро": "EUR",
        "доллар": "USD",
        "рубль": "RUB"
    }

    @staticmethod
    def get_price(base, quote, amount):
        base = base.lower().strip()
        quote = quote.lower().strip()
        amount = str(amount).strip().replace(",", ".")

        if base == quote:
            raise APIException("Нельзя переводить одинаковые валюты.")

        try:
            base_ticker = CurrencyConverter.currencies[base]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту: {base}")

        try:
            quote_ticker = CurrencyConverter.currencies[quote]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту: {quote}")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество: {amount}")

        if amount <= 0:
            raise APIException("Количество должно быть больше нуля.")

        try:
            url = f"https://open.er-api.com/v6/latest/{base_ticker}"
            response = requests.get(url, timeout=10)

            if response.status_code != 200:
                raise APIException("Сервис курсов валют временно недоступен.")

            data = json.loads(response.text)

            if "rates" not in data:
                raise APIException("Некорректный ответ от сервиса валют.")

            if quote_ticker not in data["rates"]:
                raise APIException(f"Не найден курс для валюты: {quote}")

            rate = data["rates"][quote_ticker]
            total = rate * amount

            return round(total, 4)

        except requests.exceptions.RequestException:
            raise APIException("Ошибка подключения к сервису курсов валют.")
        except json.JSONDecodeError:
            raise APIException("Ошибка обработки ответа от сервиса валют.")