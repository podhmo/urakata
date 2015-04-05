# -*- coding:utf-8 -*-
import re
from collections import defaultdict, OrderedDict
from pyramid.decorator import reify
from zope.interface import implementer
from .interfaces import INameScanner, ITemplateScanner, IScanConfig


@implementer(IScanConfig)
class ScanConfig(object):
    def __init__(self, request, root):
        self.request = request
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

    def fill_defaults(self, v=""):
        for p in self.parameters:
            if p not in self.defaults:
                self.add_default(p, v)

    @reify
    def name_scanner(self):
        factory = self.request.find_service(INameScanner)
        return factory(self)

    @reify
    def template_scanner(self):
        factory = self.request.find_service(ITemplateScanner)
        return factory(self)


@implementer(INameScanner)
class NameScanner(object):
    def __init__(self, config):
        self.config = config

    rx = re.compile("\+([^\+]+)\+")

    def scan(self, filename):
        for k in self.rx.findall(filename):
            self.config.parameters.add(k)

    def replace(self, name, env):
        def repl(m):
            return env[m.group(1)]
        return self.rx.sub(repl, name)


@implementer(ITemplateScanner)
class Jinja2Scanner(object):
    def __init__(self, config):
        self.config = config

    @reify
    def environment(self):
        from jinja2.environment import Environment
        return Environment()  # todo: input encofing, customize

    def is_template_name(self, name):
        return name.endswith(".tmpl")

    def normalize_name(self, name):
        return name.rsplit(".tmpl", 1)[0]

    def parse(self, content):
        from jinja2 import meta
        ast = self.environment.parse(content)
        return meta.find_undeclared_variables(ast)

    def scan(self, io):
        content = io.read()
        for k in self.parse(content):
            self.config.parameters.add(k)

    def replace(self, content, env):
        from jinja2 import Template
        from jinja2.utils import concat
        t = Template(content)
        return concat(t.root_render_func(t.new_context(env)))
