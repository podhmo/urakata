from pyramid.config import Configurator
from sqlalchemy import engine_from_config


def main(global_config, **settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    config = Configurator(settings=settings)
    config.include("pyramid_tm")
    config.scan()
    return config.make_wsgi_app()
