import asyncio
from typing import List
from save_data_to_excel import ExcelData
from telegram.telethone import collect_messages_data
from config.bot_config import API_ID, API_HASH


async def collect_messages_from_telegram():
    """Collect data about users from telegram group"""
    api_id = API_ID
    api_hash = API_HASH
    await collect_messages_data.bot_init(api_id=api_id, api_hash=api_hash)


def write_data_to_excel(data_filter: str = None):
    """Writes messages from DB to Excel"""
    excel_data = ExcelData()
    return excel_data.write_data_to_excel(data_filter)


asyncio.run(collect_messages_from_telegram())
