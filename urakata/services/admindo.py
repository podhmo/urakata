# -*- coding:utf-8 -*-
import logging
from urakata.decorator import reify
from . import get_registration
from ..models import Account, Session
logger = logging.getLogger(__name__)


class AdminDo(object):
    def __init__(self, request, name="admin"):
        self.request = request
        self.name = name

    def create_account(self):
        registration = get_registration(self.request)
        key = registration.gen_key(self.name)
        registration.account(self.name, key)

    @reify
    def account(self):
        return Session.query(Account).filter(Account.name == self.name).first()


def get_admindo(request, name="admin"):
    return AdminDo(request, name)
