# -*- coding:utf-8 -*-
import logging
import transaction
from cliff.command import Command
logger = logging.getLogger(__name__)


class Initialize(Command):
    log = logger

    def get_parser(self, prog_name):
        parser = super(Initialize, self).get_parser(prog_name)
        parser.add_argument("config", nargs="?", default="development.ini")
        parser.add_argument("--disable-admin", type=bool)
        parser.add_argument("--logging", choices=["DEBUG", "INFO", "WARNING", "ERROR"], default="INFO")
        return parser

    def take_action(self, parsed_args):
        import logging
        from pyramid.paster import bootstrap
        from urakata.models import Base
        logging.basicConfig(level=parsed_args.logging)
        env = bootstrap(parsed_args.config)
        Base.metadata.create_all()

        if not parsed_args.disable_admin:
            self.create_admin(env["request"])

    def create_admin(self, request):
        from urakata.services import get_admindo
        admindo = get_admindo(request)
        if admindo.account is None:
            try:
                admindo.create_account()
                transaction.commit()
            except:
                self.log.exception("hmm")
                transaction.rollback()
