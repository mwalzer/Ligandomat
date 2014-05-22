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
@view_config(route_name='data_access', match_param="action=ligandomat_output.xls",
             renderer='ligandomat:templates/output/table_all_infos.mako', permission='view')
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
    conn = MySQLdb.connect(host=config.host, user=config.user, passwd=config.passwd,
                           port=config.port)
    c = conn.cursor(MySQLdb.cursors.DictCursor)
    c.execute("SET tmp_table_size = 16000000")

    # Search for peptide list
    if "search" in request.params:
        # Collecting input from Mako and creating query parts
        search_dict = ast.literal_eval(request.params.get("search"))
        querystring = queries.search_query_new

        # header for the output
        header = ['sequence', 'uniprot_accession', 'sourcename', 'hlatype', 'minRT', 'maxRT', 'minMZ', 'maxMZ',
                  'minScore', 'maxScore', 'minE', 'maxE', 'minQ', 'maxQ', 'runnames', 'antibody_set', 'organ', 'tissue',
                  'dignity']

        # including the prediction information into the query
        if "prediction_information" in search_dict.keys():
            if search_dict["prediction_information"] != "":
                # adding the HLA types to the SELECT statement using serious string manipulations
                querystring_select, querystring_rest = querystring.split("FROM")
                # all netmhc_3_4 alleles in the database
                net_mhc_3_4_alleles = ['A_01_01_affinity','A_01_01_score','A_02_01_affinity','A_02_01_score','A_02_02_affinity','A_02_02_score','A_02_03_affinity','A_02_03_score','A_02_06_affinity','A_02_06_score','A_02_11_affinity','A_02_11_score','A_02_12_affinity','A_02_12_score','A_02_16_affinity','A_02_16_score','A_02_17_affinity','A_02_17_score','A_02_19_affinity','A_02_19_score','A_02_50_affinity','A_02_50_score','A_03_01_affinity','A_03_01_score','A_11_01_affinity','A_11_01_score','A_23_01_affinity','A_23_01_score','A_24_02_affinity','A_24_02_score','A_24_03_affinity','A_24_03_score','A_25_01_affinity','A_25_01_score','A_26_01_affinity','A_26_01_score','A_26_02_affinity','A_26_02_score','A_26_03_affinity','A_26_03_score','A_29_02_affinity','A_29_02_score','A_30_01_affinity','A_30_01_score','A_30_02_affinity','A_30_02_score','A_31_01_affinity','A_31_01_score','A_32_01_affinity','A_32_01_score','A_32_07_affinity','A_32_07_score','A_32_15_affinity','A_32_15_score','A_33_01_affinity','A_33_01_score','A_66_01_affinity','A_66_01_score','A_68_01_affinity','A_68_01_score','A_68_02_affinity','A_68_02_score','A_68_23_affinity','A_68_23_score','A_69_01_affinity','A_69_01_score','A_80_01_affinity','A_80_01_score','B_07_02_affinity','B_07_02_score','B_08_01_affinity','B_08_01_score','B_08_02_affinity','B_08_02_score','B_08_03_affinity','B_08_03_score','B_14_02_affinity','B_14_02_score','B_15_01_affinity','B_15_01_score','B_15_02_affinity','B_15_02_score','B_15_03_affinity','B_15_03_score','B_15_09_affinity','B_15_09_score','B_15_17_affinity','B_15_17_score','B_18_01_affinity','B_18_01_score','B_27_05_affinity','B_27_05_score','B_27_20_affinity','B_27_20_score','B_35_01_affinity','B_35_01_score','B_35_03_affinity','B_35_03_score','B_38_01_affinity','B_38_01_score','B_39_01_affinity','B_39_01_score','B_40_01_affinity','B_40_01_score','B_40_02_affinity','B_40_02_score','B_40_13_affinity','B_40_13_score','B_42_01_affinity','B_42_01_score','B_44_02_affinity','B_44_02_score','B_44_03_affinity','B_44_03_score','B_45_01_affinity','B_45_01_score','B_46_01_affinity','B_46_01_score','B_48_01_affinity','B_48_01_score','B_51_01_affinity','B_51_01_score','B_53_01_affinity','B_53_01_score','B_54_01_affinity','B_54_01_score','B_57_01_affinity','B_57_01_score','B_58_01_affinity','B_58_01_score','B_73_01_affinity','B_73_01_score','B_83_01_affinity','B_83_01_score','C_03_03_affinity','C_03_03_score','C_04_01_affinity','C_04_01_score','C_05_01_affinity','C_05_01_score','C_06_02_affinity','C_06_02_score','C_07_01_affinity','C_07_01_score','C_07_02_affinity','C_07_02_score','C_08_02_affinity','C_08_02_score','C_12_03_affinity','C_12_03_score','C_14_02_affinity','C_14_02_score','C_15_02_affinity','C_15_02_score','E_01_01_affinity','E_01_01_score']
                # all netmhc_170414 alleles in the database
                syfpeithi_170414_alleles = ['A_01_01_affinity','A_01_01_score','A_02_01_affinity','A_02_01_score','A_03_01_affinity','A_03_01_score','A_11_01_affinity','A_11_01_score','A_24_02_affinity','A_24_02_score','A_26_01_affinity','A_26_01_score','A_31_01_affinity','A_31_01_score','A_32_01_affinity','A_32_01_score','A_33_03_affinity','A_33_03_score','A_68_01_affinity','A_68_01_score','B_07_02_affinity','B_07_02_score','B_08_01_affinity','B_08_01_score','B_13_02_affinity','B_13_02_score','B_14_02_affinity','B_14_02_score','B_15_01_affinity','B_15_01_score','B_15_10_affinity','B_15_10_score','B_15_16_affinity','B_15_16_score','B_18_01_affinity','B_18_01_score','B_27_05_affinity','B_27_05_score','B_27_09_affinity','B_27_09_score','B_35_01_affinity','B_35_01_score','B_37_01_affinity','B_37_01_score','B_38_01_affinity','B_38_01_score','B_39_01_affinity','B_39_01_score','B_39_02_affinity','B_39_02_score','B_40_01_affinity','B_40_01_score','B_40_02_affinity','B_40_02_score','B_41_01_affinity','B_41_01_score','B_44_02_affinity','B_44_02_score','B_45_01_affinity','B_45_01_score','B_47_01_affinity','B_47_01_score','B_49_01_affinity','B_49_01_score','B_50_01_affinity','B_50_01_score','B_51_01_affinity','B_51_01_score','B_53_01_affinity','B_53_01_score','B_57_01_affinity','B_57_01_score','B_58_01_affinity','B_58_01_score','B_58_02_affinity','B_58_02_score','C_04_01_affinity','C_04_01_score','C_05_01_affinity','C_05_01_score','C_06_01_affinity','C_06_01_score']

                # add selected alles to query
                for hla in search_dict['prediction_information'].split(";"):
                    hla_databank_format = hla.replace("*", "_").replace(":", "_")
                    #checking if allele is present in netmhc
                    if hla_databank_format+"_affinity" in syfpeithi_170414_alleles:
                        #rename the results to distinguish from which prediction method
                        querystring_select += ", Prediction_mapping.syfpeithi_170414.%s_affinity AS syfpeithi_170414_%s_affinity, Prediction_mapping.syfpeithi_170414.%s_score AS syfpeithi_170414_%s_score" % (hla_databank_format, hla_databank_format, hla_databank_format, hla_databank_format)
                        # adding alles to the header
                        header.append('syfpeithi_170414_%s_affinity'%hla_databank_format)
                        header.append('syfpeithi_170414_%s_score'%hla_databank_format)
                    # checking if allele is present in syfpeithi
                    if hla_databank_format+"_affinity" in net_mhc_3_4_alleles:
                        #rename the results to distinguish from which prediction method
                        querystring_select += ", Prediction_mapping.netMHC_3_4.%s_affinity AS netMHC_3_4_%s_affinity , Prediction_mapping.netMHC_3_4.%s_score AS netMHC_3_4_%s_score" % (hla_databank_format, hla_databank_format, hla_databank_format, hla_databank_format)
                        # adding alles to the header
                        header.append('netMHC_3_4_%s_affinity'%hla_databank_format)
                        header.append('netMHC_3_4_%s_score'%hla_databank_format)

                #querystring_select += "," + search_dict["prediction_information"].replace(";", ",").replace("*", "_").replace(":", "_")
                querystring = querystring_select + "\n FROM \n" + querystring_rest
                ## adding the innerjoin to the prediction database
                querystring += "INNER JOIN Prediction_mapping.netMHC_3_4 ON peptide_id = netMHC_3_4.peptide_peptide_id \nINNER JOIN Prediction_mapping.syfpeithi_170414 ON peptide_id = syfpeithi_170414.peptide_peptide_id\n"

        querystring += create_query(search_dict)

        print querystring
        c.execute(querystring)
        result = c.fetchall()

        # Write ouput

        filename = authenticated_userid(request) + '.xls'
        if os.path.isfile(filename) == 1:
            os.remove(filename)
        XlsDictAdapter.XlsDictWriter(filename, result, headerlist=header)

        template = Template(filename='./ligandomat/templates/output/table_all_infos.mako')
        result = template.render(rows=result)
        return Response(result)

    if "search_run_name_name" in request.params:
        if "peptide_count" not in request.params:
            querystring = queries.query_run_name_info % (request.params.get("search_run_name_name"))
            c.execute(querystring)
            result = c.fetchall()

            # Write ouput
            header = ['filename', 'name', 'organ', 'dignity', 'tissue', 'date', 'sample_mass', 'antibody_mass',
                      'antibody_set', 'hlatype']
            filename = authenticated_userid(request) + '.xls'
            if os.path.isfile(filename) == 1:
                os.remove(filename)
            XlsDictAdapter.XlsDictWriter(filename, result, headerlist=header)

            template = Template(filename='./ligandomat/templates/output/table_run_information.mako')
            result = template.render(rows=result)
            conn.close()
            return Response(result)
        else:
            search_dict = ast.literal_eval(request.params.get("search_run_name_name"))
            querystring = queries.query_run_name_info_peptides % (
                search_dict["ionscore_input"], search_dict["e_value_input"]
                , search_dict["q_value_input"], search_dict["run_name"])
            c.execute(querystring)
            result = c.fetchall()

            # Write output
            header = ['filename', 'name', 'organ', 'dignity', 'tissue', 'date', 'sample_mass', 'antibody_mass',
                      'antibody_set', 'hlatype', 'number_of_peptides']
            filename = authenticated_userid(request) + '.xls'
            if os.path.isfile(filename) == 1:
                os.remove(filename)
            XlsDictAdapter.XlsDictWriter(filename, result, headerlist=header)

            template = Template(filename='./ligandomat/templates/output/table_run_information_peptides.mako')
            result = template.render(rows=result)
            conn.close()
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
            result = template.render(rows=result)
            conn.close()
            return Response(result)
        else:
            search_dict = ast.literal_eval(request.params.get("search_source_name"))
            querystring = queries.query_source_info_peptides % (
                search_dict["ionscore_input"], search_dict["e_value_input"],
                search_dict["q_value_input"], search_dict["source"])
            #querystring = queries.query_source_info_peptides % (request.params.get("search_source_name"))
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
            conn.close()
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











