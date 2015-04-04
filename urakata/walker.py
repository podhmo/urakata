# -*- coding:utf-8 -*-
import os
from pyramid.decorator import reify
from .interfaces import INameScanner, ITemplateScanner, IScanConfig
import logging
logger = logging.getLogger(__name__)


class DirectoryWalker(object):
    def __init__(self, request, root):
        self.request = request
        self.root = root

    @reify
    def config(self):
        factory = self.request.find_service(IScanConfig)
        return factory(self.root)

    @reify
    def name_scanner(self):
        factory = self.request.find_service(INameScanner)
        return factory(self.config)

    @reify
    def template_scanner(self):
        factory = self.request.find_service(ITemplateScanner)
        return factory(self.config)

    def register(self, abspath, content):
        name = abspath.replace(self.root, "")
        self.config.add_content(name, content)

    def walk(self):
        for r, ds, fs in os.walk(self.root):
            for d in ds:
                self.name_scanner.scan(d)
            for f in fs:
                self.name_scanner.scan(f)
                fullpath = os.path.join(r, f)
                logger.debug("walk[F] -- %s", fullpath)
                with open(fullpath) as rf:
                    try:
                        self.register(fullpath, rf.read())
                        if self.template_scanner.is_template(f):
                            rf.seek(0)
                            self.template_scanner.scan(rf)
                    except UnicodeDecodeError:
                        logger.warn("skip: %s is binary file", f)


def get_walker(request, root):
    return DirectoryWalker(request, root)
