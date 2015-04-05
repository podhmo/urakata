# -*- coding:utf-8 -*-
from ..models import (
    Session,
    Account
)
import uuid


class Registration(object):
    def __init__(self, request):
        self.request = request

    def gen_key(self, name):  # TODO:move
        return "{}@{}".format(name, uuid.uuid4().hex)

    def account(self, name, key=None):
        account = Account(name=name)
        Session.add(account)
        key = key or self.gen_key(name)
        account.register_key(key)
        return account


def get_registration(request):
    return Registration(request)
