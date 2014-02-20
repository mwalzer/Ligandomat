from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
)

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from ligandomat.security import groupfinder

import MySQLdb


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
	"""

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    authn_policy = AuthTktAuthenticationPolicy('sosecret', callback=groupfinder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()

    #session cookie needed for collect data in wizard
    from pyramid.session import UnencryptedCookieSessionFactoryConfig

    my_session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')

    config = Configurator(settings=settings, session_factory=my_session_factory,
                          root_factory='ligandomat.models.RootFactory')
    config.include('pyramid_mako')
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('Ligandomat', '/Ligandomat')
    config.add_route('fyi', '/FYI')

    #action one of load_list, source, prep, run, overview
    config.add_route('upload', '/Ligandomat/upload/{action}/{attach}')
    config.add_route('data_access', '/Ligandomat/data_access/{action}')
    config.add_route('wizard_help', '/Ligandomat/help')
    config.add_route('statistics', '/Ligandomat/statistics')

    config.scan()
    return config.make_wsgi_app()
