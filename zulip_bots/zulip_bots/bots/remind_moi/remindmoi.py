import os
import json
import requests

from typing import Any, Dict
from datetime import timedelta, datetime

COMMANDS = ['add', 'remove']
UNITS = ['minute', 'minutes', 'hour', 'hours', 'day','days', 'week', 'weeks']

ADD_ENDPOINT = 'http://localhost:8000/add_reminder/'


class RemindMoiHandler(object):
    '''
    A docstring documenting this bot.
    the reminder bot reminds people of its reminders
    '''

    def usage(self) -> str:
        return \
            '''
        A bot that schedules reminders for users.
        <COMMAND> reminder <int> UNIT <str>
            '''

    def handle_message(self, message: Dict[str, Any], bot_handler: Any) -> None:
        bot_response = get_remind_moi_bot_response(message, bot_handler)
        bot_handler.send_reply(message, bot_response)


def get_remind_moi_bot_response(message: Dict[str, Any], bot_handler: Any) -> str:

    if is_valid_content(message['content']):
        try:
            reminder_object = parse_content(message)
            response = requests.post(url=ADD_ENDPOINT, json=reminder_object)
            response = response.json()
            assert response['success']
        except (json.JSONDecodeError, AssertionError):
            return "Something went wrong"

        # append_json_file('reminders.json', reminder_object)
        return "Reminder stored."  # TODO: Better message
    else:
        return "Invlaid input. Please check help."


def is_valid_content(content: str, commands=COMMANDS, units=UNITS) -> bool:
    """
    Ensure message is in form <COMMAND> reminder <int> UNIT <str>
    """
    content = content.split(' ', maxsplit=4)  # Ensure the last element is str
    return all((
        content[0] in commands,
        content[1] == 'reminder',
        type(int(content[2])) == int,
        content[3] in units,
        type(content[4]) == str
    ))


def parse_content(message: Dict[str, Any]) -> Dict[str, Any]:
    """
    Given a message object with reminder details,
    construct a JSON/dict.
    """
    content = message['content'].split(' ', maxsplit=4)  # Ensure the last element is str
    return {
        "zulip_user_id": message['sender_id'],
        "title": content[4],
        "created": message['timestamp'],
        "deadline": compute_deadline_timestamp(message['timestamp'], content[2], content[3]),
        "active": True
    }


def compute_deadline_timestamp(timestamp_submitted: str, time_value: int, time_unit: str) -> str:
    """
    Given a submitted stamp and an interval,
    return deadline timestamp.
    """
    interval = timedelta(**{time_unit: int(time_value)})  # TODO: Create sanitize function
    datetime_submitted = datetime.fromtimestamp(timestamp_submitted)
    return (datetime_submitted + interval).timestamp()


def standardize_time_units(input: str) -> str:
    pass


def append_json_file(filename: str, new_data: Dict[str, Any]) -> None :
    file_path = "{}/{}".format(os.path.dirname(os.path.realpath(__file__)), filename)

    data_collected = load_json_file(file_path)

    # append data to 'data_collected' dict
    data_collected[len(data_collected)] = new_data

    save_json_file(file_path, data_collected)


def save_json_file(file_path, json_data: Dict[str, Any]):
    with open(file_path, 'w') as fp:
        json.dump(json_data, fp)


def load_json_file(file_path):
    if not os.path.isfile(file_path):
        with open(file_path, 'w+') as fp:
            json.dump({}, fp)
        return {}

    with open(file_path, 'r+') as fp:
        try:
            data = json.load(fp)
        except Exception:
            fp.truncate(0)
            json.dump({}, fp)
            data = {}
    return data


handler_class = RemindMoiHandler
