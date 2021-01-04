import vk_api
import random, json
from vk_api.longpoll import VkLongPoll, VkEventType
from bot_vk import BotVk


def write_msg(user_id, random_id, message):  # отправляет сообщение в какому-то конкретному юзеру
    vk.method('messages.send', {'user_id': user_id, 'random_id': random_id, 'message': message})


def write_msg_chat(chat_id, random_id, message):  # отправляет сообщение в чат
    vk.method('messages.send', {'chat_id': chat_id, 'random_id': random_id, 'message': message})


def send_poll_in_chat(chat_id, random_id, attachment):  # отправляет опрос в чат
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


# API-ключ с
f = open("token.txt")  # тут содержится токен, он необходим для подключения
token = f.readline()

vk = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkLongPoll(vk)

print("Server started")

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
                    poll = create_poll_for_simple_training(question, answers)  # создание опроса
                    attachment = 'poll' + str(poll['owner_id']) + '_' + str(poll['id'])  # идентификатор опроса
                    send_poll_in_chat(event.chat_id, random.randint(1, 100000), attachment)  # отправка опроса
                elif request[0].lower() == "#треняломострела" or request[0].lower() == "#тренястрелаломо":
                    question = BotVk.get_question_for_lomo_training_next_day(BotVk)
                    if len(request) > 1:
                        question = BotVk.get_question_for_lomo_training(BotVk, ''.join(request[1:]))
                    answers = BotVk.get_answers_for_simple_training(BotVk)
                    poll = create_poll_for_simple_training(question, answers)
                    attachment = 'poll' + str(poll['owner_id']) + '_' + str(poll['id'])
                    send_poll_in_chat(event.chat_id, random.randint(1, 100000), attachment)

                    question = BotVk.get_question_for_strela_training_next_day(BotVk)
                    if len(request) > 1:
                        question = BotVk.get_question_for_lomo_training(BotVk, ''.join(request[1:]))
                    answers = BotVk.get_answers_for_simple_training(BotVk)
                    poll = create_poll_for_simple_training(question, answers)
                    attachment = 'poll' + str(poll['owner_id']) + '_' + str(poll['id'])
                    send_poll_in_chat(event.chat_id, random.randint(1, 100000), attachment)

                elif request[0].lower() == "#треняломо":
                    question = BotVk.get_question_for_lomo_training_next_day(BotVk)
                    if len(request) > 1:
                        question = BotVk.get_question_for_lomo_training(BotVk, ''.join(request[1:]))
                    answers = BotVk.get_answers_for_simple_training(BotVk)
                    poll = create_poll_for_simple_training(question, answers)
                    attachment = 'poll' + str(poll['owner_id']) + '_' + str(poll['id'])
                    send_poll_in_chat(event.chat_id, random.randint(1, 100000), attachment)
                elif request[0].lower() == "#тренястрела":
                    question = BotVk.get_question_for_strela_training_next_day(BotVk)
                    if len(request) > 1:
                        question = BotVk.get_question_for_strela_training(BotVk, ''.join(request[1:]))
                    answers = BotVk.get_answers_for_simple_training(BotVk)
                    poll = create_poll_for_simple_training(question, answers)
                    attachment = 'poll' + str(poll['owner_id']) + '_' + str(poll['id'])
                    send_poll_in_chat(event.chat_id, random.randint(1, 100000), attachment)
                elif request[0].lower() == "#хелп" or request[0].lower() == "#помощь" or request[0].lower() == "#help":
                    write_msg_chat(event.chat_id, random.randint(1, 1000000), BotVk.get_message_help(BotVk))
