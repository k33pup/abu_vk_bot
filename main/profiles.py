from keyboard import general_keyboard


def print_hero(event, collection, id_chat, vk_session):
    available_keys = ["Имя", "Баланс", "В банке", "Недвижимость", "Судимости", "Пасспорт", "Состояние", "Статус"]
    user_id = event.object.message['from_id']
    if collection.count_documents({"_id": user_id}) == 0:
        vk_session.method('messages.send',
                          {'chat_id': id_chat, 'message': f"У вас нет бандита!",
                           'random_id': 0, "keyboard": general_keyboard})
    else:
        person_data = collection.find({"_id": user_id})[0]
        person_data.pop("_id")
        text_result = ""
        for i in available_keys:
            if type(person_data[i]) == list:
                person_data[i] = " ".join(person_data[i])
            text_result += i + ": " + str(person_data[i]) + "\n" + "\n"
        vk_session.method('messages.send',
                          {'chat_id': id_chat, 'message': text_result,
                           'random_id': 0, "keyboard": general_keyboard})


def print_inventory(event, collection, id_chat, vk_session):
    key = "Инвентарь"
    user_id = event.object.message['from_id']
    if collection.count_documents({"_id": user_id}) == 0:
        vk_session.method('messages.send',
                          {'chat_id': id_chat, 'message': f"У вас нет бандита!",
                           'random_id': 0, "keyboard": general_keyboard})
    else:
        person_inventory = collection.find_one({"_id": user_id})[key]
        text_result = ""
        for i in person_inventory.keys():
            text_result += i + ": " + str(person_inventory[i]) + "\n" + "\n"
        vk_session.method('messages.send',
                          {'chat_id': id_chat, 'message': text_result,
                           'random_id': 0, "keyboard": general_keyboard})
