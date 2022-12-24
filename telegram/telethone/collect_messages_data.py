import asyncio
from datetime import datetime
from telethon import TelegramClient
from telethon.types import Message

import var_globals
from app_types import TGMessage
from config.bot_config import BOT_ID
from database.controllers import message_controller


async def bot_init(api_id: int, api_hash: str):
    """Bot initialization"""
    client = TelegramClient('anon', api_id, api_hash)
    async with client:
        await start_colleting_data(client)


async def collect_user_chats(client):
    """Collects all private chats"""
    private_chat_ids = []
    async for dialog in client.iter_dialogs():
        if dialog.id == BOT_ID:
            continue
        if dialog.is_user:
            private_chat_ids.append(dialog.id)
    return private_chat_ids


def get_msg_timestamp(msg: Message) -> str:
    """Get last timestamp"""
    if msg.edit_date:
        return str(msg.edit_date).split('+')[0]
    return str(msg.date).split('+')[0]


def compare_dates(db_timestamp_str: str, tg_timestamp_str: str) -> bool:
    """Compares dates. If first arg > second arg returns true"""
    db_timestamp = datetime.strptime(db_timestamp_str, '%Y-%m-%d %H:%M:%S')
    tg_timestamp = datetime.strptime(tg_timestamp_str, '%Y-%m-%d %H:%M:%S')
    if db_timestamp >= tg_timestamp:
        return True
    else:
        return False


async def start_colleting_data(client: TelegramClient):
    """Get messages from all private chats"""
    user_chat_ids = await collect_user_chats(client)
    try:
        last_timestamp = message_controller.db_get_sorted_data()[0].timestamp
    except Exception as ex:
        last_timestamp = '2022-12-22 00:00:00'
    for chat_id in user_chat_ids:
        async for msg in client.iter_messages(chat_id):
            tg_timestamp = get_msg_timestamp(msg)
            if compare_dates(last_timestamp, tg_timestamp):
                break
            message_obj = TGMessage(
                tg_id=msg.chat.id,
                tg_username=str(msg.chat.username).replace("'", "`"),
                tg_phone=msg.chat.phone,
                tg_fname=str(msg.chat.first_name).replace("'", "`"),
                tg_lname=str(msg.chat.last_name).replace("'", "`"),
                message=str(msg.message).replace("'", "`"),
                timestamp=tg_timestamp
            )
            message_controller.db_write_message_data(message_obj)
            var_globals.new_messages.append(message_obj)
