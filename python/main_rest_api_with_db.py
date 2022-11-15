"""
REST API WITH DB
"""

import json
from db import database
from jsonpath_ng import parse
from bottle import (
    app,
    response,
    run)

app = app()


def read_data():
    """

    :return:
    """
    try:
        file = open('raw_data.json')
        json_data = json.load(file)
        file.close()
    except Exception as e:
        raise

    return json_data


@app.get("/init_data")
def init_data():
    """

    :return:
    """
    try:
        data = read_data()

        # Create tables
        database.create_tables()

        # Insert server
        database.insert_server(data)

        rooms_iterator = (x for x in data.get("rooms"))
        rooms = [room for room in rooms_iterator]
        # Insert room
        database.insert_room(
            server_id=data.get('id'),
            data=list(rooms)
        )

        chats_expression = parse(f'$.rooms[*].chats')
        chats = []
        for x in chats_expression.find(data):
            chat = (chat for chat in x.value)
            for c in chat:
                chats.append(c)

        # Insert chat
        database.insert_chat(chats)

        room_owner = (y.get('owner') for y in (x for x in data.get("rooms")))
        chat_sender = (chat.get('sender') for chat in chats)

        users = list()
        for user in list(room_owner):
            users.append(user)

        for user in list(chat_sender):
            users.append(user)

        # Insert user
        database.insert_user(users)

    except Exception as e:
        print(e)
        response.status = 500
        response.body = "Internal server Error"
    else:
        response.status = 200
        response.body = f"Initialized \n\n {json.dumps(data, indent=2)}"

    return response


@app.get("/room/<room_id>")
def get_room_by_id(room_id):
    """

    :param room_id:
    :return:
    """
    room_id = str(room_id).strip()

    valid, error_message = validate_menu_input(room_id)

    if not valid:
        response.status = 400
        response.body = error_message
        return response
    else:
        try:

            room = database.select_room_by_id(room_id)
            output = f"""
            id: {room.get('id')}
            room: {room.get('name')}
            Owner: {room.get('owner').get('nickname')}
            """
            response.status = 200
            response.body = output

        except IndexError:
            response.status = 400
            response.body = f"### room id : {room_id} not found"

        return response


@app.get("/rooms")
def get_all_room():
    """

    :return:
    """

    try:

        rooms = database.select_all_room()
        print(f"### {rooms}")
        output = str()

        for room in rooms:
            output += f"""
            id: {room.get('id')}
            room: {room.get('name')}
            Owner: {room.get('owner').get('nickname')}
            """

        response.status = 200
        response.body = output

    except Exception:
        response.status = 500
        response.body = "Internal server Error"

    return response


@app.get("/chat/<chat_id>")
def get_chat_by_id(chat_id):
    """

    :param chat_id:
    :return:
    """
    chat_id = str(chat_id).strip()

    valid, error_message = validate_menu_input(chat_id)

    if not valid:
        response.status = 400
        response.body = error_message
        return response

    try:
        chat = database.select_chat_by_id(chat_id)
        output = f"""
        id: {chat.get('id')}
        Message: {chat.get('message')}
        Sender: {chat.get('sender').get('nickname')}
        Published: {chat.get('published_date')}
        """
        response.status = 200
        response.body = output

    except IndexError:
        response.status = 400
        response.body = f"### No chat with id : {chat_id}"

    return response


@app.get("/chats/<room_id>")
def get_all_chat_in_room(room_id):

    room_id = str(room_id).strip()

    valid, error_message = validate_menu_input(room_id)

    if not valid:
        response.status = 400
        response.body = error_message
        return response

    try:
        database.select_room_by_id(room_id)

    except IndexError:
        response.status = 400
        response.body = f"### room id : {room_id} not found"
        return response

    try:
        output = str()
        chats = database.select_all_chat_in_room(room_id)

        if len(chats) == 0:
            response.status = 200
            response.body = f"### room id : {room_id} found no chat"
            return response

        for chat in chats:
            output += f"""
            id: {chat.get('id')}
            Message: {chat.get('message')}
            Sender: {chat.get('sender').get('nickname')}
            Published: {chat.get('published_date')}
            """

        response.status = 200
        response.body = output
        return response

    except Exception:
        response.status = 500
        response.body = f"### Not able to get chat"
        return response


def validate_menu_input(action_selected):
    """
    Validate input function
    :param action_selected:
    :return: true/false
    """

    if not action_selected:
        return False, "### WARNING : Empty id not allowed"

    if not action_selected.isnumeric():
        return False, "### WARNING : id must be number"

    return True, ""


if __name__ == "__main__":
    run(host='localhost', port=8998, debug=True)
