import telebot
from Config_file import TOKEN, currency
from Extensions import Converter, APIException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def command_start(message: telebot.types.Message):
    bot.send_message(message.chat.id, f'Привет,\t {message.chat.first_name}!')
    bot.send_message(message.chat.id, 'Я помогу Вам конвертировать валюту!'
                                      ' Воспользуйтесь подсказками по команде /help')


@bot.message_handler(commands=['help'])
def command_help(message: telebot.types.Message):
    text = 'Для начала работы введите текст в следующем формате (через пробел):\n' \
           '<Валюта, которую хотите обменять>\n <Валюта, которую хотите купить>\n' \
           '<Количество валюты>\n' \
           'Чтобы посмотреть список доступных валют, введите: /values'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def command_values(message: telebot.types.Message):
    text = 'Могу конвертировать следующие валюты:'
    for key in currency.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def data_enter(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) > 3:
            raise APIException('Вы ввели слишком много данных!\n'
                               'Введите только 3 параметра в следующем формате (через пробел):\n'
                               '<Валюта, которую хотите обменять>\n<Валюта, которую хотите купить>\n'
                               '<Количество валюты>\n')

        elif len(values) < 3:
            raise APIException('Вы что-то забыли указать! Повторите, пожалуйста, ввод.')
        base_cur, quote_cur, amount = values
        base_cur = base_cur.lower()
        quote_cur = quote_cur.lower()
        rate = Converter.get_price(base_cur, quote_cur, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Ошибка!\n Не удалось обработать команду \n{e}')
    else:
        quantity_rated = rate * int(amount)
        text = f'Сумма {amount} {base_cur} равна {quantity_rated:.2f} {quote_cur}'
        bot.send_message(message.chat.id, text)


bot.polling()
