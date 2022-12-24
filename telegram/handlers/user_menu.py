from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot
from aiogram.dispatcher import FSMContext

import aux_func
from config.db_config import EXCEL_TABLE_PATH
import bot_actions
from telegram import markups


class MessageState(StatesGroup):
    waiting_for_filter = State()


class UserMenu:
    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    async def user_choice(call: types.CallbackQuery):
        await call.answer()
        keyboard = markups.get_collect_data_menu()
        await call.message.answer(text='Что Вы хотите сделать? 🧐',
                                  reply_markup=keyboard)

    @staticmethod
    async def user_choice_command(message: types.Message):
        keyboard = markups.get_collect_data_menu()
        await message.answer(text='Что Вы хотите сделать? 🧐',
                             reply_markup=keyboard)

    @staticmethod
    async def get_messages(call: types.CallbackQuery):
        await call.answer()
        await call.message.answer(f'Собираю данные о сообщениях...')
        await bot_actions.collect_messages_from_telegram()
        keyboard = markups.get_collect_data_menu()
        if not bot_actions.write_data_to_excel():
            await call.message.answer(f'Еще нет сообщений')
            return
        doc = open(EXCEL_TABLE_PATH, 'rb')
        await call.message.answer_document(doc, reply_markup=keyboard)

    @staticmethod
    async def get_filter_for_messages(call: types.CallbackQuery, state: FSMContext):
        await call.answer()
        await call.message.answer(f'Введите дату в формате "yyyy-mm-dd"\n'
                                  f'например: 2022-12-30')
        await state.set_state(MessageState.waiting_for_filter.state)

    @staticmethod
    async def get_filtered_messages(message: types.Message, state: FSMContext):
        data_filter = message.text
        data_filtered = aux_func.valid_date(data_filter)
        if not data_filtered:
            await message.answer(f'Формат даты не верный. '
                                 f'Убедитесь что формат соответствует "yyyy-mm-dd"\n'
                                 f'например: 2022-12-30')
            return

        await message.answer(f'Собираю данные о сообщениях за период: {data_filter}...')
        await bot_actions.collect_messages_from_telegram()
        keyboard = markups.get_collect_data_menu()
        if not bot_actions.write_data_to_excel(data_filtered):
            await message.answer(f'За выбранную дату нет сообщений')
            return
        doc = open(EXCEL_TABLE_PATH, 'rb')
        await message.answer_document(doc, reply_markup=keyboard)
        await state.finish()

    def register_handlers(self, dp: Dispatcher):
        """Register message handlers"""
        dp.register_callback_query_handler(self.user_choice, text='start_app')
        dp.register_message_handler(self.user_choice_command, commands="messages")
        dp.register_callback_query_handler(self.get_messages, text='get_messages')
        dp.register_callback_query_handler(self.get_filter_for_messages, text='get_messages_filtered')
        dp.register_message_handler(self.get_filtered_messages, content_types='text',
                                    state=MessageState.waiting_for_filter)
