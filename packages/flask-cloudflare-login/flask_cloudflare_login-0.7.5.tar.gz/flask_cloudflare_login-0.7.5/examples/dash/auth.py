from os import getenv
import logging
from functools import wraps
from flask_login import AnonymousUserMixin
from flask_login import current_user
from flask_cloudflare_login.access import CfUser


log = logging.getLogger(getenv("APP_NAME"))


class AnonymousUser(CfUser, AnonymousUserMixin):
    pass


class User(CfUser):
    pass


def login_required(fail_response="Unauthorized!"):
    def callable(fn):
        @wraps(fn)
        def login_check(*args, **kwargs):
            if not current_user.is_authenticated:
                return fail_response
            return fn(*args, **kwargs)

        return login_check

    return callable


def group_required(groups=None, fail_response="Unauthorized!"):
    def callable(fn):
        @wraps(fn)
        def group_check(*args, **kwargs):
            log.debug(groups)
            log.debug(current_user.groups)
            if current_user.groups:
                for g in current_user.groups:
                    if g.get("name") in groups:
                        return fn(*args, **kwargs)
            log.warn(f"groups: {groups} is required to access resource!")
            return fail_response

        return group_check

    return callable
