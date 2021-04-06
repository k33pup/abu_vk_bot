import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import config
from pymongo import MongoClient
from random import randint
from profiles import Profiles
from keyboard import general_keyboard, work_keyboard
from work import Work

cluster = MongoClient(
    f"mongodb+srv://{config.login_mongo}:{config.pass_mongo}@abucontroller.vzuyo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster.chats
vk_session = vk_api.VkApi(token=config.TOKEN)
longpoll = VkBotLongPoll(vk_session, config.group_id)
characteristics = ["Имя", "Баланс", "В банке", "Статус", "Судимости", "Состояние"]
all_profiles = Profiles()
all_jobs = Work()

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
                        "Начал работу": 0,
                        "Закончил работу": 0,
                    }
                    collection.insert_one(post)
                    vk_session.method('messages.send',
                                      {'chat_id': id_chat, 'message': f"Бандит создан!",
                                       'random_id': 0,
                                       "keyboard": general_keyboard})
            if "Работа" in text_message:
                vk_session.method('messages.send',
                                  {'chat_id': id_chat, 'message': f"Выбирай работу!",
                                   'random_id': 0,
                                   "keyboard": work_keyboard})
            if "Работа Грабеж" in text_message:
                all_jobs.do_robbery(event, collection, id_chat, vk_session)
            if "Закончить работу" in text_message:
                all_jobs.stop_work(event, collection, id_chat, vk_session)
            if "мой бандит" in text_message:
                all_profiles.print_hero(event, collection, id_chat, vk_session)