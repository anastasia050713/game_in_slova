# @game_in_slova_bot
Этот бот играет с пользователем в слова (то есть пользователь и бот поочередно отправляют слово, начинающееся на последнюю букву слова предыдущего игрока)
____
## функции
Бот содержит в себе 5 функций

### start
Стандартная команда для активации бота. После её запуска в чат отправляется приветствие и появляется клавиатура с кнопкой "Начать новую игру"

### help
Команда, при использовании которой отправляется краткое описание принципа игры в слова и работы самого бота, а так же описание других команд:
- /start
- /rules
- /feedback

### rules
Команда, которая отправляет в чат правила игры
#### feedback
Команда, которое отправляет в чат сообщение с прикрепленной к нему ссылкой на Google форму для обратной связи

### game
Функция, принимающая сообщения пользователя и отвечающая за процесс игры. При нажатии кнопки "Начать новую игру", по очереди выводит кнопки, которые дают изменить условия игры
Примерно так выглядит очередность нажатия кнопок:

- **"Начать новую игру"** \n
    В чате появляется вопрос "Будешь выбирать тематику игры?" и 2 кнопки для выбора настроек
    - **"Выбирать тематику"**
    В чате появлятеся сообщение "Выбери тематику" и 2 кнопки для выбора тематики
        - **"Города России"**
        Теперь в игре бот будет использовать слова только из списка cities (список со всеми городами РФ)
        В чате появляется вопрос "Кто начнет игру?" и 2 кнопки для выбора игрока
            - **"Я"**
            В чате появляется сообщение "Твой ход! Введи любое слово" и бот ждет, когда вы отправите первое слово на заданную тему для начала игры
            На клавиатуре появляется кнопка для остановки игры, в случае, если пользователь зайдёт в тупик во время игры или ему просто надоест игра
                - **"Остановить игру"**
                    При нажатии этой кнопки бот возвращается в начало "цикла" из кнопок, и пользователь может начать играть заново
                    Возможен вариант кнопки с таким же функционалом с названием "Начать сначала", она появляется, когда у бота заканчиваются слова в выбранном списке и он больше не может продолжать игру
                    - **"Начать новую игру"** 
            - **"Бот"**
            Бот отправляет пользователю рандомное слово из выбранного списка и сообщение "Твой ход, тебе на букву "последняя буква слова, отправленного ботом"
                - **"Остановить игру"**
                    - **"Начать новую игру"**    
        - **"Животные"**
        Теперь в игре бот будет использовать слова только из списка animals (список со всеми(почти) животными)
        В чате появляется вопрос "Кто начнет игру?" и 2 кнопки для выбора игрока
            - **"Я"**
                - **"Остановить игру"**
                    - **"Начать новую игру"** 
            - **"Бот"**
                - **"Остановить игру"**
                    - **"Начать новую игру"**  
    - **"Не выбирать"** 
    При нажатии этой кнопки пропускается этап выбора тематики игры и бот в качестве списка слов по умолчанию использует список all_words (список со всеми словами русского языка)
    В чате появляется вопрос "Кто начнет игру?" и 2 кнопки для выбора игрока
        - **"Я"**
            - **"Остановить игру"**
                - **"Начать новую игру"** 
        - **"Бот"**
            - **"Остановить игру"**
                - **"Начать новую игру"** 

После настройки игры, бот и пользователь поочередно отправляют друг другу слова в соответсвии с правилами игры и настройками. Бот обрабатывает слова пользователя при помощи условий и циклов, которые находятся в условии "else:" функции game. При нажатии кнопки "Остановить игру" или "Начать сначала" весь процесс запускается по новой. 
