from pyramid.config import Configurator


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include("pyramid_tm")
    config.include("pyramid_sqlalchemy")
    config.include("pyramid_services")
    config.enable_sql_two_phase_commit()
    config.include(register_walker)  # xxx: tentative
    config.scan()
    return config.make_wsgi_app()


def register_walker(config):
    from .scanner import NameScanner, Jinja2Scanner, ScanConfig
    from .interfaces import (
        INameScanner,
        ITemplateScanner,
        IScanConfig)
    config.register_service(NameScanner, INameScanner)
    config.register_service(Jinja2Scanner, ITemplateScanner)
    config.register_service(ScanConfig, IScanConfig)
