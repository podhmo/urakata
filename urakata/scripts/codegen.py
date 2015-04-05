# -*- coding:utf-8 -*-
import logging
from cliff.command import Command
logger = logging.getLogger(__name__)


class Codegen(Command):
    log = logger

    def get_parser(self, prog_name):
        parser = super(Codegen, self).get_parser(prog_name)
        parser.add_argument("config")
        parser.add_argument("name")
        parser.add_argument("-version")
        return parser

    def take_action(self, parsed_args):
        from pyramid.paster import bootstrap
        from urakata.repositories import ScaffoldRepository
        from urakata.services import get_codegen, get_scan_config
        from urakata.emitter import get_emitter
        from urakata.models import Base
        env = bootstrap(parsed_args.config)

        # suppress logging
        Base.metadata.bind.echo = False

        request = env["request"]
        scaffold = ScaffoldRepository(request).get(parsed_args.name, parsed_args.version)
        if scaffold is None:
            raise RuntimeError("Scaffold[name={}, version={}] is not found".format(parsed_args.name, parsed_args.version))
        codegen = get_codegen(request)
        root = None
        emitter = get_emitter(request, root, get_scan_config(request, root))
        print(codegen.codegen(scaffold, emitter))
