from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def get_start_menu():
    user_menu = InlineKeyboardMarkup(row_width=1)
    start_button = InlineKeyboardButton(text='🤖Начать работу с ботом🤖', callback_data='start_app')
    user_menu.insert(start_button)
    return user_menu


def get_user_menu():
    user_menu = InlineKeyboardMarkup(row_width=2)
    get_group_list_button = InlineKeyboardButton(text='Список групп', callback_data='get_group_list')
    faq_button = InlineKeyboardButton(text='ℹ Справка', callback_data='faq')
    user_menu.insert(get_group_list_button)
    user_menu.insert(faq_button)
    return user_menu


def get_groups_menu(groups_list):
    group_menu = InlineKeyboardMarkup(row_width=1)
    add_group_buttons(groups_list=groups_list, group_menu=group_menu)
    back_button = InlineKeyboardButton(text='👈 Вернуться назад', callback_data='back')
    group_menu.insert(back_button)
    return group_menu


def add_group_buttons(groups_list, group_menu):
    for group in groups_list:
        select_group_button = InlineKeyboardButton(text=f'{group.get("username")}',
                                                   callback_data=f'selected_group_{group.get("username")}')
        group_menu.insert(select_group_button)
    return group_menu


def get_back_button():
    back_menu = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text='👈 Вернуться назад', callback_data='back')
    back_menu.insert(back_button)
    return back_menu
