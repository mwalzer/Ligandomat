import os
import shutil
import re
import hashlib
from sqlalchemy import and_
from docutils.core import publish_parts

from sqlalchemy.ext.declarative import declarative_base
from datetime import *

from mako.template import Template
from pyramid.response import Response

from pyramid.response import Response
from pyramid.view import (
    view_config,
    forbidden_view_config,
)
from pyramid.security import (
    remember,
    forget,
    authenticated_userid,
)
from ligandomat.tools import queries
from ligandomat.tools.queryCreator import create_query
from .security import groupfinder
from .forms import Source, Prep, Mass_spec, DataQuery
from .transformer import *
from pyramid.httpexceptions import HTTPFound
from sqlalchemy.exc import DBAPIError
from .models import *
from datetime import *

from DBtransfer import *
from run_list_handling import *
from tools import reader, patternRec
import tools
import presentData

# Index Page ----------------------------------------------------------------------------------------------------------
@view_config(route_name='home', renderer='ligandomat:templates/index.mako', permission='view')
def index(request):
    return dict(logged_in=authenticated_userid(request))


# Login ----------------------------------------------------------------------------------------------------------
@view_config(route_name='login', renderer='ligandomat:templates/login.mako', permission='view')
def login(request):
    """ Login function using md5 hashing for security check."""
    login_url = request.route_url('home')
    referrer = request.url
    if referrer == login_url:
        referrer = '/'  # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    login = ''
    password = ''
    message = ''
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']

        sha = hashlib.md5()
        sha.update(password)
        password = sha.digest().encode('hex')
        uc = DBSession.query(User).filter(and_(User.username == login, User.password == password)).count()
        if (uc != 0):
            headers = remember(request, login)
            return HTTPFound(location=request.route_url('Ligandomat'), headers=headers)
        else:
            message = 'Failed login'

    return dict(
        message=message,
        url=request.route_url('login'),
        came_from=came_from,
        logged_in=authenticated_userid(request),
        login=login,
        password=password,
    )


# Logout ----------------------------------------------------------------------------------------------------------
@view_config(route_name='logout')
def logout(request):
    """ Logout function

    TODO: Remove already uploaded session data.
    """
    headers = forget(request)
    return HTTPFound(location=request.route_url('home'),
                     headers=headers)


# Ligandomat Start ---------------------------------------------------------------------------------------------------------------
@view_config(route_name='Ligandomat', renderer='ligandomat:templates/start.mako', permission='edit')
def choice_page(request):
    return dict(
        logged_in=authenticated_userid(request)
    )


# DB Statistics ---------------------------------------------------------------------------------------------------------------------
@view_config(route_name='statistics', renderer='ligandomat:templates/output/statistics.mako', permission='view')
def statistics_page(request):
    """ Old statistics page. Should be removed"""
    seqs = getAllPeptide_Sequence(DBSession, Peptide)

    return dict(logged_in=authenticated_userid(request),
                seqs=seqs,
                nSeqs=len(seqs)
    )


# Access Data - Query---------------------------------------------------------------------------------------------------------------
@view_config(route_name='data_access', renderer='ligandomat:templates/output/data_query.mako',
             match_param='action=query', permission='view')
def access_data_query(request):
    """"Query website and functionality

    The query-strings are in queries.py.
    Connection to the DB using MySQLdb. NOT pyramid!
    """



    form = DataQuery(request.POST)
    form.setChoices()
    session = request.session



    # Collecting input from Mako and creating query parts
    query_dict = create_query(request.params)


    # Connecting to the DB using MySQLdb
    conn = MySQLdb.connect(host=config.host, user=config.user, passwd=config.passwd, db=config.db,
                           port=config.port)
    c = conn.cursor(MySQLdb.cursors.DictCursor)

    print("hullu")
    # Use this if the sequence is a query criteria to speed up the query
    if 'sequence' in request.params:
        print("hallo")
        querystring = queries.search_by_sequence_first
        c.execute(querystring % (query_dict.get("sequence"), query_dict.get("spectrum_hit"), query_dict("run_name"), query_dict.get("source") ))
        result = c.fetchall()
        template = Template(filename='./ligandomat/templates/output/table_all_infos.mako')
        result = template.render(rows = result)
        return Response(result)


    if 'search_by_subsequence' in request.params:
        searchstring = pat
        querystring = queries.search_by_subsequence

        c.execute(querystring % (searchstring, pat_sorting_by))
        result = c.fetchall()
        #result = database_prediction(result)
        #result = annotate(result)
        template = Template(filename='./ligandomat/templates/output/table_all_infos.mako')
        result = template.render(rows = result)
        return Response(result)


    if 'search_by_runname' in request.params:
        querystring = queries.search_by_runname
        c.execute(querystring % (run_pat, runname_sorting_by))
        result = c.fetchall()
        #	result = database_prediction(result)
        #result = annotate(result)
        #output = template('table_run_query', rows=result)
        template = Template(filename='./ligandomat/templates/output/table_all_infos.mako')
        result = template.render(rows=result)
        return Response(result)

    if 'search_by_organ' in request.params:
        querystring = queries.search_by_organ
        c.execute(querystring % (organ, organ_sorting_by))
        result = c.fetchall()
        #result = database_prediction(result)
        #result = annotate(result)
        #output = template('table_all_infos', rows=result)
        template = Template(filename='./ligandomat/templates/output/table_all_infos.mako')
        result = template.render(rows=result)
        return Response(result)

    if 'search_by_tissue' in request.params:
        querystring = queries.search_by_tissue
        c.execute(querystring % (tissue, tissue_sorting_by))
        result = c.fetchall()
        #result = database_prediction(result)
        #result = annotate(result)
        #output = template('table_all_infos', rows=result)
        template = Template(filename='./ligandomat/templates/output/table_all_infos.mako')
        result = template.render(rows=result)
        return Response(result)

    # If no case was selected return to the site itself
    return dict(form=form, logged_in=authenticated_userid(request))



# Forbidden View
@forbidden_view_config()
def unallowed(request):
    return Response(
        "[Forbidden_view_Error] You are not allowed to enter this page. User currently logged in: %s " % authenticated_userid(
            request))


# For your Information	
@view_config(route_name='fyi', renderer='ligandomat:templates/fyi.mako', permission='view')
def fyi(request):
    """ Some kind of error page. Has to be changed or removed."""
    message = request.session['fyi']
    image = request.session['image']
    return dict(logged_in=authenticated_userid(request), message=message, image=image)











