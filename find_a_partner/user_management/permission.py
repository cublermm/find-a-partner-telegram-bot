from telegram import Update

from find_a_partner.persistence.entities import User
from find_a_partner.persistence.models.base_model import db
from find_a_partner.persistence.models.user import UserLevel, TrustedState

# error messages
ERR_MSG_NOT_REQUIRED_PERMISSION = 'Sorry, du hast nicht die Berechtigung dieses Kommando auszuführen'


def ensure_required_user_level(update: Update, user_level: UserLevel) -> bool:
    """
    ensure user has required user level
    - send error message to user if not
    @param update:
    @param user_level:
    """
    user = User.get_by_telegram_id(update.message.from_user.id)
    if user.user_level != user_level:
        update.message.reply_text(ERR_MSG_NOT_REQUIRED_PERMISSION)
        return False
    return True


def trust_user(username: str, reason: str):
    """
    set user as trusted
    @param username:
    @param reason:
    """
    with db.atomic():
        user = User.get_by_username(username)
        user.trusted_state = TrustedState.TRUSTED
        user.trusted_reason = reason
        User.update(user)


def is_trusted(user_id: int):
    """
    check if user is trusted
    @param user_id:
    @return: if user is trusted
    """
    user = User.get_by_id(user_id)
    return user.trusted_state == TrustedState.TRUSTED