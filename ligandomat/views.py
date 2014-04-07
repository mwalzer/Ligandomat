import os
import hashlib

from mako.template import Template

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
from tools.XlsDictAdapter import XlsDictReader, XlsDictWriter
from .forms import DataQuery
from pyramid.httpexceptions import HTTPFound
from .models import *

from run_list_handling import *

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
    
# Download Query
@view_config(route_name='data_access', match_param="action=ligandomat_output.xls", renderer='ligandomat:templates/output/table_all_infos.mako', permission='view')
def download(request):
    if 'download_xls' in request.params:
        filename = authenticated_userid(request) + '.xls'
        response = FileResponse(filename, request=request, content_type='application/msexcel')
        return response


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

    # Connecting to the DB using MySQLdb
    conn = MySQLdb.connect(host=config.host, user=config.user, passwd=config.passwd, db=config.db,
                           port=config.port)
    c = conn.cursor(MySQLdb.cursors.DictCursor)


    if "search" in request.params:
        # Collecting input from Mako and creating query parts
        search_dict = ast.literal_eval(request.params.get("search"))
        query_dict = create_query(search_dict)
        # Use this if the sequence is a query criteria to speed up the query
        if 'sequence_input' in search_dict.keys():
            querystring = queries.search_by_sequence_first
            #TODO: Still need to implement!
            c.execute(querystring % (query_dict["peptide"], query_dict["spectrum_hit"], query_dict["ms_run"], query_dict["source"]))  #TODO: source_name, person, source_hla_typing
            result = c.fetchall()
            template = Template(filename='./ligandomat/templates/output/table_all_infos.mako')
            result = template.render(rows = result)
            return Response(result)


        if 'search_by_subsequence' in request.params:
            searchstring = pat
            querystring = queries.search_by_subsequence
            c.execute(querystring % (searchstring, pat_sorting_by))
            result = c.fetchall()
            header = ['sequence', 'sourcename', 'hlatype', 'min_RT', 'max_RT', 'min_MZ', 'max_MZ', 'min_Score', 'max_Score', 'min_Evalue', 'max_Evalue', 'runnames', 'antibody_set', 'organ', 'tissue', 'dignity']
            filename = authenticated_userid(request) + '.xls'
            if os.path.isfile(filename) == 1 :
                os.remove(filename)
            XlsDictWriter(filename, result, headerlist=header)
            #result = database_prediction(result)
            #result = annotate(result)
            template = Template(filename='./ligandomat/templates/output/table_all_infos.mako')
            result = template.render(rows = result)
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











