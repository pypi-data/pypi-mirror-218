from functools import wraps

from flask import current_app


def make_transaction(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = current_app.extensions["sqlalchemy"].session
        try:
            with session.begin_nested():
                result = func(*args, **kwargs)
                session.commit()
                return result
        except Exception as e:
            session.rollback()
            raise e

    return wrapper
