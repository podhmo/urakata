# -*- coding:utf-8 -*-
import logging
from cliff.command import Command
logger = logging.getLogger(__name__)


class Initialize(Command):
    log = logger

    def get_parser(self, prog_name):
        parser = super(Initialize, self).get_parser(prog_name)
        parser.add_argument("config", default="development.ini")
        return parser

    def take_action(self, parsed_args):
        from pyramid.paster import bootstrap
        from urakata.models import Base
        bootstrap(parsed_args.config)
        Base.metadata.create_all()
