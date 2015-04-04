from pyramid.config import Configurator


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include("pyramid_tm")
    config.include("pyramid_sqlalchemy")
    config.enable_sql_two_phase_commit()
    config.scan()
    return config.make_wsgi_app()
