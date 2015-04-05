import re
from pyramid.config import Configurator


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include("pyramid_tm")
    config.include("pyramid_sqlalchemy")
    config.include("pyramid_services")
    # config.enable_sql_two_phase_commit()
    config.include(register_walker)  # xxx: tentative
    config.scan()
    return config.make_wsgi_app()


def register_walker(config):
    from .scanner import ScanConfig
    from .interfaces import (
        IPredicateList,
        IScanConfig)
    config.register_service(ScanConfig, IScanConfig)
    predicates = [
        RegexExcludePredicate(re.compile("(?:__pycache__|\.pyc|\.git|\.hg)$"))
    ]
    config.register_service(predicates, IPredicateList)


class RegexExcludePredicate(object):
    def __init__(self, rx):
        self.rx = rx

    def __call__(self, name):
        return not self.rx.search(name)
