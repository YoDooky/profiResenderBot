import asyncio

from aiogram import Bot
import aioschedule

import var_globals
from bot_actions import collect_messages_from_telegram
from config.bot_config import USER_ID


class Schedule:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def resend_messages(self):
        for message in var_globals.new_messages:
            
            await self.bot.send_message(USER_ID, f'от: @{message.tg_username}\n'
                                                 f'сообщение: {message.message}')
            await asyncio.sleep(1)

    async def scheduler(self):
        """Shedule loop"""
        self.update_db_messages_schedule()
        while True:
            if var_globals.new_messages:
                await self.resend_messages()
                var_globals.new_messages = []
            await aioschedule.run_pending()
            await asyncio.sleep(5)

    @staticmethod
    def update_db_messages_schedule():
        """Make new shedule"""
        # print('[SCHEDULE] Write messages from TG to DB every day at 10:00')
        # aioschedule.clear()
        # aioschedule.every().day.at('10:00').do(collect_messages_from_telegram)
        print('[SCHEDULE] Write messages from TG to DB every minute')
        aioschedule.clear()
        aioschedule.every().minute.do(collect_messages_from_telegram)
