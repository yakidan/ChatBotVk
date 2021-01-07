import datetime


class BotVk:
    _DEFOLT_ANSWER = {'1': '8:00-11:00', '2': '11:00-14:00',
                      '3': '14:00-18:00', '4': '19:00-23:00',
                      '5': 'Не приду', '6': 'Болею'}
    time_end = 60 * 60 * 24 * 7
    question_lomo = "Ломоносова"
    question_strela = "Стрела"

    every_day_hour = 10
    every_day_minute = 0
    every_day_second = 0


    man_chat = "Мужской чат"
    woman_chat = "Женский чат"
    chat1 = "Олег, Дмитрий"
    chat2 = "Тестирование"



    def get_answers_for_simple_training(self):
        return self._DEFOLT_ANSWER


    def get_question_for_simple_training(request):
        for i in range(len(request)):
            request[i] += " "
        if len(request) > 1:
            return ''.join(request[1:])
        else:
            return "Тренировка сегодня"


    def get_question_for_lomo_training_next_day(self):
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        return self.question_lomo + " " + tomorrow.strftime('%d.%m')


    def get_question_for_lomo_training(self, date):
        return self.question_lomo + ' ' + date


    def get_question_for_strela_training(self, date):
        return self.question_strela + ' ' + date


    def get_question_for_strela_training_next_day(self):
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        return self.question_strela + " " + tomorrow.strftime('%d.%m')


    def get_message_help(self):
        return "Создать опрос для тренировки: \n " \
               "#треня <Название тренировки> (название тренировки переходит в заголовок опроса)\n" \
               "#треняломо <Дата> - создание опроса с тренировкой на Ломономова, если не указана дата, " \
               "то дата устанавливается на следующий день \n" \
               "#тренястрела <Дата> - аналогично с ломо\n" \
               "#треняломострела <Дата> - создание двух опросов для Ломоносова и Стрелы, если не указана дата, " \
               "то дата устанавливается на следующий день \n"
