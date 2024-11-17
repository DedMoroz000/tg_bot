import random
import telebot
from telebot.types import Message
import os

bot = telebot.TeleBot('7354187699:AAFjphXqBSUoon8zg6nwVMbod_o2d8Bb7kE')

bot.answer_cache = {}

@bot.message_handler(commands=['start'])
def cmd_start(message):
    bot.reply_to(message, 'Привет! Я бот. Команда /help покажет все команды.')

@bot.message_handler(commands=['author'])
def cmd_author(message):
    bot.reply_to(message, 'Автор: Dima')

@bot.message_handler(commands=['coins'])
def cmd_coins(message: Message):
    x = random.randint(1, 2)
    if x == 1:
        bot.reply_to(message, 'выпал орёл')
    else:
        bot.reply_to(message, 'выпала решка')

@bot.message_handler(commands=['password'])
def cmd_password(message: Message):
    vowels = 'euyioaEYUIOA'
    consonants = 'qwrtpsdfghjklzxcvbnmQWRTPSDFGHJKLZXCVBNM'
    numbers = '1234567890'
    symbols = "№+=-!*/@"
    password = ''

    for i in range(3):
        password += random.choice(consonants)
        password += random.choice(vowels)

    for i in range(2):
        password += random.choice(numbers)

    for i in range(2):
        password += random.choice(symbols)

    bot.reply_to(message, 'Сгенерированный пароль:')
    bot.reply_to(message, password)

@bot.message_handler(commands=['help'])
def cmd_help(message: Message):
    bot.reply_to(message, 'Есть команды: /author, /coins, /password, /sulifa, /name, /riddle, /quote, /fact, /task, /mem, /read, /pvzMem.')

@bot.message_handler(commands=['name'])
def cmd_name(message: Message):
    bot.reply_to(message, 'Как вас зовут?')
    bot.register_next_step_handler(message, get_name)

def get_name(message: Message):
    name = message.text
    bot.reply_to(message, 'Ваше имя: ' + name)

@bot.message_handler(commands=['sulifa'])
def cmd_sulifa(message: Message):
    bot.reply_to(message, 'Что вы поставите?')
    bot.register_next_step_handler(message, get_sulifa)

def get_sulifa(message):
    player = message.text
    comp = random.choice(['камень', 'ножницы', 'бумага'])
    if player == comp:
        bot.reply_to(message, 'Ничья!')
    elif player == 'камень' and comp == 'ножницы':
        bot.reply_to(message, 'Вы победили!')
    elif player == 'ножницы' and comp == 'бумага':
        bot.reply_to(message, 'Вы победили!')
    elif player == 'бумага' and comp == 'камень':
        bot.reply_to(message, 'Вы победили!')
    else:
        bot.reply_to(message, 'Вы проиграли!')

@bot.message_handler(commands=['riddle'])
def cmd_riddle(message: Message):
    riddles = [
        {"question": "Что имеет ключи, но не может открыть замок?", "answer": "пианино"},
        {"question": "У чего есть голова, хвост, но нет ног и оно коричневое?", "answer": "монета"},
        {"question": "Я говорю безо рта и слышу без ушей. У меня нет тела, но я оживаю на ветру. Кто я?", "answer": "эхо"},
    ]

    riddle = random.choice(riddles)
    question = riddle["question"]
    answer = riddle["answer"]

    bot.send_message(message, f"Вот тебе загадка:\n\n{question}\n\nОтветь на неё!")
    
    bot.answer_cache[message] = answer

@bot.message_handler(func=lambda message: message in bot.answer_cache)
def check_riddle_answer(message: Message):
    correct_answer = bot.answer_cache.get(message).lower()
    user_answer = message.text.lower()

    if user_answer == correct_answer:
        bot.send_message(message, "Верно! 🎉 Молодец!")
    else:
        bot.send_message(message, "Неправильно. Попробуй ещё раз или напиши '/riddle' для новой загадки!")

@bot.message_handler(commands=['quote'])
def cmd_quote(message: Message):
    quotes = [
        "Никогда не поздно стать тем, кем мог бы быть. – Джордж Элиот",
        "Верьте, что можете, и вы уже на полпути. – Теодор Рузвельт",
        "Ваше время ограничено, не тратьте его, живя чужой жизнью. – Стив Джобс",
        "Только те, кто рискует идти слишком далеко, могут узнать, как далеко можно зайти. – Т. С. Элиот",
        "Каждый человек — архитектор своего счастья. – Аристотель",
        "Жизнь — это 10% того, что с вами происходит, и 90% того, как вы на это реагируете. – Чарльз Суиндолл",
        "Не важно, как медленно ты идешь, до тех пор, пока ты не остановишься. – Конфуций",
        "Будь тем изменением, которое хочешь видеть в мире. – Махатма Ганди",
        "Лучший способ предсказать будущее — это создать его. – Питер Друкер",
        "Успех — это не ключ к счастью. Счастье — это ключ к успеху. Если вы любите то, что делаете, вы будете успешны. – Альберт Швейцер"
    ]

    # Выбираем случайную цитату
    quote = random.choice(quotes)

    # Отправляем цитату пользователю
    bot.reply_to(message, f"Вот вдохновляющая цитата для тебя:\n\n{quote}")

@bot.message_handler(commands=['fact'])
def cmd_fact(message: Message):
    facts = [
        "Муравьи никогда не спят.",
        "Осьминоги имеют три сердца.",
        "Самый большой айсберг был больше Ямайки.",
        "Пчелы могут различать человеческие лица.",
        "Каждую секунду в мире рождается около 4 детей."
    ]

    fact = random.choice(facts)
    bot.reply_to(message, fact)

@bot.message_handler(commands=['task'])
def cmd_task(message: Message):
    bot.reply_to(message, 'Какую задачу вы хотите добавить?')
    bot.register_next_step_handler(message, add_task)

def add_task(message: Message):
    task = message.text
    with open('task.txt', 'a', encoding='utf-8') as file:
        file.write(task + '\n')
        bot.reply_to(message, 'Ваша задача успешно добавлена')

@bot.message_handler(commands=['read'])
def cmd_read(message: Message):
    with open('task.txt', 'r', encoding='utf-8') as file:
        text = file.read()
        bot.reply_to(message, text)

@bot.message_handler(commands=['mem'])
def cmd_mem(message: Message):
    mems = os.listdir('images')
    mem = random.choice(mems)
    mem = 'images/' + mem
    with open(mem, 'rb') as file:
        bot.send_photo(message.chat.id, file)

@bot.message_handler(commands=['pvzMem'])
def cmd_pvzMem(message: Message):
    pvzmems = os.listdir('pvzmems')
    pvzmem = random.choice(pvzmems)
    pvzmem = 'pvzmems/' + pvzmem
    with open(pvzmem, 'rb') as file:
        bot.send_photo(message.chat.id, file)

bot.polling()
