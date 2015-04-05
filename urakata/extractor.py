# -*- coding:utf-8 -*-
from zope.interface import implementer
from .interfaces import IExtractor


@implementer(IExtractor)
class ConfigExtractor(object):
    def __init__(self, request):
        self.request = request

    def on_template(self, name, content):
        return {"name": name, "content": content, "encoding": "utf-8"}  # todo: encoding

    def on_config(self, name, config):
        return {
            "name": name,
            "version": "0.0.1",
            "root": config.root,
            "parameters": list(config.parameters),
            "usages": config.usages,
            "defaults": config.defaults,
            "templates": [self.on_template(fname, content)
                          for fname, content in config.contents.items()]
        }

    def extract(self, name, config):
        return self.on_config(name, config)


@implementer(IExtractor)
class ModelExtractor(object):
    def __init__(self, request):
        self.request = request

    def on_template(self, t):
        return {"name": t.name, "content": t.content, "encoding": t.output_encoding}  # xxx: encoding

    def on_scaffold(self, name, scaffold):
        return {
            "name": name,
            "version": scaffold.version,
            "parameters": scaffold.parameters,
            "usages": scaffold.usages,
            "defaults": scaffold.defaults,
            "templates": [self.on_template(template) for template in scaffold.templates]
        }

    def extract(self, name, scaffold):
        return self.on_scaffold(name, scaffold)


# todo: use ZCA
class Dispatch(object):
    def __init__(self, request):
        self.request = request

    def extract(self, name, target):
        if hasattr(target, "contents"):
            return ConfigExtractor(self.request).extract(name, target)
        else:
            return ModelExtractor(self.request).extract(name, target)


def get_extractor(request):
    return Dispatch(request)
