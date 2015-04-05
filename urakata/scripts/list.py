# -*- coding:utf-8 -*-
import logging
from cliff.lister import Lister
logger = logging.getLogger(__name__)


class List(Lister):
    log = logger

    def get_parser(self, prog_name):
        parser = super(List, self).get_parser(prog_name)
        parser.add_argument("config", nargs="?", default="development.ini")
        return parser

    def take_action(self, parsed_args):
        from pyramid.paster import bootstrap
        from urakata.models import Scaffold, Session, Base
        bootstrap(parsed_args.config)

        # suppress logging
        Base.metadata.bind.echo = False

        header = [("name", "version", "repository", "utime")]
        row = [(s.name, s.version, s.repository.name, s.utime) for s in Session.query(Scaffold)]
        return header + [row]
