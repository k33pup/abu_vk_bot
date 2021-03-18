import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import json
import config
from pymongo import MongoClient
from random import randint
from profiles import print_hero, print_inventory
from keyboard import general_keyboard

cluster = MongoClient(
    f"mongodb+srv://{config.login_mongo}:{config.pass_mongo}@abucontroller.vzuyo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster.chats
vk_session = vk_api.VkApi(token=config.TOKEN)
longpoll = VkBotLongPoll(vk_session, config.group_id)
characteristics = ["Имя", "Баланс", "В банке", "Статус", "Судимости", "Состояние"]



for event in longpoll.listen():
    '''
    if event.type == VkBotEventType.group_join:
        id_chat = event.chat_id
        if str(id_chat) not in db.getCollectionNames():
            db.createCollevtion(str(id_chat))
    '''
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.from_chat:
            id_peer = event.object.message["peer_id"]
            id_chat = event.chat_id
            msg = event
            print(msg)
            print(id_chat)
            if str(id_chat) not in db.list_collection_names():
                collection = db[str(id_peer)]
            name_collection = str(id_peer)
            collection = db[name_collection]
            text_message = msg.object.message["text"]

            if "привет" in text_message:
                print("fgd")
                vk_session.method('messages.send',
                                  {'chat_id': id_chat, 'message': f"Бандит!",
                                   'random_id': 0,
                                   "keyboard": general_keyboard})
                '''
                if "случайное число" in msg:
                    vk_session.method('messages.send',
                                      {'chat_id': id, 'message': f"Ваше число: {random.randint(1, 100)}", 'random_id': 0,
                                       "keyboard": keyboard})
                if "цитата" in msg:
                    
                '''
            if "получить бандита" in text_message:
                user_id = event.object.message['from_id']
                if collection.count_documents({"_id": user_id}):
                    vk_session.method('messages.send',
                                      {'chat_id': id_chat, 'message': f"У вас уже есть бандит!",
                                       'random_id': 0})
                else:
                    post = {
                        "_id": event.object.message['from_id'],
                        "Имя": "Бандит",
                        "Баланс": str(randint(100, 200)),
                        "В банке": 0,
                        "Статус": "обычный",
                        "Судимости": 0,
                        "Состояние": "живой",
                        "Шкала голода": "1/10",
                        "Пасспорт": ["Российский", "Американский"],
                        "Инвентарь": {
                            "Куртка": "нет",
                            "Штаны": "нет",
                            "Ботинки": "нет",
                            "Шапка": "нет",
                            "Бронежилет": "нет",
                            "Шлем": "нет",
                        },
                        "Недвижимость": ["нет"]
                    }
                    collection.insert_one(post)
                    vk_session.method('messages.send',
                                      {'chat_id': id_chat, 'message': f"Бандит создан!",
                                       'random_id': 0,
                                       "keyboard": general_keyboard})
            if "мой бандит" in text_message:
                print_hero(event, collection, id_chat, vk_session)
            if "мой инвентарь" in text_message:
                print_inventory(event, collection, id_chat, vk_session)
            if "положить в банк" in text_message:
                args = text_message.split()
                user_id = event.object.message['from_id']
                if collection.count_documents({"_id": user_id}) == 0:
                    vk_session.method('messages.send',
                                      {'chat_id': id_chat, 'message': f"У вас нет бандита!",
                                       'random_id': 0})
                else:
                    user_balance = collection.find_one({"_id": user_id})
                    if args[-1] == "банк":
                        vk_session.method('messages.send',
                                          {'chat_id': id_chat, 'message': f"Укажите сумму!",
                                           'random_id': 0})
                    elif not args[-1].isdigit():
                        vk_session.method('messages.send',
                                          {'chat_id': id_chat, 'message': f"Укажите число!",
                                           'random_id': 0})
