# -*- coding:utf-8 -*-
from ..models import (
    Session,
    Repository)
from urakata.decorator import reify


class AddScaffold(object):
    def __init__(self, request, account):
        self.request = request
        self.account = account

    @reify
    def repository(self):
        # xxx:
        return Session.query(Repository).filter(Repository.account == self.account).first()

    def add_repository(self):
        return self.account.register_repository(name=self.account.name)

    def add_scaffold(self, data):
        name = data["name"]
        version = data["version"]
        parameters = data["parameters"]
        defaults = data["defaults"]
        usages = data["usages"]

        scaffold = self.repository.get_scaffold(name)
        if scaffold is None:
            return self.repository.register_scaffold(name, version, parameters, defaults, usages)
        else:
            return scaffold.swap(name, version, parameters, defaults, usages)
        return scaffold

    def add_template(self, scaffold, data):
        name = data["name"]
        content = data["content"]
        encoding = data["encoding"]
        return scaffold.register_template(name, content, encoding)

    def add(self, data):
        if self.repository is None:
            self.repository = self.add_repository()

        scaffold = self.add_scaffold(data)
        for template_data in data["templates"]:
            self.add_template(scaffold, template_data)


def get_addscaffold(request, account):
    return AddScaffold(request, account)
