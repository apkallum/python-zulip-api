from typing import Any, Dict


class RemindMoiHandler(object):
    '''
    A docstring documenting this bot.
    '''

    def usage(self) -> str:
        return \
            '''
        A bot that schedules reminders for users.
            '''

    def handle_message(self, message: Dict[str, str], bot_handler: Any) -> None:
        bot_response = get_remind_moi_bot_response(message, bot_handler)
        bot_handler.send_reply(message, "response is hello")


def get_remind_moi_bot_response(message: Dict[str, str], bot_handler: Any) -> str:
    pass


handler_class = RemindMoiHandler
