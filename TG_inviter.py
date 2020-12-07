from pyrogram import Client
from pyrogram import filters
from pyrogram.errors import (
    BadRequest, FloodWait, InternalServerError,
    SeeOther, Unauthorized, UnknownError
)
import time
import json
import csv

ACCOUNTS_JSON_PATH = 'accounts.json'
USERS_CSV_PATH = 'members.csv'
CHAT_NAME = "testing_chat_123"


def get_accounts(file_path=ACCOUNTS_JSON_PATH):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)


def get_members(file_path=USERS_CSV_PATH):
    with open(file_path, 'r', newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=";")
        return [el[0] for el in reader]


def save_members(members, file_path=USERS_CSV_PATH):
    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerows([[el] for el in members])


def main():
    accounts = get_accounts()
    for account in accounts:
        with Client(str(account['api_id']), account['api_id'], api_hash=account['api_hash']) as app:
            i = 0
            members_usernames = get_members()
            if not members_usernames:
                continue
            members = app.get_users(members_usernames)
            not_added_members = []
            for member in members:
                try:
                    app.join_chat(CHAT_NAME)
                    app.add_chat_members(CHAT_NAME, member.id)
                    i += 1
                except Exception:
                    print('Баг')
                    not_added_members.append(member.username)
                    pass
                print("В чат добавлено: ", +i)
            save_members(not_added_members)


if __name__ == '__main__':
    main()
