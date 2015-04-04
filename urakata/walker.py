# -*- coding:utf-8 -*-
import os
from pyramid.decorator import reify
from .interfaces import (
    IScanConfig,
    IPredicateList
)
import logging
logger = logging.getLogger(__name__)


class DirectoryWalker(object):
    def __init__(self, request, root):
        self.request = request
        self.root = root

    @reify
    def predicates(self):
        return self.request.find_service(IPredicateList)

    @reify
    def config(self):
        factory = self.request.find_service(IScanConfig)
        return factory(self.request, self.root)

    @reify
    def name_scanner(self):
        return self.config.name_scanner

    @reify
    def template_scanner(self):
        return self.config.template_scanner

    def register(self, abspath, content):
        name = abspath.replace(self.root, "")
        self.config.add_content(name, content)

    def walk(self):
        for r, ds, fs in os.walk(self.root):
            ds[:] = [d for d in ds for p in self.predicates if p(d)]
            for d in ds:
                self.name_scanner.scan(d)
            for f in fs:
                self.name_scanner.scan(f)
                fullpath = os.path.join(r, f)
                logger.debug("walk[F] -- %s", fullpath)
                with open(fullpath) as rf:
                    try:
                        self.register(fullpath, rf.read())
                        if self.template_scanner.is_template_name(f):
                            rf.seek(0)
                            self.template_scanner.scan(rf)
                    except UnicodeDecodeError:
                        logger.warn("skip: %s is binary file", f)


def get_walker(request, root):
    return DirectoryWalker(request, root)
