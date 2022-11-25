import json
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot

import bot_actions

from telegram import markups


class OrderItem(StatesGroup):
    waiting_for_photo = State()
    waiting_for_question = State()


class UserMenu:
    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def check_auth(decorated_func):
        """Auth decorator"""
        def inner(*args, **kwargs):
            decorated_func(*args, **kwargs)
        return inner

    @staticmethod
    async def user_choice(call: types.CallbackQuery):
        keyboard = markups.get_user_menu()
        await call.message.answer(text='Что Вы хотите сделать? 🧐',
                                  reply_markup=keyboard)

    @staticmethod
    async def get_bot_groups(call: types.CallbackQuery):
        await call.message.edit_text(text='Собираю данные о группах, в которых состоит бот...')
        await bot_actions.collect_bot_groups_from_telegram()
        with open('C:/PyProject/profiEstateBot/config/bot_groups.json', 'r', encoding='utf-8') as file:
            data = json.loads(file.read())
        keyboard = markups.get_groups_menu(data)
        await call.message.edit_text(text='Выберите группу из которой хотите получить данные:',
                                     reply_markup=keyboard)

    @staticmethod
    async def get_group_data(call: types.CallbackQuery):
        selected_group = call.data.split('selected_group_')[1]
        await call.message.edit_text(f'Собираю данные о пользователях группы: {selected_group}.\n'
                                     f'Скорость сбора данных 50 пользователей в минуту\n'
                                     f'Пожалуйста подождите...')
        await bot_actions.get_data_from_group(group_name=selected_group)
        doc = open(f'C:/PyProject/profiEstateBot/excel/{selected_group}.xlsx', 'rb')
        keyboard = markups.get_back_button()
        await call.message.answer_document(doc, reply_markup=keyboard)

    @staticmethod
    async def send_faq(call: types.CallbackQuery):
        keyboard = markups.get_back_button()
        await call.message.edit_text(text='ℹ Справка ℹ \n\n'
                                          'Чтобы пользоваться ботом, необходимо:\n'
                                          '1) Добавить пользователя бота в целевые группы\n'
                                          '2) Нажать кнопку "Список групп", после чего бот выдаст '
                                          'список групп в которых он состоит\n'
                                          '3) Выбрать группу из которой необходимо получить '
                                          'информацию о пользователях\n'
                                          '4) Бот выдаст файл с данными о пользователях по прошествию времени',
                                     reply_markup=keyboard)

    def register_handlers(self, dp: Dispatcher):
        """Register message handlers"""
        dp.register_callback_query_handler(self.user_choice, text='start_app')
        dp.register_callback_query_handler(self.user_choice, text='back')
        dp.register_callback_query_handler(self.get_bot_groups, text='get_group_list')
        dp.register_callback_query_handler(self.send_faq, text='faq')
        dp.register_callback_query_handler(self.get_group_data, Text(contains='selected_group'))
