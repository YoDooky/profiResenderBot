from datetime import datetime
from typing import List, Dict

import aux_func
from database.models.utils import dbcontrol
from typing import Dict
from app_types import TGMessage

from config.db_config import MESSAGES_TABLE


def db_write_message_data(message_data: TGMessage):
    """Write message data to DB"""
    data = {
        'tg_id': message_data.tg_id,
        'tg_username': message_data.tg_username,
        'tg_phone': message_data.tg_phone,
        'tg_fname': message_data.tg_fname,
        'tg_lname': message_data.tg_lname,
        'message': message_data.message,
        'timestamp': aux_func.time_from_utc_to_moscow_timezone(message_data.timestamp)
    }
    try:
        dbcontrol.insert_db(MESSAGES_TABLE, data)
    except Exception as ex:
        print(ex)


def db_read_message_data() -> List[TGMessage]:
    """Read message data from DB"""
    data_columns = ['tg_id', 'tg_username', 'tg_phone', 'tg_fname', 'tg_lname', 'message', 'timestamp']
    table_data = dbcontrol.fetchall(MESSAGES_TABLE, data_columns)
    data_list = []
    for data in table_data:
        message_data = TGMessage(
            tg_id=data.get('tg_id'),
            tg_username=data.get('tg_username'),
            tg_phone=data.get('tg_phone'),
            tg_fname=data.get('tg_fname'),
            tg_lname=data.get('tg_lname'),
            message=data.get('message'),
            timestamp=data.get('timestamp')
        )
        data_list.append(message_data)
    return data_list


def db_get_sorted_data(data_filter: str = None) -> List[TGMessage]:
    """Read sorted message data from DB"""
    data_columns = ['tg_id', 'tg_username', 'tg_phone', 'tg_fname', 'tg_lname', 'message', 'timestamp']
    table_data = dbcontrol.sort(MESSAGES_TABLE, data_columns, 'timestamp')
    data_list = []
    for data in table_data:
        message_data = TGMessage(
            tg_id=data.get('tg_id'),
            tg_username=data.get('tg_username'),
            tg_phone=data.get('tg_phone'),
            tg_fname=data.get('tg_fname'),
            tg_lname=data.get('tg_lname'),
            message=data.get('message'),
            timestamp=data.get('timestamp')
        )
        data_list.append(message_data)

    if not data_filter:
        return data_list
    filtered_data = []
    for num, data in enumerate(data_list):
        if data_filter in data.timestamp:
            filtered_data.append(data)
        # if aux_func.compare_dates(db_timestamp=data.timestamp, filter_timestamp=data_filter):
        #     continue
        # if aux_func.compare_dates(db_timestamp=data.timestamp, filter_timestamp=data_filter):
        #     filtered_data.append(data)
        #     continue
    return filtered_data
