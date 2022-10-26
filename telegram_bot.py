import telebot
from random import randint
import requests
from bs4 import BeautifulSoup
import string

all_words = requests.get(
    'https://raw.githubusercontent.com/Harrix/Russian-Nouns/main/dist/russian_nouns.txt').text.split('\n')
cities_resp = requests.get('https://xn----7sbiew6aadnema7p.xn--p1ai/alphabet.php').text
animals = requests.get(
    'https://gist.githubusercontent.com/oboshto/a0bf911b03068d43e41cf17da2331b0d/raw'
    '/551341af5287afc80ab5200cc26105ebe3e4a396/%25D0%25B6%25D0%25B8%25D0%25B2%25D0%25BE%25D1%2582%25D0%25BD%25D1%258B'
    '%25D0%25B5.txt').text.split('\n')
cities = []
for elem in BeautifulSoup(cities_resp, 'lxml')('li'):
    if elem.find('a') is not None:
        city_county = ''.join(str(elem)[i] for i in range(len(str(elem)))
                              if all([str(elem)[i] not in string.ascii_letters,
                                      str(elem)[i] not in ')<>="/_.?0123456789']))
        city_county = city_county.split('(')
        city = city_county[0].replace(' ', '', 1)
        cities.append(city[:len(city) - city.count(' ')])
used_words = []
words = []
reply: str
cities_flag = False


def remake(el: str):
    el = el.replace('ё', 'е')
    el = el.replace('Ё', 'Е')
    return el


API_TOKEN = '5520553389:AAHRq_GacwKRcOabjw0Fc0JiYRpTP9ixSkM'
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def welcomes(message):
    bot.reply_to(message, 'Привет! Я бот для игры в слова, помогу тебе нескучно и полезно провести время!\n'
                          '\n'
                          'Подробная информация - /help')
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton('Начать новую игру'))
    bot.send_message(message.chat.id, 'Чтобы начать игру, нажми на кнопку ниже\n'
                                      'P.S перед началом игры советую прочитать правила\n'
                                      '/rules', reply_markup=markup)


@bot.message_handler(commands=['help'])
def helping(message):
    bot.reply_to(message,
                 'С этим ботом ты сможешь поиграть в слова. Перед началом игры ты можешь решить, будешь ты играть в '
                 'слова, связанные с одной тематикой (например, города) или будешь использовать все слова русского '
                 'языка в игре, а так же ты можешь выбрать, кто начнёт игру, ты или бот. Если во время игры ты зайдёшь '
                 'в тупик и не сможешь придумать новое слово, то ты всегда можешь остановить игру и начать играть '
                 'сначала\n'
                 '\n'
                 '/start - тут ты можешь запустить бот по новой\n'
                 '/rules - тут ты можешь прочитать правила\n'
                 '/feedback - тут ты можешь оставить свой отзыв о боте')


@bot.message_handler(commands=['feedback'])
def feedback(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('тык', url='https://forms.gle/xw1xXbQqHGRo27Ka6'))
    bot.send_message(message.chat.id,
                     'Если у тебя есть какие-то идеи для улучшения бота (например, добавление новых тем в игру), '
                     'пожелания, жалобы, вопросы и т. д., то ты всегда можешь написать их в эту форму',
                     reply_markup=markup)


@bot.message_handler(commands=['rules'])
def game_rules(message):
    bot.reply_to(message,
                 'Правила игры \n'
                 '\n'
                 '1. Участник каждый раз подбирает понятие на последнюю букву названного перед ним слова. '
                 'Однако, следуя правилам русского языка, в игре предусмотрены исключения. '
                 'Если слово заканчивается на Ь, Ъ, Ы, Й, то сочиняют на предпоследнюю букву.\n'
                 '2. Наименования не должны повторяться – каждый раз придумывается новое.\n')


@bot.message_handler(content_types=['text'])
def game(message):
    global words
    global used_words
    global cities_flag
    global reply
    if message.text == 'Начать новую игру':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(telebot.types.KeyboardButton('Выбрать тематику'),
                   telebot.types.KeyboardButton('Не выбирать'))
        bot.send_message(message.chat.id, 'Будешь выбирать тематику игры?', reply_markup=markup)
    elif message.text == 'Выбрать тематику':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(telebot.types.KeyboardButton('Животные'), telebot.types.KeyboardButton('Города России'))
        bot.send_message(message.chat.id, 'Выбери тематику', reply_markup=markup)
    elif message.text == 'Не выбирать':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(telebot.types.KeyboardButton('Я'), telebot.types.KeyboardButton('Бот'))
        bot.send_message(message.chat.id, 'Кто начнёт игру?', reply_markup=markup)
        words = all_words
    elif message.text == 'Животные':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(telebot.types.KeyboardButton('Я'), telebot.types.KeyboardButton('Бот'))
        bot.send_message(message.chat.id, 'Кто начнёт игру?', reply_markup=markup)
        words = animals
    elif message.text == 'Города России':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(telebot.types.KeyboardButton('Я'), telebot.types.KeyboardButton('Бот'))
        bot.send_message(message.chat.id, 'Кто начнёт игру?', reply_markup=markup)
        words = cities
        cities_flag = True
    elif message.text == 'Остановить игру' or message.text == 'Начать сначала':
        words = []
        used_words = []
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(telebot.types.KeyboardButton('Начать новую игру'))
        bot.send_message(message.chat.id, 'Чтобы начать новую игру нажми на кнопку ниже', reply_markup=markup)
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
                                              f'Твой ход, тебе на букву "{reply[-2].upper()}"', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, f'{reply}\n'
                                              f'Твой ход, тебе на букву "{reply[-1].upper()}"', reply_markup=markup)
    else:
        words = [remake(word) for word in words]
        if len(words) == 0:
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(telebot.types.KeyboardButton('Начать сначала'))
            bot.send_message(message.chat.id, 'Я больше не знаю слов на эту тему :(', reply_markup=markup)
        if cities_flag:
            word = remake(message.text[0].upper() + message.text[1:])
            if word in used_words:
                bot.reply_to(message, 'Это слово уже было использовано в игре, придумай другое слово')
            elif word not in words and word not in used_words:
                bot.reply_to(message, 'Я не знаю такого слова, придумай, пожалуйста, новое\n'
                                      'Возможно город, который ты назвал, не является русским')
            else:
                words.remove(word)
                used_words.append(word)
                if message.text[-1] in 'ЬЪЫЙъьый':
                    for i in range(len(words)):
                        if words[i][0] == word[-2].upper():
                            reply = words[i]
                            break
                else:
                    for i in range(len(words)):
                        if words[i][0] == word[-1].upper():
                            reply = words[i]
                            break
        else:
            word = remake(message.text.lower())
            if word in used_words:
                bot.reply_to(message, 'Это слово уже было использовано в игре, придумай другое слово')
            elif word not in words and word not in used_words:
                bot.reply_to(message, 'Я не знаю такого слова, придумай, пожалуйста, новое')
            else:
                words.remove(word)
                used_words.append(word)
                if message.text[-1] in 'ЬЪЫЙъьый':
                    for i in range(len(words)):
                        if words[i][0] == word[-2].lower():
                            reply = words[i]
                            break
                else:
                    for i in range(len(words)):
                        if words[i][0] == word[-1].lower():
                            reply = words[i]
                            break
        words.remove(reply)
        used_words.append(reply)
        if reply[-1] in 'ЬЪЫЙъьый':
            bot.reply_to(message, f'{reply}\n'
                                  f'Твой ход, тебе на букву "{reply[-2].upper()}"')
        else:
            bot.reply_to(message, f'{reply}\n'
                                  f'Твой ход, тебе на букву "{reply[-1].upper()}"')


bot.infinity_polling()
