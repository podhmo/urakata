# -*- coding:utf-8 -*-
import logging
import json
from cliff.command import Command
logger = logging.getLogger(__name__)


class Scan(Command):
    log = logger

    def get_parser(self, prog_name):
        parser = super(Scan, self).get_parser(prog_name)
        parser.add_argument("config")
        parser.add_argument("root")
        parser.add_argument("-overrides")
        parser.add_argument("name", nargs="?", default="my-scaffold")
        return parser

    def build_overrides_dict(self, parsed_args):
        with open(parsed_args.overrides) as rf:
            return json.load(rf)

    def take_action(self, parsed_args):
        from pyramid.paster import bootstrap
        from urakata.walker import get_walker
        from urakata.extractor import get_extractor
        env = bootstrap(parsed_args.config)
        request = env["request"]
        walker = get_walker(request, parsed_args.root)
        walker.walk()
        walker.config.fill_defaults("")

        if parsed_args.overrides:
            overrides = self.build_overrides_dict(parsed_args)
            walker.config.defaults.update(overrides)

        extractor = get_extractor(request)
        data = extractor.extract(parsed_args.name, walker.config)
        print(json.dumps(data, indent=2, ensure_ascii=False))
