import datetime
import random


class Work:
    def do_robbery(self, event, collection, id_chat, vk_session):
        user_id = event.object.message['from_id']
        last_date = collection.find_one({"_id": user_id})["Закончил работу"]
        start_date = datetime.datetime.today()
        if collection.count_documents({"_id": user_id}) == 0:
            vk_session.method('messages.send',
                              {'chat_id': id_chat, 'message': f"У вас нет бандита!",
                               'random_id': 0, "keyboard": None})
        elif collection.find_one({"_id": user_id})["Начал работу"] != 0:
            vk_session.method('messages.send',
                              {'chat_id': id_chat,
                               'message': f"Вы уже на работе!",
                               'random_id': 0})
        elif last_date != 0:
            if last_date + datetime.timedelta(minutes=2) > start_date:
                vk_session.method('messages.send',
                                  {'chat_id': id_chat,
                                   'message': f"Кулдаун на работу!",
                                   'random_id': 0})
            else:
                collection.update_one({"_id": user_id}, {"$set": {"Начал работу": start_date}})
                collection.update_one({"_id": user_id}, {"$set": {"Закончил работу": 0}})
                vk_session.method('messages.send',
                                  {'chat_id': id_chat,
                                   'message': f"Ну и опасная же работа!\n Удачи! Через 5 минут забирай награду!",
                                   'random_id': 0})
        elif last_date == 0:
            collection.update_one({"_id": user_id}, {"$set": {"Начал работу": start_date}})
            collection.update_one({"_id": user_id}, {"$set": {"Закончил работу": 0}})
            vk_session.method('messages.send',
                              {'chat_id': id_chat,
                               'message': f"Ну и опасная же работа!\n Удачи! Через 5 минут забирай награду!",
                               'random_id': 0})

    def stop_work(self, event, collection, id_chat, vk_session):
        user_id = event.object.message['from_id']
        start_date = collection.find_one({"_id": user_id})["Начал работу"]
        now_date = datetime.datetime.today()
        if collection.count_documents({"_id": user_id}) == 0:
            vk_session.method('messages.send',
                              {'chat_id': id_chat, 'message': f"У вас нет бандита!",
                               'random_id': 0, "keyboard": None})
        elif start_date == 0:
            vk_session.method('messages.send',
                              {'chat_id': id_chat, 'message': f"Вы не выходили на работу!",
                               'random_id': 0, "keyboard": None})
        elif start_date + datetime.timedelta(minutes=2) <= now_date:
            collection.update_one({"_id": user_id}, {"$set": {"Начал работу": 0}})
            collection.update_one({"_id": user_id}, {"$set": {"Закончил работу": now_date}})
            chance = random.randint(1, 10)
            if chance == 1:
                gold = random.randint(1, 5)
                were_gold = collection.find_one({"_id": user_id})["Золотые слитки"]
                collection.update_one({"_id": user_id}, {"$set": {"Золотые слитки": were_gold + gold}})
                vk_session.method('messages.send',
                                  {'chat_id': id_chat,
                                   'message': f"Вы поработали хорошо! И о чудо! Вы ограбили буржуя и получили {gold} золотых слитков!",
                                   'random_id': 0, "keyboard": None})
            elif chance == 2:
                collection.update_one({"_id": user_id}, {"$set": {"Баланс": 0}})
                collection.update_one({"_id": user_id}, {"$set": {"Состояние": "Без сознания"}})
                vk_session.method('messages.send',
                                  {'chat_id': id_chat,
                                   'message': f"Вы решили ограбить скинхеда, а он привел толпу людей и вас избили, а так же забрали все деньги в кармане!",
                                   'random_id': 0, "keyboard": None})
            else:
                cash = random.randint(1000, 2000)
                were_cash = collection.find_one({"_id": user_id})["Баланс"]
                collection.update_one({"_id": user_id}, {"$set": {"Баланс": were_cash + cash}})
                vk_session.method('messages.send',
                                  {'chat_id': id_chat,
                                   'message': f"Вы поработали хорошо! Награбили на {cash} рублей!",
                                   'random_id': 0, "keyboard": None})
        else:
            vk_session.method('messages.send',
                              {'chat_id': id_chat, 'message': f"Еще рано уходить!",
                               'random_id': 0, "keyboard": None})
