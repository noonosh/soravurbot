from src.db.base import session
from src.db.models import User

def lang(user, context):
    try:
        return context.user_data['language_code']
    except KeyError:
        code = session.get(User, user).language_code
        context.user_data.update({'language_code': code})
        return code
