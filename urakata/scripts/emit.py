# -*- coding:utf-8 -*-
import logging
import json
from cliff.command import Command
logger = logging.getLogger(__name__)


class Emit(Command):
    log = logger

    def get_parser(self, prog_name):
        parser = super(Emit, self).get_parser(prog_name)
        parser.add_argument("config")
        parser.add_argument("-overrides")
        parser.add_argument("src")
        parser.add_argument("dst")
        return parser

    def build_overrides_dict(self, parsed_args):
        with open(parsed_args.overrides) as rf:
            return json.load(rf)

    def take_action(self, parsed_args):
        from pyramid.paster import bootstrap
        from urakata.walker import get_walker
        from urakata.emitter import get_emitter
        env = bootstrap(parsed_args.config)
        request = env["request"]
        walker = get_walker(request, parsed_args.src)
        walker.walk()

        overrides = None
        if parsed_args.overrides:
            overrides = self.build_overrides_dict(parsed_args)
        emitter = get_emitter(request, parsed_args.dst, walker.config, overrides=overrides)
        emitter.emit()
