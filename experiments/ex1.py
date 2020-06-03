import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

def main():

    vk = vk_api.VkApi(token="2b8aa808598003ea90db24446159e6a5badf11eead9cfd92ff17da3c86300aefabb22d10c785b1207bd53")
    vk._auth_token()
    vk.get_api()
    longpoll = VkBotLongPoll(vk, group_id=119335933)

    while True:
        for event in longpoll.listen():
            print(event.object)
            if event.type == VkBotEventType.MESSAGE_NEW:
                print(event.object.text)
            #     if event.object.peer_id == event.object.from_id:
            #         print(event.object.text)
            #         if event.object.text == "кто пидор":
            #             vk.messages.send(peer_id=peer_id, chat_id=event.chat_id, message= "Ты")


main()