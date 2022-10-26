import telebot
from random import randint

API_TOKEN = '5717442815:AAEBziWv-5QoBQHKm2nMCn7z-SlMvytVNrM'
bot = telebot.TeleBot(API_TOKEN)

with open('singular.txt') as f:
    all_words = [row.strip() for row in f]
used_words = []


# Handle '/start'
@bot.message_handler(commands=['start'])
def welcomes(message):
    bot.reply_to(message, 'Привет! Я бот для игры в слова, помогу тебе нескучно и полезно провести время!')
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton('Начать игру'))
    markup.add(telebot.types.KeyboardButton('Правила игры'))
    bot.send_message(message.chat.id, 'Чтобы начать игру или прочитать правила к ней,\
    нажми на соответствующую кнопку ниже', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def game_process(message):
    if message.text == 'Правила игры':
        bot.reply_to(message, '''\
        Правила игры
1. Медлить с ответом нельзя. Если отвечающий раздумывает больше 30 секунд, то он выбывает.
2. Участник каждый раз подбирает понятие на последнюю букву названного перед ним слова. Однако, следуя правилам русского
языка, в игре предусмотрены исключения. Если слово заканчивается на Ь, Ъ, Ы, Й, то сочиняют на предпоследнюю букву.
3. Наименования не должны повторяться – каждый раз придумывается новое.''')
    elif message.text == 'Начать игру':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(telebot.types.KeyboardButton('Я'))
        markup.add(telebot.types.KeyboardButton('Бот'))
        bot.send_message(message.chat.id, 'Кто начнёт игру?', reply_markup=markup)
    elif message.text == 'Я':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(telebot.types.KeyboardButton('Остановить игру'))
        bot.send_message(message.chat.id, 'Твой ход! Введи любое слово')
    elif message.text == 'Бот':
        reply = 'ЬЪЫЙъьый'
        while reply[-1] not in 'ЬЪЫЙъьый':
            reply = all_words[randint(0, len(all_words))]
        all_words.remove(reply)
        used_words.append(reply)
        bot.send_message(message.chat.id, f'{reply}\n'
                                          f'Твой ход, тебе на букву "{reply[-1]}"')
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(telebot.types.KeyboardButton('Остановить игру'))


@bot.message_handler(content_types=['text'])
def game_process_2(message):
    reply = ''
    if message.text in used_words:
        bot.reply_to(message, '''Это слово уже было использовано в игре, придумай другое слово''')
    else:
        all_words.remove(message)
        if message.text[-1] in 'ЬЪЫЙъьый':
            for i in range(len(all_words)):
                if all([all_words[i][0] == message[-2], all_words[i] not in used_words]):
                    reply = all_words[i]
                    break
        else:
            for i in range(len(all_words)):
                if all([all_words[i][0] == message[-1], all_words[i] not in used_words]):
                    reply = all_words[i]
                    break
        used_words.append(message)
        used_words.append(reply)
        if reply[-1] in 'ЬЪЫЙъьый':
            bot.reply_to(message, f'{reply}'
                                  f'Твой ход, тебе на букву "{reply[-2]}"')
        else:
            bot.reply_to(message, f'{reply}'
                                  f'Твой ход, тебе на букву "{reply[-1]}"')
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton('Остановить игру'))


@bot.message_handler(content_types=['text'])
def stop_bot(message):
    if message.text == 'Остановить игру':
        bot.stop_bot()
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton('Начать новую игру'))


bot.infinity_polling()
