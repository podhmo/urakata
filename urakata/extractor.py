# -*- coding:utf-8 -*-
import json
from zope.interface import implementer
from .interfaces import IExtractor


def jsonize(name, config):
    def on_template(name, content):
        return {"name": name, "content": content, "encoding": "utf-8"}  # todo: encoding

    return {
        "name": name,
        "version": "0.0.1",
        "root": config.root,
        "parameters": list(config.parameters),
        "usages": config.usages,
        "defaults": config.defaults,
        "templates": [on_template(fname, content)
                      for fname, content in config.contents.items()]
    }


@implementer(IExtractor)
class JSONExtractor(object):
    def __init__(self, request):
        self.request = request

    def extract(self, name, config):
        D = jsonize(name, config)
        return json.dumps(D, indent=2, ensure_ascii=False)


def get_extractor(request):
    return JSONExtractor(request)
