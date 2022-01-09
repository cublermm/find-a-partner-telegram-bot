from telegram import Bot

from bot_config import TOKEN
from find_a_partner.persistence.entities import Message
from find_a_partner.persistence.entities.User import get_all_admins, get_all_trusted_users
from find_a_partner.persistence.models.message import NewMessage
from find_a_partner.persistence.models.user import User

MSG_PREFIX_SEARCH_REQUEST = 'Suchanfrage von:'


def add_message_request(user: User, message_content: str) -> None:
    """
    persist message request for future processing
    redirect message requests to all admins
    @param user:
    @param message_content:
    """
    # persist message in database
    new_message = NewMessage(user=user, content=message_content)
    message = Message.create(new_message)

    # redirect message request to all admins
    # TODO: strip command prefix
    request_message = f'Message ID: {str(message.get_id())}' \
                      f' - User: {user.username} posted a request\n {message_content}'
    send_message_to_admins(request_message)


def confirm_message_request(message_id) -> None:
    """
    redirect message to all trusted users
    @param message_id:
    @param message_content:
    """

    # redirect message request to all trusted users
    message = Message.get_by_id(message_id)
    # TODO: strip command prefix
    search_message = f'{MSG_PREFIX_SEARCH_REQUEST} https://t.me/{message.user.username} \n {message.content}'
    send_message_to_admins(search_message)


def send_message_to_admins(message_text):
    """
    send message to all admins
    @param message_text:
    """
    admins = get_all_admins()
    bot = Bot(TOKEN)
    for admin in admins:
        bot.send_message(admin.telegram_id, message_text)


def send_message_to_trusted_users(message_text):
    """
    send message to all trusted users
    @param message_text:
    """
    trusted_users = get_all_trusted_users()
    bot = Bot(TOKEN)
    for trusted_user in trusted_users:
        bot.send_message(trusted_user.telegram_id, message_text)
