# -*- coding:utf-8 -*-
import logging
import json
import sys
import argparse
import transaction
from cliff.command import Command
logger = logging.getLogger(__name__)


class Register(Command):
    log = logger

    def get_parser(self, prog_name):
        parser = super(Register, self).get_parser(prog_name)
        parser.add_argument("config")
        parser.add_argument("-account", default=None)
        parser.add_argument("data", type=argparse.FileType("r"), default=sys.stdin, nargs="?")
        return parser

    def take_action(self, parsed_args):
        from pyramid.paster import bootstrap
        from urakata.services import (
            get_admindo,
            get_addscaffold
        )
        if parsed_args.account:
            raise NotImplementedError("sorry not implemented, yet")

        data = json.load(parsed_args.data)

        env = bootstrap(parsed_args.config)
        request = env["request"]
        account = get_admindo(request).account

        addscaffold = get_addscaffold(request, account)
        try:
            addscaffold.add(data)
            transaction.commit()
        except:
            self.log.exception("hmm")
            transaction.abort()
