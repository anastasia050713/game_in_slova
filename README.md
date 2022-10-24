import telebot
from random import randint

API_TOKEN = '5717442815:AAEBziWv-5QoBQHKm2nMCn7z-SlMvytVNrM'
bot = telebot.TeleBot(API_TOKEN)

with open('russian_nouns.txt') as f:
    all_words = [row.strip() for row in f]
with open('animals.txt') as f:
    animals = [row.strip() for row in f]
with open('Список городов России') as f:
    cities = [row.strip() for row in f]
used_words = []
words = []


@bot.message_handler(commands=['start'])
def welcomes(message):
    bot.reply_to(message, 'Привет! Я бот для игры в слова, помогу тебе нескучно и полезно провести время!')
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton('Начать игру'))
    markup.add(telebot.types.KeyboardButton('Правила игры'))
    bot.send_message(message.chat.id, 'Чтобы начать игру или прочитать правила к ней, '
                                      'нажми на соответствующую кнопку ниже', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def game(message):
    global words
    global used_words
    if message.text == 'Правила игры':
        bot.reply_to(message, '''\
        Правила игры
    1. Участник каждый раз подбирает понятие на последнюю букву названного перед ним слова. Однако, следуя правилам 
    русского языка, в игре предусмотрены исключения. Если слово заканчивается на Ь, Ъ, Ы, то сочиняют на предпоследнюю 
    букву.
    2. Наименования не должны повторяться – каждый раз придумывается новое.
    P.S Не используй, пожалуйста, букву Ё, я ее "не знаю"  :) 
    P.P.S И вводи, пожалуйста, слова с маленькой буквы, я умею играть ''')
    elif message.text == 'Начать игру':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(telebot.types.KeyboardButton('Животные'))
        markup.add(telebot.types.KeyboardButton('Города'))
        markup.add(telebot.types.KeyboardButton('Без темы'))
        bot.send_message(message.chat.id, 'Выбери тему игры', reply_markup=markup)
    elif message.text == 'Животные':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(telebot.types.KeyboardButton('Я'))
        markup.add(telebot.types.KeyboardButton('Бот'))
        words = animals
        bot.send_message(message.chat.id, 'Кто начнёт игру?', reply_markup=markup)
    elif message.text == 'Города':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(telebot.types.KeyboardButton('Я'))
        markup.add(telebot.types.KeyboardButton('Бот'))
        words = cities
        bot.send_message(message.chat.id, 'Кто начнёт игру?', reply_markup=markup)
    elif message.text == 'Без темы':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(telebot.types.KeyboardButton('Я'))
        markup.add(telebot.types.KeyboardButton('Бот'))
        bot.send_message(message.chat.id, 'Кто начнёт игру?', reply_markup=markup)
        words = all_words
    elif message.text == 'Я':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(telebot.types.KeyboardButton('Остановить игру'))
        bot.send_message(message.chat.id, 'Твой ход! Введи любое слово', reply_markup=markup)
    elif message.text == 'Бот':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(telebot.types.KeyboardButton('Остановить игру'))
        reply = words[randint(0, len(words))]
        words.remove(reply)
        used_words.append(reply)
        if reply[-1] in 'ЬЪЫЙъьый':
            bot.send_message(message.chat.id, f'{reply}\n'
                                              f'Твой ход, тебе на букву "{reply[-2]}"', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, f'{reply}\n'
                                              f'Твой ход, тебе на букву "{reply[-1]}"', reply_markup=markup)
    elif message.text == 'Остановить игру':
        words = []
        used_words = []
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(telebot.types.KeyboardButton('Начать игру'))
        markup.add(telebot.types.KeyboardButton('Правила игры'))
        bot.send_message(message.chat.id, 'Чтобы начать новую игру или прочитать правила к ней, '
                                          'нажми на соответствующую кнопку ниже', reply_markup=markup)
    else:
        if len(words) == 0:
            bot.send_message(message.chat.id, 'Я больше не знаю слов на эту тему :('
                                              'Чтобы начать заново, останови игру')
        reply = ''
        if all([message.text not in words, message.text not in used_words]):
            bot.reply_to(message, 'Я не знаю такого слова, придумай, пожалуйста, новое')
        if message.text in used_words:
            bot.reply_to(message, '''Это слово уже было использовано в игре, придумай другое слово''')
        else:
            words.remove(message.text)
            used_words.append(message.text)
            if message.text[-1] in 'ЬЪЫЙъьый':
                for i in range(len(words)):
                    if words[i][0] == message.text[-2]:
                        reply = words[i]
                        break
            else:
                for i in range(len(words)):
                    if words[i][0] == message.text[-1]:
                        reply = words[i]
                        break
            words.remove(reply)
            used_words.append(reply)
            if reply[-1] in 'ЬЪЫЙъьый':
                bot.reply_to(message, f'{reply}\n'
                                      f'Твой ход, тебе на букву "{reply[-2]}"')
            else:
                bot.reply_to(message, f'{reply}\n'
                                      f'Твой ход, тебе на букву "{reply[-1]}"')


bot.infinity_polling()
