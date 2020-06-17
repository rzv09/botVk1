"""
this file establishes communication
with longpoll server

Author: Raman Zatsarenko
"""

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api
import random
import time


logs_file = "/home/pi/Documents/logs.txt"
ID_ZHENYA = 369591033

gifs = ["doc151898113_553723460", "doc151898113_553723478", "doc151898113_553723471", "doc151898113_553723914",
        "doc151898113_553723932", "doc151898113_553723949", "doc151898113_553724109"]

def connect(token, group_id):
    """
    this method established connection between server and bot
    :param token: group token
    :param group_id: group id
    :return: longpoll object
    """
    vk = vk_api.VkApi(token=token)
    vk._auth_token()
    vk.get_api()

    longpoll = VkBotLongPoll(vk, group_id)
    return longpoll, vk


def bot_loop(longpoll_object, vk):
    """
    bot's main loop
    listens until the program is terminated
    :param longpoll_object: longpoll object
    :return: none
    """
    users_storage = []

    for event in longpoll_object.listen():
        print(event)
        received_event_logs(logs_file)
        if event.type == VkBotEventType.MESSAGE_NEW:
            # bot was added to the conversation
            if event.object.message["text"] == "":
                if event.object.message["action"]["type"] == "chat_invite_user":
                    vk.method("messages.send",
                          {"peer_id": event.object.message["peer_id"],
                           "message": "Pidor detector activated. Initializing all systems...",
                           "random_id": random.random(), "attachment": "doc151898113_553717223"})
            else:
                if event.object.peer_id != event.object.from_id:
                    # received message from a user
                    if event.object.message["text"] == "hello":
                        # debugging print statement
                        print(event.object.message["peer_id"])
                        vk.method("messages.send",
                                  {"user_id": event.object.message["from_id"], "peer_id": event.object.message["peer_id"],
                                   "message": "hi there", "random_id": random.random()})
                        # received a message from chat group
                    elif event.object.message["text"] == "[club119335933|@russia4life] hello":
                        vk.method("messages.send",
                                  {"peer_id": event.object.message["peer_id"],
                                   "message": "hi there", "random_id": random.random()})
                    elif event.object.message["text"] == "[club119335933|@russia4life] i m in":
                        vk.method("messages.send",
                                  {"peer_id": event.object.message["peer_id"],
                                   "message": "@id" + str(event.object.message["from_id"]) + " принял",
                                   "random_id": random.random()})
                        users_storage.append(event.object.message["from_id"])
                    elif event.object.message["text"] == "[club119335933|@russia4life] result":
                        if len(users_storage) != 0:
                            pidor_id = choose_pidor(users_storage)
                            time.sleep(3)
                            vk.method("messages.send",
                                  {"peer_id": event.object.message["peer_id"],
                                   "message": "@id" + str(pidor_id) + " " + random_phrase(),
                                   "random_id": random.random(), "attachment": gifs[random.randint(0, len(gifs)-1)]})
                            users_storage = []
                else:
                    # received message from a user
                    if event.object.message["text"] == "hello":
                        vk.method("messages.send",
                                  {"user_id": event.object.message["from_id"], "peer_id": event.object.message["peer_id"],
                                   "message": "hi there", "random_id": random.random()})
                        # received a message from chat group
                    elif event.object.message["text"] == "[club119335933|@russia4life] hello":
                        vk.method("messages.send",
                                  {"peer_id": event.object.message["peer_id"],
                                   "message": "hi there", "random_id": random.random()})
                    elif event.object.message["text"] == "[club119335933|@russia4life] i m in":
                        vk.method("messages.send",
                                  {"peer_id": event.object.message["peer_id"],
                                   "message": "@id" + str(event.object.message["from_id"]) + " принял",
                                   "random_id": random.random()})
                        users_storage.append(event.object.message["from_id"])
                    elif event.object.message["text"] == "[club119335933|@russia4life] result":
                        if len(users_storage) != 0:
                            time.sleep(3)
                            pidor_id = choose_pidor(users_storage)
                            vk.method("messages.send",
                                  {"peer_id": event.object.message["peer_id"],
                                   "message": "@id" + str(pidor_id) + " " + random_phrase(),
                                   "random_id": random.random(), "attachment": gifs[random.randint(0, len(gifs)-1)]})
                            users_storage = []


def choose_pidor(pidors):
    """
    chooses a random pidor from a list of ids
    :param pidors: list of ids
    :return: random id
    """
    pidor_index = random.randint(0, len(pidors)-1)
    if ID_ZHENYA in pidors:
        pidor_id = ID_ZHENYA
    else:
        pidor_id = pidors[pidor_index]
    return pidor_id

def random_phrase():
    """
    returns a random phrase
    :return: a random phrase which is used in bot's message
    """
    phrases = ["кто пидорас? ты пидорас", "кто кто пидорок? ты пидорок",
               "тебя хлебом не корми лишь бы пидором обозвали", "бан по причине пидарас"]
    prase_index = random.randint(0, len(phrases)-1)
    r_phrase = phrases[prase_index]
    return r_phrase

def init_logs(filename):
    """
    writes filelogs to logs.txt
    """
    file = open(filename, "a")
    file.write("\nWriting to log file. Program started running.")
    file.close()

def shut_down_logs(filename):
    """
    writes shutdown to logs.txt
    """
    file = open(filename, "a")
    file.write("\nFinished executing bot loop. Shutting down...")
    file.close()

def received_event_logs(filename):
    """
    received event from longpoll server
    sending message to the log file
    """
    file = open(filename, "a")
    file.write("\nReceived event from longpoll server")
    file.close()

def custom_message(filename, message):
    """
    prints a custom message to the logs
    """
    file = open(filename, "a")
    file.write("\n" + message)
    file.close()

def main():
    init_logs(logs_file)
    print("initializing token and group id")
    custom_message(logs_file, "initializing token and group id")
    token = '2b8aa808598003ea90db24446159e6a5badf11eead9cfd92ff17da3c86300aefabb22d10c785b1207bd53'
    group_id = 119335933
    print("connecting to lognpoll server")
    custom_message(logs_file, "connecting to longpoll server")
    longpoll, vk = connect(token, group_id)
    print("starting up bot main loop")
    custom_message(logs_file, "starting up bot main loop")
    time.sleep(10)
    bot_loop(longpoll, vk)
    shut_down_logs(logs_file)

if __name__ == '__main__':
    main()
