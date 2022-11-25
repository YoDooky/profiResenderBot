from typing import Dict, List
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import UserFull, User
from telethon import TelegramClient
import json


async def bot_init(api_id: int, api_hash: str, phone: str, group_name: str):
    """Bot initialization"""
    client = TelegramClient('anon', api_id, api_hash)
    async with client:
        await start_colleting_data(client, group_name)


def get_useful_data(raw_user_full_info: UserFull, raw_user_info: User) -> Dict:
    """Collecting only demand data"""
    try:
        last_online = str(raw_user_info.status.was_online)
    except Exception as ex:
        print(f'[ERR] Cant collect was_online option, {ex}')
        last_online = None
    # return {
    #     'id': raw_user_info.id,
    #     'username': raw_user_info.username,
    #     'first_name': raw_user_info.first_name,
    #     'last_name': raw_user_info.last_name,
    #     'phone': raw_user_info.phone,
    #     'was_online': last_online,
    #     'is_bot': raw_user_info.bot,
    #     'about': raw_user_full_info.about,
    #     'blocked': raw_user_full_info.blocked,
    #     'phone_calls_available': raw_user_full_info.phone_calls_available,
    #     'phone_calls_private': raw_user_full_info.phone_calls_private,
    #     'video_calls_available': raw_user_full_info.video_calls_available,
    #     'voice_message_forbidden': raw_user_full_info.voice_messages_forbidden,
    # }
    return {
        'first_name': raw_user_info.first_name,
        'last_name': raw_user_info.last_name,
        'username': raw_user_info.username,
        'phone': raw_user_info.phone,
        'phone_calls_available': raw_user_full_info.phone_calls_available,
        'id': raw_user_info.id,
        'was_online': last_online,
        'is_bot': raw_user_info.bot,
        'about': raw_user_full_info.about,
        'blocked': raw_user_full_info.blocked,
        'phone_calls_private': raw_user_full_info.phone_calls_private,
        'video_calls_available': raw_user_full_info.video_calls_available,
        'voice_message_forbidden': raw_user_full_info.voice_messages_forbidden,
    }


def save_json_file(file_name: str, data: List[Dict]):
    """Save data to json"""
    with open(f'json/{file_name}.json', 'w', encoding='utf-8') as file:
        print('[INFO] Collected data writing to json...')
        file.write(json.dumps(data))


def open_json_file(file_name: str) -> List:
    """Get data from existing json"""
    try:
        with open(f'json/{file_name}.json', 'r', encoding='utf-8') as file:
            return json.loads(file.read())
    except Exception as ex:
        print(f'[INFO] No existing data in {file_name}.json. Creating new list...\n{ex}')
        return []


async def start_colleting_data(client: TelegramClient, group_name: str):
    user_list = client.iter_participants(group_name)
    full_users_info = open_json_file(group_name)
    exist_data_id = [each_info.get('id') for each_info in full_users_info]

    users_counter = 0
    async for user in user_list:
        users_counter += 1
        if user.id in exist_data_id:
            continue
        user_info = await client(GetFullUserRequest(user))
        target_data = get_useful_data(user_info.full_user, user)
        full_users_info.append(target_data)
        print(f'[INFO] Collected {users_counter} users')
        if users_counter % 20 == 0:
            save_json_file(file_name=group_name, data=full_users_info)
    save_json_file(file_name=group_name, data=full_users_info)
