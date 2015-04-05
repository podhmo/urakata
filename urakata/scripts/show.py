# -*- coding:utf-8 -*-
import logging
from cliff.lister import Lister
logger = logging.getLogger(__name__)


class Show(Lister):
    log = logger

    def get_parser(self, prog_name):
        parser = super(Show, self).get_parser(prog_name)
        parser.add_argument("config", nargs="?", default="development.ini")
        parser.add_argument("-version", default=None)
        parser.add_argument("name")
        return parser

    def take_action(self, parsed_args):
        from pyramid.paster import bootstrap
        from urakata.models import Base
        from urakata.repositories import ScaffoldRepository
        env = bootstrap(parsed_args.config)
        request = env["request"]

        # suppress logging
        Base.metadata.bind.echo = False

        scaffold = ScaffoldRepository(request).get(parsed_args.name, parsed_args.version)
        header = [("name", "utime")]
        row = [(t.name, t.utime) for t in scaffold.templates]
        return header + [row]
