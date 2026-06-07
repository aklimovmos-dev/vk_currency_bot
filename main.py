import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.exceptions import ApiError

from config import TOKEN
from extensions import APIException, CurrencyConverter

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

currencies = {
    "евро": "EUR",
    "доллар": "USD",
    "рубль": "RUB"
}


def send_message(user_id, text):
    try:
        vk.messages.send(
            user_id=user_id,
            message=text,
            random_id=random.randint(1, 2_147_483_647)
        )
    except ApiError as e:
        print(f"Ошибка отправки сообщения пользователю {user_id}: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка при отправке сообщения: {e}")


def get_values_text():
    values_text = "Доступные валюты:\n"
    for currency in currencies:
        values_text += f"- {currency}\n"
    return values_text


print("Бот работает...")

try:
    for event in longpoll.listen():
        try:
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                text = event.text.lower().strip()
                user_id = event.user_id

                if text in ["/start", "/help"]:
                    send_message(
                        user_id,
                        "Чтобы начать работу, введите команду в формате:\n"
                        "<имя валюты> <в какую валюту перевести> <количество>\n\n"
                        "Пример:\n"
                        "евро доллар 100\n\n"
                        "Доступные команды:\n"
                        "/start или /help — инструкция\n"
                        "/values — список доступных валют"
                    )

                elif text == "/values":
                    send_message(user_id, get_values_text())

                else:
                    values = text.split()

                    if len(values) != 3:
                        raise APIException(
                            "Неверное количество параметров.\n"
                            "Используйте формат:\n"
                            "<валюта> <в какую валюту> <количество>"
                        )

                    base, quote, amount = values
                    total = CurrencyConverter.get_price(base, quote, amount)

                    send_message(
                        user_id,
                        f"{amount} {base} = {total} {quote}"
                    )

        except APIException as e:
            send_message(event.user_id, f"Ошибка пользователя:\n{e}")

        except Exception as e:
            try:
                send_message(event.user_id, f"Не удалось обработать команду:\n{e}")
            except Exception:
                pass
            print(f"Ошибка обработки события: {e}")

except KeyboardInterrupt:
    print("Бот остановлен вручную.")
except Exception as e:
    print(f"Критическая ошибка бота: {e}")