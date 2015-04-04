# -*- coding:utf-8 -*-
import logging
import sys
import os.path
from collections import Mapping
from pyramid.decorator import reify
logger = logging.getLogger(__name__)


class InputWrapper(object):
    def __init__(self, input_port):
        self.input_port = input_port

    def __getattr__(self, k):
        return getattr(self.input_port, k)

    def read(self):
        return input()


class EmitEnv(Mapping):
    def __init__(self, cache, defaults, usages,
                 input_port=InputWrapper(sys.stdin), output_port=sys.stderr):
        self.cache = cache
        self.defaults = defaults
        self.usages = usages
        self.input_port = input_port
        self.output_port = output_port

    def __getitem__(self, k):
        try:
            return self.cache[k]
        except:
            self.cache[k] = self.read(k)
            return self.cache[k]

    def read(self, k):
        usage = self.usages.get(k) or "{name}(default:{default}):?\n".format(name=k, default=self.defaults.get(k, ""))
        while True:
            self.output_port.write(usage)
            self.output_port.flush()
            value = self.input_port.read().rstrip()
            if value:
                return value

    def __iter__(self):
        return iter(self.cache)

    def __len__(self):
        return len(self.cache)


class Emitter(object):
    def __init__(self, request, root, config, overrides=None):
        self.request = request
        self.root = root
        self.config = config
        self.overrides = overrides or {}

    @reify
    def env(self):
        return EmitEnv(self.overrides, self.config.defaults, self.config.usages)

    def emit(self):
        for name, content in self.config.contents.items():
            self.emit_content(name, content)

    def emit_content(self, name, content):
        name_scanner = self.config.name_scanner
        template_scanner = self.config.template_scanner

        emit_name = name_scanner.replace(name, self.env)
        if template_scanner.is_template_name(name):
            content = template_scanner.replace(content, self.env)
            emit_name = template_scanner.normalize_name(emit_name)
        fullpath = os.path.join(self.root, emit_name)
        dirpath = os.path.dirname(fullpath)

        if not os.path.exists(dirpath):
            logger.debug("emit[D] -- %s", dirpath)
            os.makedirs(dirpath)

        logger.debug("emit[F] -- %s", fullpath)
        with open(fullpath, "w") as wf:
            wf.write(content)


def get_emitter(request, root, config, overrides=None):
    return Emitter(request, root, config, overrides)
