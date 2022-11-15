# homework

Prerequisite

    IDE : Pycharm/Terminal

    Required environment : Python >= 3.8

    Required libraries : jsonpath_ng, bottle, sqlite3


      pip install jsonpath_ng

      pip install bottle

      pip install sqlite3


CLI

    #> python main_cli.py


REST API with JSON 

    Start server on localhost port 8999

    #> python main_rest_api.py



REST API with SQL database

    Start server on localhost port 8998

    #> python main_rest_api_with_db.py



Available API


Init data

    GET localhost:8999/init_data  # Will read data from json

    GET localhost:8998/init_data  # Will create tables and insert data from json


Get room by id

    GET localhost:<port>/room/<room_id>


Get all room

    GET localhost:<port>/rooms


Get chat by id

    GET localhost:<port>/chat/<chat_id>


Get all chat in room

    GET localhost:<port>/chats/<room_id>

