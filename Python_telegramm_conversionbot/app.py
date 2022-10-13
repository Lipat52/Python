import telebot
from telebot import types
from config import keys, TOKEN
from extensions import ConvertException, Convert


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Привет!\nЧто бы начать работу, введите команду боту в следующем формате: \n<Имя валюты> \
<В какую валюту перевести> <Колличество переводимой валюты> \nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


def build_menu(buttons, n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    # text = 'Доступные валюты:'
    # for key in keys.keys():
    #     text = '\n'.join((text, key, ))
    # bot.reply_to(message, text)

 # Попробовал добавить кнопки, но не осилил обработчик
    reply_markup = types.InlineKeyboardMarkup()

    for v in keys.keys():
        reply_markup.add(types.InlineKeyboardButton(text=v, callback_data=v))
        # reply_markup.add(reply)

    bot.send_message(message.chat.id, 'Доступные валюты: '.format(message.from_user), reply_markup=reply_markup)
    bot.send_message(message.chat.id, 'Выберете валюту, цену на которую надо узнать')


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    global quote
    if not keys.get(call.message.from_user.id):
        keys[call.message.from_user.id] = 1
    else:
        keys[call.message.from_user.id] += 1
    if keys[call.message.from_user.id] == 1:
        bot.send_message(call.message.chat.id, call.data)
        bot.send_message(call.message.chat.id, 'Выберете валюту, цену в которой надо узнать')
        quote = call.data
    if keys[call.message.from_user.id] == 2:
        bot.send_message(call.message.chat.id, call.data)
        base = call.data
        if base == call.data:
            # bot.send_message(call.message.chat.id, quote)
            # bot.send_message(call.message.chat.id, base)
            data = Convert.get_price_for_button(quote, base)
            text = f'Цена {quote} в {base} {data}'
            bot.send_message(call.message.chat.id, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')

    try:
        if len(values) != 3:
            raise ConvertException('введите команду боту в следующем формате: \n<Имя валюты> \
<В какую валюту перевести> \
<Колличество переводимой валюты>')
        quote, base, amount = values
        data = Convert.get_price(quote, base, amount)
    except ConvertException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} {data}'
        bot.send_message(message.chat.id, text)


bot.polling()
