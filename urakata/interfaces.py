# -*- coding:utf-8 -*-
from zope.interface import (
    Interface,
    Attribute
)


class IPredicateList(Interface):
    def __iter__():
        pass


class IScanConfig(Interface):
    root = Attribute("root name[IString]")
    parameters = Attribute("parameters[ISet]")
    defaults = Attribute("default value of scaffold[IDict]")
    usages = Attribute("usage of scaffold[IDict]")


class INameScanner(Interface):
    config = Attribute("config[IScanConfig]")

    def scan(filename):
        pass

    def replace(filename, env):
        pass


class ITemplateScanner(Interface):
    config = Attribute("config[IScanConfig]")

    def is_template_name(name):
        pass

    def normalize_name(name):
        pass

    def scan(io):
        pass

    def replace(content, env):
        pass


class IExtractor(Interface):
    def extract(name, config):
        pass
