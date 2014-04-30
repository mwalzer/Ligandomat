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
from ligandomat.tools import XlsDictAdapter
from .forms import DataQuery
from pyramid.httpexceptions import HTTPFound
from .models import *

from run_list_handling import *
from pyramid.response import FileResponse

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
        querystring = queries.search_query_new + create_query(search_dict)

        c.execute("SET tmp_table_size = 4096000")
        c.execute(querystring)
        result = c.fetchall()

        # Write ouput
        header = ['sequence', 'sourcename', 'hlatype', 'minRT', 'maxRT', 'minMZ', 'maxMZ', 'minScore', 'maxScore', 'minE', 'maxE', 'runnames', 'antibody_set', 'organ', 'tissue', 'dignity']
        filename = authenticated_userid(request) + '.xls'
        if os.path.isfile(filename) == 1:
            os.remove(filename)
        XlsDictAdapter.XlsDictWriter(filename, result, headerlist=header)

        template = Template(filename='./ligandomat/templates/output/table_all_infos.mako')
        result = template.render(rows = result)
        return Response(result)

    if "search_run_name_name" in request.params:
        if "peptide_count" not in request.params:
            querystring = queries.query_run_name_info % (request.params.get("search_run_name_name"))
            c.execute(querystring)
            result = c.fetchall()

            # Write ouput
            header = ['filename', 'name', 'organ', 'dignity', 'tissue', 'date', 'sample_mass', 'antibody_mass', 'antibody_set', 'hlatype']
            filename = authenticated_userid(request) + '.xls'
            if os.path.isfile(filename) == 1:
                os.remove(filename)
            XlsDictAdapter.XlsDictWriter(filename, result, headerlist=header)

            template = Template(filename='./ligandomat/templates/output/table_run_information.mako')
            result = template.render(rows = result)
            return Response(result)
        else:
            search_dict = ast.literal_eval(request.params.get("search_run_name_name"))
            querystring = queries.query_run_name_info_peptides % (search_dict["ionscore_input"], search_dict["e_value_input"]
                                                                  , search_dict["q_value_input"], search_dict["run_name"])
            c.execute("SET tmp_table_size = 4096000")
            c.execute(querystring)
            result = c.fetchall()

            # Write output
            header = ['filename', 'name', 'organ', 'dignity', 'tissue', 'date', 'sample_mass', 'antibody_mass', 'antibody_set', 'hlatype', 'number_of_peptides']
            filename = authenticated_userid(request) + '.xls'
            if os.path.isfile(filename) == 1:
                os.remove(filename)
            XlsDictAdapter.XlsDictWriter(filename, result, headerlist=header)

            template = Template(filename='./ligandomat/templates/output/table_run_information_peptides.mako')
            result = template.render(rows = result)
            return Response(result)

    if "search_source_name" in request.params:
        if "peptide_count" not in request.params:
            querystring = queries.query_source_info % (request.params.get("search_source_name"))
            c.execute(querystring)
            result = c.fetchall()
            # Write output
            header = ['name', 'organ', 'dignity', 'tissue', 'hlatype']
            filename = authenticated_userid(request) + '.xls'
            if os.path.isfile(filename) == 1:
                os.remove(filename)
            XlsDictAdapter.XlsDictWriter(filename, result, headerlist=header)

            template = Template(filename='./ligandomat/templates/output/table_source_information.mako')
            result = template.render(rows = result)
            return Response(result)
        else:
            search_dict = ast.literal_eval(request.params.get("search_source_name"))
            querystring = queries.query_source_info_peptides % (search_dict["ionscore_input"], search_dict["e_value_input"],
                                                                search_dict["q_value_input"], search_dict["source"])
            #querystring = queries.query_source_info_peptides % (request.params.get("search_source_name"))
            c.execute("SET tmp_table_size = 4096000")
            c.execute(querystring)
            result = c.fetchall()

            # Write ouput
            header = ['name', 'organ', 'dignity', 'tissue', 'hlatype', 'number_of_peptides']
            filename = authenticated_userid(request) + '.xls'
            if os.path.isfile(filename) == 1:
                os.remove(filename)
            XlsDictAdapter.XlsDictWriter(filename, result, headerlist=header)

            template = Template(filename='./ligandomat/templates/output/table_source_information_peptides.mako')
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











