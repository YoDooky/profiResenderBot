from typing import Dict, List
from telethon import TelegramClient
import json


async def bot_init(api_id: int, api_hash: str, phone: str):
    """Bot initialization"""
    client = TelegramClient('anon', api_id, api_hash)
    async with client:
        await collect_bot_groups(client)


def save_json_file(file_name: str, data: List[Dict]):
    """Save data to json"""
    with open(f'config/{file_name}.json', 'w', encoding='utf-8') as file:
        print('[INFO] Collected data writing to json...')
        file.write(json.dumps(data))


def open_json_file(file_name: str) -> List:
    """Get data from existing json"""
    try:
        with open(f'config/{file_name}.json', 'r', encoding='utf-8') as file:
            return json.loads(file.read())
    except Exception as ex:
        print(f'[INFO] No existing data in {file_name}.json. Creating new list...\n{ex}')
        return []


async def collect_bot_groups(client: TelegramClient):
    bot_chats = client.iter_dialogs()
    bot_groups = []
    async for chat in bot_chats:
        if not chat.is_group:
            continue
        bot_groups.append({
            'id': chat.id,
            'username': chat.message.chat.username,
            'name': chat.name,
            'title': chat.title
        })
    save_json_file(file_name='bot_groups', data=bot_groups)
