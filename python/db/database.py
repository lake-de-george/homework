
import sqlite3


def create_tables():
    """

    :return:
    """
    conn = sqlite3.connect('chat-room.db')

    conn.execute('''DROP table IF EXISTS user''')
    conn.execute('''
    CREATE TABLE user(
    id INT PRIMARY KEY NOT NULL,
    uuid TEXT NOT NULL,
    level TEXT NOT NULL,
    profile_icon TEXT NOT NULL,
    nickname TEXT NOT NULL);
    ''')
    print("Create user table successfully")

    conn.execute('''DROP table IF EXISTS server''')
    conn.execute('''
    CREATE TABLE server(
    id INT PRIMARY KEY NOT NULL,
    uuid TEXT NOT NULL,
    hostname TEXT NOT NULL,
    ip_address TEXT NOT NULL);
    ''')
    print("Create server table successfully")

    conn.execute('''DROP table IF EXISTS room''')
    conn.execute('''
    CREATE TABLE room(
    id INT PRIMARY KEY NOT NULL,
    uuid TEXT NOT NULL,
    name TEXT NOT NULL,
    user_id INT NOT NULL,
    server_id INT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(server_id) REFERENCES server(id));
    ''')
    print("Create room table successfully")

    conn.execute('''DROP table IF EXISTS chat''')
    conn.execute('''
    CREATE TABLE chat(
    id INT PRIMARY KEY NOT NULL,
    uuid TEXT NOT NULL,
    sender_ip_address TEXT NOT NULL,
    message CHAR(500),
    user_id INT NOT NULL,
    published_date TEXT NOT NULL,
    room_id INT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(room_id) REFERENCES room(id));
    ''')
    print("Create chat table successfully")

    conn.close()


def insert_server(data):
    """

    :param data:
    :return:
    """
    conn = sqlite3.connect('chat-room.db')
    statement = f'''
    INSERT INTO server (id, uuid, hostname, ip_address)
    VALUES (
        {data.get('id')},
        "{data.get('uuid')}",
        "{data.get('hostname')}",
        "{data.get('ip_address')}"
    )'''
    conn.execute(statement)
    conn.commit()
    print("Insert server data successfully")
    conn.close()


def insert_user(data):
    """

    :param data:
    :param room_id:
    :return:
    """

    conn = sqlite3.connect('chat-room.db')

    for d in data:

        cursor = conn.execute(f"SELECT EXISTS (SELECT * FROM user WHERE id={d.get('id')})")
        if cursor.rowcount == -1:
            statement = f'''
            INSERT OR IGNORE INTO user (id, uuid, level, profile_icon, nickname)
            VALUES (
                {d.get('id')},
                "{d.get('uuid')}",
                "{d.get('level')}",
                "{d.get('profile_icon')}",
                "{d.get('nickname')}"
            )'''
            conn.execute(statement)
            conn.commit()
    print("Insert user data successfully")
    conn.close()


def insert_chat(data):
    """

    :param data:
    :param room_id:
    :return:
    """

    conn = sqlite3.connect('chat-room.db')

    for d in data:

        statement = f'''
        INSERT INTO chat (id, uuid, sender_ip_address, message, user_id, published_date, room_id)
        VALUES (
            {d.get('id')},
            "{d.get('uuid')}",
            "{d.get('sender_ip_address')}",
            "{d.get('message')}",
            {d.get('sender').get('id')},
            "{d.get('published_date')}",
            {d.get('room_id')}
        )'''
        conn.execute(statement)
        conn.commit()
    print("Insert chat data successfully")
    conn.close()


def insert_room(server_id, data):
    """

    :param data:
    :param server_id:
    :return:
    """

    conn = sqlite3.connect('chat-room.db')

    for d in data:
        statement = f'''
        INSERT INTO room (id, uuid, name, user_id, server_id)
        VALUES (
            {d.get('id')},
            "{d.get('uuid')}",
            "{d.get('name')}",
            {d.get('owner').get('id')},
            {server_id}
        )
        '''
        # print(statement)
        conn.execute(statement)
        conn.commit()

    print("Insert room data successfully")
    conn.close()


def select_all_room():
    """

    :return:
    """
    try:
        print("in select_all_room")
        conn = sqlite3.connect('chat-room.db')
        cursor = conn.execute("SELECT * FROM room")
        rooms = list()

        for row in cursor:
            print(row)
            room_id, uuid, name, user_id, _ = row

            # FIXME need better query here
            owner = [owner for owner in conn.execute(f"SELECT * FROM user WHERE id={user_id}")][0]
            owner_id, owner_uuid, level, profile_icon, nickname = owner

            rooms.append({
                "id": room_id,
                "uuid": uuid,
                "name": name,
                "owner": {
                    "id": owner_id,
                    "uuid": owner_uuid,
                    "level": level,
                    "profile_icon": profile_icon,
                    "nickname": nickname
                },
                "chats": list()
            })

        return rooms

    except Exception as e:
        print("Fail to select data ")
        raise
    finally:
        conn.close()


def select_room_by_id(room_id):
    """

    :return:
    """
    try:
        conn = sqlite3.connect('chat-room.db')

        # FIXME need better query here
        room = [room for room in conn.execute(f"SELECT * FROM room WHERE id={room_id}")][0]
        room_id, uuid, name, user_id, _ = room

        # FIXME need better query here
        owner = [owner for owner in conn.execute(f"SELECT * FROM user WHERE id={user_id}")][0]
        owner_id, owner_uuid, level, profile_icon, nickname = owner

        return {
            "id": room_id,
            "uuid": uuid,
            "name": name,
            "owner": {
                "id": owner_id,
                "uuid": owner_uuid,
                "level": level,
                "profile_icon": profile_icon,
                "nickname": nickname
            },
            "chats": list()
        }

    except Exception:
        raise
    finally:
        conn.close()


def select_chat_by_id(chat_id):
    """

    :return:
    """
    try:

        conn = sqlite3.connect('chat-room.db')

        # FIXME need better query here
        chat = [chat for chat in conn.execute(f"SELECT * FROM chat WHERE id={chat_id}")][0]
        chat_id, chat_uuid, sender_ip_address, message, user_id, published_date, room_id = chat

        # FIXME need better query here
        owner = [owner for owner in conn.execute(f"SELECT * FROM user WHERE id={user_id}")][0]
        owner_id, owner_uuid, level, profile_icon, nickname = owner

        return {
            "id": chat_id,
            "uuid": chat_uuid,
            "message": message,
            "sender_ip_address": sender_ip_address,
            "room_id": room_id,
            "sender": {
                "id": owner_id,
                "uuid": owner_uuid,
                "level": level,
                "profile_icon": profile_icon,
                "nickname": nickname
            },
            "published_date": published_date
        }

    except Exception:
        raise
    finally:
        conn.close()


def select_all_chat_in_room(room_id):
    """

    :return:
    """
    try:

        conn = sqlite3.connect('chat-room.db')

        # FIXME need better query here
        chats_in_room = [chats for chats in conn.execute(f"SELECT * FROM chat WHERE room_id={room_id}")]
        chats = list()

        for chat in chats_in_room:
            chat_id, chat_uuid, sender_ip_address, message, user_id, published_date, room_id = chat

            # FIXME need better query here
            owner = [owner for owner in conn.execute(f"SELECT * FROM user WHERE id={user_id}")][0]
            owner_id, owner_uuid, level, profile_icon, nickname = owner

            chats.append({
                "id": chat_id,
                "uuid": chat_uuid,
                "message": message,
                "sender_ip_address": sender_ip_address,
                "room_id": room_id,
                "sender": {
                    "id": owner_id,
                    "uuid": owner_uuid,
                    "level": level,
                    "profile_icon": profile_icon,
                    "nickname": nickname
                },
                "published_date": published_date
            })

        return chats

    except Exception:
        raise
    finally:
        conn.close()





