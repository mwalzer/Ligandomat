import os
import shutil
import re
import hashlib
from sqlalchemy import and_
from docutils.core import publish_parts

from sqlalchemy.ext.declarative import declarative_base
from datetime import *

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
	
	return dict(logged_in =  authenticated_userid(request))


# Login ----------------------------------------------------------------------------------------------------------
@view_config(route_name='login', renderer='ligandomat:templates/login.mako', permission='view')
def login(request):
	
	login_url = request.route_url('home')
	referrer = request.url
	if referrer == login_url:
		referrer = '/' # never use the login form itself as came_from
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
		uc = DBSession.query(User).filter(and_(User.username==login,User.password==password)).count()
		if(uc != 0):
			headers = remember(request, login)
			return HTTPFound(location = request.route_url('Ligandomat'), headers = headers)
		else:
			message = 'Failed login :('

	return dict(
		message = message,
		url = request.route_url('login'),
		came_from = came_from,
		logged_in =  authenticated_userid(request),
		login = login,
		password = password,
	)


# Logout ----------------------------------------------------------------------------------------------------------
@view_config( route_name='logout')
def logout(request):
	headers = forget(request)
	return HTTPFound(location = request.route_url('home'),
					 headers = headers)

# Ligandomat Start ---------------------------------------------------------------------------------------------------------------
@view_config(route_name='Ligandomat', renderer='ligandomat:templates/start.mako', permission='edit')
def choice_page(request) :
	return dict(
	logged_in = authenticated_userid(request)
	)



# DB Statistics ---------------------------------------------------------------------------------------------------------------------
@view_config(route_name='statistics', renderer='ligandomat:templates/output/statistics.mako', permission='view')
def statistics_page(request) :
	
	seqs = getAllPeptide_Sequence(DBSession, Peptide)

	return dict(logged_in = authenticated_userid(request),
				seqs = seqs, 
				nSeqs = len(seqs)
	)



# Access Data - Query---------------------------------------------------------------------------------------------------------------
@view_config(route_name='data_access', renderer='ligandomat:templates/output/data_query.mako', match_param='action=query', permission='view')
def access_data_query(request) :
	form = DataQuery(request.POST) 
	form.setChoices()
	session = request.session
	
	# PEPTIDE
	if 'button_peptide_all' in request.params :
		#session['action'] = 'peptide_all'	
		return HTTPFound(location = request.route_url('statistics'))
	
	if 'button_peptide_info' in request.params :
		session['action'] = 'peptide_info'	
		session['sequence'] = request.params['peptide_info']
		return HTTPFound(location = request.route_url('data_access', action='output_peptides'))
		
	if 'button_peptide_pattern' in request.params :
		session['action'] = 'peptide_pattern'
		session['pattern'] = request.params['peptide_pattern']
		
		return HTTPFound(location = request.route_url('data_access', action='output_peptides'))
		
	# SOURCE
	if 'button_source_detail' in request.params :
		session['action'] = 'source_detail'
		session['source'] = request.params['source_detail']
		return HTTPFound(location = request.route_url('data_access', action='output_sources'))
		
	if 'button_source_peptides' in request.params :
		session['action'] = 'source_peptides'
		session['source'] = request.params['source_peptides']
		return HTTPFound(location = request.route_url('data_access', action='output_peptides'))	
		
		
	if 'button_get_mining_csv' in request.params :
		con = Connection()
		name = 'mining' + datetime.today().isoformat()[0:10] + '.csv'
		con.getMiningTable(name)
		return HTTPFound(location = request.route_url('Ligandomat'))
		
		
	return dict(form = form, logged_in = authenticated_userid(request))



# Access Data - Output -----------------------PEPTIDES---------------------------------------------------------------------------------------
@view_config(route_name='data_access', renderer='ligandomat:templates/output/peptides.mako', match_param='action=output_peptides', permission='view')
def access_data_output_peptides(request) :
	session = request.session
	action = session['action']
	
	if action == 'peptide_all' :
		message = 'Here you can see all peptides from the data bank'
		peptides = DBSession.query(Peptide).all()
		table = presentData.fastPeptidesTable(DBSession, Peptide, Hit, SourceData, SourceHLA, HLAAllele, PrepData, MSData, Person, peptides) 
	if action == 'peptide_pattern' :
		pattern = session['pattern']
		peptides = patternRec.getPatternPeptides(pattern, DBSession, Peptide)
		message = 'Peptides that share the pattern %s' %pattern
		table = presentData.fastPeptidesTable(DBSession, Peptide, Hit, SourceData, SourceHLA, HLAAllele, PrepData, MSData, Person, peptides) 
		
	if action == 'peptide_info' :
		sequence = session['sequence']
		message = 'Information about the peptide %s' %sequence
		peptide = getPeptideBySeq(DBSession, Peptide, sequence)
		if peptide is None :
			return Response('Sorry, this peptide could not be found in our data bank :(')
		table = presentData.smallPeptidesTable(DBSession, Peptide, Hit, SourceData, SourceHLA, HLAAllele, PrepData, MSData, Person, [peptide])
		

	if action == 'source_peptides' :
		source = getSourceFromCollectInt(DBSession, SourceData, int(session['source']))
		message = "Peptides of source %s :" %source.name
		#TODO
		ms_runs = DBSession.query(MSData.ms_run_id).filter(MSData.source_source_id == source.source_id).all()
		hits = DBSession.query(Hit.peptide_peptide_id).filter(Hit.ms_run_ms_run_id in ms_runs).all()
		print hits
		return Response("bla")
		peptides = DBSession.query(Peptide).get(Peptide.peptide_id in hits)
		table = presentData.smallPeptidesTable(DBSession, Peptide, Hit, SourceData, SourceHLA, HLAAllele, PrepData, MSData, Person, peptides)
		
		return dict(logged_in = authenticated_userid(request), 
				message = message, 
				table = table)

	#session.invalidate()
	return dict(logged_in = authenticated_userid(request), 
				message = message, 
				table = table)
			


# Access Data - Output -----------------------SOURCE---------------------------------------------------------------------------------------
@view_config(route_name='data_access', renderer='ligandomat:templates/output/sources.mako', match_param='action=output_sources', permission='view')
def access_data_output_source(request) :
	session = request.session
	action = session['action']
	
	if action == 'source_detail' :
		source = getSourceFromCollectInt(DBSession, SourceData, int(session['source']))
		message = 'Information about the requested source %s' %source.name
		if 'button_change_source' in request.params :
			session['fyi'] = 'One job... Only one job...'
			session['image'] = 'onejob'
			return HTTPFound(location = request.route_url('fyi'))
		return dict(logged_in = authenticated_userid(request), 
					message = message,
					table = SourceData.stringIt(source))
	
	


# Forbidden View
@forbidden_view_config()
def unallowed(request) :
	return Response("[Forbidden_view_Error] You are not allowed to enter this page. User currently logged in: %s " % authenticated_userid(request) )
	
# For your Information	
@view_config(route_name='fyi', renderer='ligandomat:templates/fyi.mako', permission='view')
def fyi(request) :
	message = request.session['fyi']
	image = request.session['image'] 
	return dict(logged_in = authenticated_userid(request), message = message, image = image)











