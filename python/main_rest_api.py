"""
REST API
"""

import json
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

    try:
        data = read_data()
        print(type(data))
    except Exception as e:
        response.status = 500
        response.body = "Internal Server Error"
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

    try:
        data = read_data()
        room = [x for x in data.get("rooms") if x.get("id") == int(room_id)][0]
        output = f"""
        Id: {room.get('id')}
        Room: {room.get('name')}
        Owner: {room.get('owner').get('nickname')}
        """
        response.status = 200
        response.body = output

    except IndexError:
        response.status = 400
        response.body = f"### Room Id : {room_id} not found"

    return response


@app.get("/rooms")
def get_all_room():
    """

    :return:
    """

    try:
        data = read_data()
        rooms = (x for x in data.get("rooms"))
        output = ""

        for room in rooms:
            output += f"""
            Id: {room.get('id')}
            Room: {room.get('name')}
            Owner: {room.get('owner').get('nickname')}
            """
        response.status = 200
        response.body = output

    except IOError:
        response.status = 500
        response.body = "Internal Server Error"

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
        jsonpath_expression = parse('$.rooms[*].chats')
        data = read_data()
        output = ""

        for x in jsonpath_expression.find(data):
            chats = (chats for chats in x.value)
            chat = [chat for chat in chats if int(chat_id) == chat.get('id')][0]
            output += f"""
            Id: {chat.get('id')}
            Message: {chat.get('message')}
            Sender: {chat.get('sender').get('nickname')}
            Published: {chat.get('published_date')}
            """

            response.status = 200
            response.body = output
            break

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

    rooms_expression = parse(f'$.rooms[{int(room_id)-1}]')

    try:
        data = read_data()
        output = ""

        if len(rooms_expression.find(data)) == 0:
            response.status = 400
            response.body = f"### Room Id : {room_id} not found"
            return response

        chats_expression = parse(f'$.rooms[{int(room_id)-1}].chats')
        chats = chats_expression.find(data)[0]

        if len(chats.value) == 0:
            response.status = 200
            response.body = f"### Room Id : {room_id} found no chat"
            return response

        for x in chats_expression.find(data):
            chats = (chats for chats in x.value)

            for chat in chats:
                output += f"""
                Id: {chat.get('id')}
                Message: {chat.get('message')}
                Sender: {chat.get('sender').get('nickname')}
                Published: {chat.get('published_date')}
                """
                response.status = 200
                response.body = output

    except IndexError:
        response.status = 400
        response.body = f"### Room Id : {room_id} not found"

    return response


def validate_menu_input(action_selected):
    """
    Validate input function
    :param action_selected:
    :return: true/false
    """

    if not action_selected:
        return False, "### WARNING : Empty ID not allowed"

    if not action_selected.isnumeric():
        return False, "### WARNING : ID must be number"

    return True, ""


if __name__ == "__main__":
    run(host='localhost', port=8999, debug=True)
