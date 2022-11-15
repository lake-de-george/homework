"""
Simple CLI script
"""

import os
import json
from jsonpath_ng import parse

SOURCE_DIR = os.path.dirname(__file__)
FILENAME = "raw_data.json"
MENUS = {
    "1": "Initialize data",
    "2": "getRoomById",
    "3": "getAllRoom",
    "4": "getChatById",
    "5": "getAllChatInRoom"
}


def main():
    """

    :return:
    """
    action_menu = """
---------------------------
    Action
    1. Initialize data
    2. getRoomById
    3. getAllRoom
    4. getChatById
    5. getAllChatInRoom
---------------------------
    """

    print(action_menu)

    while True:
        action_selected = input("Select the action: ")
        if validate_menu_input(action_selected):
            break

    menu(action_selected)


def validate_menu_input(action_selected):
    """
    Validate input function
    :param action_selected:
    :return: true/false
    """

    if not action_selected:
        return

    if not action_selected.isnumeric():
        print("### WARNING : Input must be number")
        return

    if int(action_selected) not in range(1, 6):
        print("### WARNING : Input must only be number between 1..5")
        return

    return True


def menu(action):
    """

    :param action:
    :return:
    """
    global json_data

    if action == "1":
        try:
            json_data = json.load(open(FILENAME))
        except Exception as e:
            print(e)
        else:
            sep = '/' if '/' in SOURCE_DIR else '\\'
            print(f"### {MENUS.get(action)} with file path: {SOURCE_DIR}{sep}{FILENAME}")

            print(f"### Initialized")
            main()

    if action == "2":
        try:
            get_room_by_id(f"{MENUS.get(action)}: ", json_data)
        except NameError:
            print(f"### You need to initialize data (Action No.1) first..")
            main()

    if action == "3":
        try:
            get_all_room(json_data)
        except NameError:
            print(f"### You need to initialize data (Action No.1) first..")
            main()

    if action == "4":
        try:
            get_chat_by_id(f"{MENUS.get(action)}: ", json_data)
        except NameError:
            print(f"### You need to initialize data (Action No.1) first..")
            main()

    if action == "5":
        try:
            get_all_chat_in_room(f"{MENUS.get(action)}: ", json_data)
        except NameError:
            print(f"### You need to initialize data (Action No.1) first..")
            main()


def get_room_by_id(menu, data):
    """

    :param menu:
    :param data:
    :return:
    """

    while True:
        content_id = input(menu)
        if not content_id:
            continue

        if not content_id.isnumeric():
            print("### WARNING : Input must be number")
            continue
        break

    try:
        room = [x for x in data.get("rooms") if x.get("id") == int(content_id)][0]
        output = f"""
        Id: {room.get('id')}
        Room: {room.get('name')}
        Owner: {room.get('owner').get('nickname')}
        """
        print(output)
    except IndexError:
        print(f"### No room with id : {content_id}")

    main()


def get_all_room(data):
    """

    :param menu:
    :param data:
    :return:
    """

    rooms = (x for x in data.get("rooms"))

    for room in rooms:
        output = f"""
        Id: {room.get('id')}
        Room: {room.get('name')}
        Owner: {room.get('owner').get('nickname')}
        """
        print(output)

    main()


def get_all_chat_in_room(menu, data):
    """

    :param menu:
    :param data:
    :return:
    """

    while True:
        content_id = input(menu)
        if not content_id:
            continue

        if not content_id.isnumeric():
            print("### WARNING : Input must be number")
            continue
        break

    rooms_expression = parse(f'$.rooms[{int(content_id)-1}]')

    if len(rooms_expression.find(data)) == 0:
        print(f"### No room with id : {content_id}")
        main()
    else:
        chats_expression = parse(f'$.rooms[{int(content_id)-1}].chats')
        chats = chats_expression.find(data)[0]
        if len(chats.value) == 0:
            print(f"### No chat in room Id : {content_id}")
            main()

        for x in chats_expression.find(data):
            chats = (chats for chats in x.value)

            for chat in chats:
                output = f"""
                Id: {chat.get('id')}
                Message: {chat.get('message')}
                Sender: {chat.get('sender').get('nickname')}
                Published: {chat.get('published_date')}
                """
                print(output)

    main()


def get_chat_by_id(menu, data):
    """

    :param menu:
    :param data:
    :return:
    """

    while True:
        content_id = input(menu)
        if not content_id:
            continue

        if not content_id.isnumeric():
            print("### WARNING : Input must be number")
            continue
        break

    try:
        jsonpath_expression = parse('$.rooms[*].chats')

        for x in jsonpath_expression.find(data):
            chats = (chats for chats in x.value)
            chat = [chat for chat in chats if int(content_id) == chat.get('id')][0]
            output = f"""
            Id: {chat.get('id')}
            Message: {chat.get('message')}
            Sender: {chat.get('sender').get('nickname')}
            Published: {chat.get('published_date')}
            """
            print(output)
            break

    except IndexError:
        print(f"### No room with id : {content_id}")

    main()


if __name__ == '__main__':
    main()
