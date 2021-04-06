import datetime


class Work:
    def do_robbery(self, event, collection, id_chat, vk_session):
        user_id = event.object.message['from_id']
        last_date = collection.find_one({"_id": user_id})["Закончил работу"]
        start_date = datetime.datetime.today()
        if collection.count_documents({"_id": user_id}) == 0:
            vk_session.method('messages.send',
                              {'chat_id': id_chat, 'message': f"У вас нет бандита!",
                               'random_id': 0, "keyboard": None})
            return
        if last_date == 0:
            collection.update_one({"_id": user_id}, {"$set": {"Начал работу": start_date}})
            vk_session.method('messages.send',
                              {'chat_id': id_chat,
                               'message': f"Ну и опасная же работа!\n Удачи! Через 5 минут забирай награду!",
                               'random_id': 0})
            return
        if last_date + datetime.timedelta(minutes=10) > start_date:
            vk_session.method('messages.send',
                              {'chat_id': id_chat,
                               'message': f"Кулдаун на работу!",
                               'random_id': 0})
            return
        elif collection.find_one({"_id": user_id})["Начал работу"] != 0:
            vk_session.method('messages.send',
                              {'chat_id': id_chat,
                               'message': f"Вы уже на работе!",
                               'random_id': 0})
        elif collection.find_one({"_id": user_id})["Начал работу"] == 0:
            collection.update_one({"_id": user_id}, {"$set": {"Начал работу": start_date}})
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
        elif start_date + datetime.timedelta(minutes=5) <= now_date:
            collection.update_one({"_id": user_id}, {"$set": {"Начал работу": 0}})
            collection.update_one({"_id": user_id}, {"$set": {"Закончил работу": now_date}})
            vk_session.method('messages.send',
                              {'chat_id': id_chat, 'message': f"Вы поработали хорошо!",
                               'random_id': 0, "keyboard": None})
        else:
            vk_session.method('messages.send',
                              {'chat_id': id_chat, 'message': f"Еще рано уходить!",
                               'random_id': 0, "keyboard": None})
