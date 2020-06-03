"""
this file establishes communication
with longpoll server

Author: Raman Zatsarenko
"""



from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api
import random

vk = vk_api.VkApi(token='2b8aa808598003ea90db24446159e6a5badf11eead9cfd92ff17da3c86300aefabb22d10c785b1207bd53')
vk._auth_token()
vk.get_api()

longpoll = VkBotLongPoll(vk, 119335933)


for e in longpoll.listen():
    # debugging print statement
    print(e)
    print(e.object.message["action"]["type"])
    if e.type == VkBotEventType.MESSAGE_NEW:
        if e.object.peer_id != e.object.from_id:
            # received message from a user
            if e.object.message["text"] == "hello":
                # debugging print statement
                print(e.object.message["peer_id"])
                vk.method("messages.send",
                          {"user_id": e.object.message["from_id"], "peer_id": e.object.message["peer_id"],
                           "message": "hi there", "random_id": random.random()})
                # received a message from chat group
            elif e.object.message["text"] == "[club119335933|@russia4life] hello":
                vk.method("messages.send",
                          {"peer_id": e.object.message["peer_id"],
                           "message": "hi there", "random_id": random.random()})
            elif e.object.message["text"].lower() == "[club119335933|@russia4life] i m in":
                pass
        else:
            # received message from a user
            if e.object.message["text"] == "hello":
                vk.method("messages.send",
                          {"user_id": e.object.message["from_id"], "peer_id": e.object.message["peer_id"],
                           "message": "hi there", "random_id": random.random()})
                # received a message from chat group
            elif e.object.message["text"] == "[club119335933|@russia4life] hello":
                vk.method("messages.send",
                          {"peer_id": e.object.message["peer_id"],
                           "message": "hi there", "random_id": random.random()})
    # bot was added to a conversation
        elif e.action["type"] == 'chat_invite_user':
            vk.method("messages.send",
                          {"peer_id": e.object.message["peer_id"],
                           "message": "hi there", "random_id": random.random()})