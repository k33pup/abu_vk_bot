import datetime


class Work:
    def do_robbery(self, event, collection, id_chat, vk_session):
        user_id = event.object.message['from_id']
        start_date = datetime.datetime.today()
        if collection.count_documents({"_id": user_id}) == 0:
            vk_session.method('messages.send',
                              {'chat_id': id_chat, 'message': f"У вас нет бандита!",
                               'random_id': 0, "keyboard": general_keyboard})
        elif collection.find_one({"_id": user_id})["Работа"]["Закончил работу"] == 0:
            collection.update_one({"_id": user_id}, {"$set": {"Начал работу": start_date}})
            vk_session.method('messages.send',
                              {'chat_id': id_chat,
                               'message': f"Ну и опасная же работа!\n Удачи! Через 5 минут забирай награду!",
                               'random_id': 0})

    def stop_work(self, event, collection, id_chat, vk_session):
        user_id = event.object.message['from_id']
        start_date = collection.find_one({"_id": user_id})["Работа"]["Начал работу"]
        now_date = datetime.datetime.today()
        if collection.count_documents({"_id": user_id}) == 0:
            vk_session.method('messages.send',
                              {'chat_id': id_chat, 'message': f"У вас нет бандита!",
                               'random_id': 0, "keyboard": general_keyboard})
        elif start_date == 0:
            vk_session.method('messages.send',
                              {'chat_id': id_chat, 'message': f"Вы не выходили на работу!",
                               'random_id': 0, "keyboard": general_keyboard})
        elif start_date + datetime.timedelta(minutes=5) <= now_date:
            collection.update_one({"_id": user_id}["Работа"], {"$set": {"Начал работу": 0}})
            collection.update_one({"_id": user_id}["Работа"], {"$set": {"Закончил работу": now_date}})
            vk_session.method('messages.send',
                              {'chat_id': id_chat, 'message': f"Вы поработали хорошо!",
                               'random_id': 0, "keyboard": general_keyboard})
        else:
            vk_session.method('messages.send',
                              {'chat_id': id_chat, 'message': f"Еще рано уходить!",
                               'random_id': 0, "keyboard": general_keyboard})
