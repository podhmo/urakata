# -*- coding:utf-8 -*-
import re
from collections import defaultdict, OrderedDict
from pyramid.decorator import reify
from zope.interface import implementer
from .interfaces import INameScanner, ITemplateScanner, IScanConfig


@implementer(IScanConfig)
class ScanConfig(object):
    def __init__(self, root):
        self.root = root
        self.parameters = set()
        self.defaults = defaultdict(str)
        self.usages = defaultdict(str)
        self.contents = OrderedDict()  # name -> content

    def add_usage(self, name, usage):
        self.usages[name] = usage

    def add_default(self, name, default):
        self.defaults[name] = default

    def add_content(self, name, content):
        self.contents[name] = content


@implementer(INameScanner)
class NameScanner(object):
    def __init__(self, config):
        self.config = config

    rx = re.compile("\+([^\+]+)\+")

    def scan(self, filename):
        for k in self.rx.findall(filename):
            self.config.parameters.add(k)


@implementer(ITemplateScanner)
class Jinja2Scanner(object):
    def __init__(self, config):
        self.config = config

    @reify
    def environment(self):
        from jinja2.environment import Environment
        return Environment()  # todo: input encofing, customize

    def is_template(self, name):
        return name.endswith(".tmpl")

    def parse(self, content):
        from jinja2 import meta
        ast = self.environment.parse(content)
        return meta.find_undeclared_variables(ast)

    def scan(self, io):
        content = io.read()
        for k in self.parse(content):
            self.config.parameters.add(k)
