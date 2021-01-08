import threading
import time
import vk_api
import random, json
import schedule
from vk_api.longpoll import VkLongPoll, VkEventType
from bot_vk import BotVk

def create_and_send_poll_every_day(chat_id, question=BotVk.get_question_for_lomo_training_next_day(BotVk),
                                   answers=BotVk.get_answers_for_simple_training(
                                       BotVk)):  # метод, который вызывается каждый день, так как установлен в планировщике задач
    try:
        poll = create_poll_for_simple_training(question, answers)  # создание опроса
        attachment = 'poll' + str(poll['owner_id']) + '_' + str(poll['id'])  # идентификатор опроса
        send_poll_in_chat(chat_id, get_random_id(), attachment)  # отправка опроса
    except Exception:
        print("Don't working send_poll_every_day")


def send_poll_in_all_chat_every_day():  # метод, который вызывается каждый день, так как установлен в планировщике задач
    # Отсылает в каждый чат один и тот же опрос
    try:
        obj_chats = get_сonversations()
        count = obj_chats['count']
        items = obj_chats['items']
        for i in range(count):
            id = items[i]['conversation']['peer']['id']  # чата
            id = id % BotVk.module_id
            if id > 0:  # берем только чаты, а не диалоги
                create_and_send_poll_every_day(id)
    except Exception:
        print("Don't working send_poll_in_all_chat_every_day")


def send_poll_in_all_different_chat_every_day():  # метод, который вызывается каждый день, так как установлен в планировщике задач
    # Отсылает в каждый чат свой уникальный опрос
    try:
        obj_chats = get_сonversations()
        count = obj_chats['count']
        items = obj_chats['items']
        for i in range(count):
            id = items[i]['conversation']['peer']['id']
            title = items[i]['conversation']['chat_settings']['title']  # название чата
            id = id % BotVk.module_id
            if id > 0:  # берем только чаты, а не диалоги
                if title == BotVk.man_chat:  # название чата
                    create_and_send_poll_every_day(id, )  # сама отправка конкретного опроса
                elif title == BotVk.woman_chat:
                    create_and_send_poll_every_day(id, "Тренировка в новый год")
                # Если хотите добавить , то прописываете elif название часа и метод отправки опроса
    except Exception:
        print("Don't working send_poll_in_all_different_chat_every_day")


def register_poll_in_all_different_chat_every_day():  # метод, который вызывается каждый день, так как установлен в планировщике задач
    # Отсылает в каждый чат свой уникальный опрос
    try:
        obj_chats = get_сonversations()
        count = obj_chats['count']
        items = obj_chats['items']
        for i in range(count):
            id = items[i]['conversation']['peer']['id']
            title = items[i]['conversation']['chat_settings']['title']  # название чата
            id = id % BotVk.module_id
            if id > 0:  # берем только чаты, а не диалоги
                if title == BotVk.chat1:  # название чата
                    schedule.every().day.at(BotVk.time_sending_poll_in_man_chat).do(create_and_send_poll_every_day, id)
                    # регистрируем отправку конкретного сообщения в конкретное время, название опроса  - дефолтное
                elif title == BotVk.chat2:
                    schedule.every().day.at(BotVk.time_sending_poll_in_woman_chat).do(create_and_send_poll_every_day, id, "Hello world")
                    # регистрируем отправку конкретного сообщения в конкретное время
                # Если хотите добавить , то прописываете elif название часа и метод отправки опроса
    except Exception:
        print("Don't working send_poll_in_all_different_chat_every_day")


def get_сonversations():
    return vk.method('messages.getConversations')


def write_msg(user_id, random_id, message):  # отправляет сообщение в какому-то конкретному юзеру
    vk.method('messages.send', {'user_id': user_id, 'random_id': random_id, 'message': message})


def write_msg_chat(chat_id, random_id, message):  # отправляет сообщение в чат
    vk.method('messages.send', {'chat_id': chat_id, 'random_id': random_id, 'message': message})


def send_poll_in_chat(chat_id, random_id, attachment):  # отправляет опрос в чат
    print(chat_id)
    vk.method('messages.send', {'chat_id': chat_id, 'random_id': random_id, 'attachment': attachment})


def create_poll_for_simple_training(quastion, answers):  # создает опрос и возращает его объект
    ans = json.dumps(answers)
    return vk.method('polls.create',
                     {'question': quastion, 'is_multiple': 1,
                      'add_answers': ans, 'background_id': get_random_background()})


def get_random_background():
    r = random.randint(1, 9)
    while (r == 5 or r == 7):
        r = random.randint(1, 9)
    return r

def get_random_id():
    return random.randint(1, 100000)

def run_listen():
    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me and event.text:
                    request = event.text
                    request = request.split()  # разбиваем сообщение на строки
                    if event.from_chat:  # Если написали в чате
                        if request[0].lower() == "#тренировка" or request[0].lower() == "#треня":  #
                            question = BotVk.get_question_for_simple_training(request)  # получение заголовка к опросу
                            answers = BotVk.get_answers_for_simple_training(
                                BotVk)  # получение ответов к опросу
                            create_and_send_poll_every_day(event.chat_id, question, answers)
                        elif request[0].lower() == "#треняломострела" or request[0].lower() == "#тренястрелаломо":
                            question = BotVk.get_question_for_lomo_training_next_day(BotVk)
                            if len(request) > 1:
                                question = BotVk.get_question_for_lomo_training(BotVk, ''.join(request[1:]))
                            answers = BotVk.get_answers_for_simple_training(BotVk)
                            create_and_send_poll_every_day(event.chat_id, question, answers)

                            question = BotVk.get_question_for_strela_training_next_day(BotVk)
                            if len(request) > 1:
                                question = BotVk.get_question_for_lomo_training(BotVk, ''.join(request[1:]))
                            answers = BotVk.get_answers_for_simple_training(BotVk)
                            create_and_send_poll_every_day(event.chat_id, question, answers)
                        elif request[0].lower() == "#треняломо":
                            question = BotVk.get_question_for_lomo_training_next_day(BotVk)
                            if len(request) > 1:
                                question = BotVk.get_question_for_lomo_training(BotVk, ''.join(request[1:]))
                            answers = BotVk.get_answers_for_simple_training(BotVk)
                            create_and_send_poll_every_day(event.chat_id, question, answers)
                        elif request[0].lower() == "#тренястрела":
                            question = BotVk.get_question_for_strela_training_next_day(BotVk)
                            if len(request) > 1:
                                question = BotVk.get_question_for_strela_training(BotVk, ''.join(request[1:]))
                            answers = BotVk.get_answers_for_simple_training(BotVk)
                            create_and_send_poll_every_day(event.chat_id, question, answers)
                        elif request[0].lower() == "#хелп" or request[0].lower() == "#помощь" or request[0].lower() == "#help":
                            write_msg_chat(event.chat_id, get_random_id(), BotVk.get_message_help(BotVk))
    except Exception:
        print("Don't working listen messages")


# API-ключ с
f = open("token.txt")  # тут содержится токен, он необходим для подключения
token = f.readline()

vk = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkLongPoll(vk)

print("Server started")

try:
    thread_for_run = threading.Thread(target=run_listen)
    thread_for_run.start()  # слушаем события от ВК в отдельном потоке
except Exception:
    print("Dont working start thread for run listen vk api")

register_poll_in_all_different_chat_every_day()
# регистрируем все опросы в разное время для каждого

# send_poll_in_all_different_chat_every_day()
# отправляем одинаковый опрос во все чаты
# schedule.every().day.at("10:30").do(create_and_send_poll_every_day, 4)
# регистрируем вызов метода в планировщике задаче, вызываемый каждый день в конкретное время
# второй параметр это число - конкретный chat_id, куда необходимо отправить опрос в 10:30

while True:
    schedule.run_pending()
    time.sleep(1)
