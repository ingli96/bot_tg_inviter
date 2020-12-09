from pyrogram import Client
from pyrogram import filters
from pyrogram.errors import (
    BadRequest, FloodWait, InternalServerError,
    SeeOther, Unauthorized, UnknownError
)
import time
from pyrogram.errors.exceptions.bad_request_400 import UserNotMutualContact
from pyrogram.errors.exceptions.forbidden_403 import Forbidden
from pyrogram.errors.exceptions.bad_request_400 import PeerFlood
from pyrogram.errors.exceptions.flood_420 import FloodWait
import json
import csv
import time

ACCOUNTS_JSON_PATH = 'accounts.json'
USERS_CSV_PATH = 'members.csv'
CHAT_NAME = "ggggg33331111"
DELAY_RANGE = 100


def get_accounts(file_path=ACCOUNTS_JSON_PATH):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)


def get_members(file_path=USERS_CSV_PATH):
    with open(file_path, 'r', newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=";")
        return [el[0] for el in reader if el[0] if el[0] != ' username']


def save_members(members, file_path=USERS_CSV_PATH):
    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerows([[el] for el in members])


def main():
    accounts = get_accounts()
    for account in accounts:
        print('Клиент:{} {}'.format(account['session_name'], account['api_id']))
        with Client(account['session_name'], account['api_id'], api_hash=account['api_hash']) as app:
            i = 0
            members_usernames = get_members()
            if not members_usernames:
                continue
            not_added_members = []
            for index, member_username in enumerate(members_usernames):
                try:
                    member = app.get_users(member_username)
                except FloodWait as ex:
                    if int(ex.x) < DELAY_RANGE:
                        print('Ожидание {} ...'.format(ex.x))
                        not_added_members.append(member_username)
                        time.sleep(ex.x)
                    else:
                        not_added_members.extend(members_usernames[index:])
                        break
                try:
                    app.join_chat(CHAT_NAME)
                    app.add_chat_members(CHAT_NAME, member.id)
                    i += 1
                except UserNotMutualContact:
                    not_added_members.append(member_username)
                    continue
                except Forbidden:
                    continue
                except PeerFlood:
                    not_added_members.extend(members_usernames[index:])
                    break
                except FloodWait as ex:
                    if int(ex.x) < DELAY_RANGE:
                        print('Ожидание {} ...'.format(ex.x))
                        not_added_members.append(member_username)
                        time.sleep(ex.x)
                    else:
                        not_added_members.extend(members_usernames[index:])
                        break

                print("В чат добавлено: ", +i)
            save_members(not_added_members)
            time.sleep(5)


if __name__ == '__main__':
    main()