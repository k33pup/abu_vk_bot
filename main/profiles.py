from keyboard import general_keyboard


class Profiles:
    def print_hero(self, event, collection, id_chat, vk_session):
        available_keys = ["Имя", "Баланс", "В банке", "Золотые слитки", "Судимости", "Состояние", "Статус"]
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
