import os
import shutil
import re
import hashlib
from sqlalchemy import and_, distinct
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
from .forms import *
from .transformer import *
from pyramid.httpexceptions import HTTPFound
from sqlalchemy.exc import DBAPIError
from .models import *
	
from DBtransfer import *
from run_list_handling import *
from tools import reader, XlsDictAdapter
import tools
import parsing
import gc
import validation



# Upload --------------------------------------------------------------------------------------------------------------------
# http://docs.pylonsproject.org/projects/pyramid_cookbook/en/latest/forms/file_uploads.html
@view_config(route_name='upload', match_param='action=load_list', renderer='ligandomat:templates/wizard/load_list.mako', permission='edit')
def upload_page(request) :
	''' 
	appears after the upload button is clicked
	* a LogFile Instance is created for this upload
	* internData Objects for each row in .csv File
	* tmp_name is generated, represents unique name for Upload
	'''
	tmp_name = '_'
	form = Upload(request.POST) 
	session = request.session
	if 'form.submitted2' in request.params:		
		filename = request.params['the_input_file'].filename
		tmp_name = authenticated_userid(request) + "]*[" + (datetime.today().isoformat())
		tmp_name = tmp_name.replace('-','_')
		tmp_name = tmp_name.replace(':','_')
		tmp_name += "]*["
		tmp_name += filename
		
		tmps = getAllTmps(DBSession, LogFile)
		tmp_filenames = []
		for tmp in tmps :
			tmp_filenames.append(tmp.split(']*[')[2])
			
		used_file_name = tmp_name.split(']*[')[2]
		if used_file_name in tmp_filenames :
			corresponding_Log = getLogByFilename(DBSession, LogFile, used_file_name)
			if corresponding_Log.successful == 1 :
				session['fyi'] = 'You have already uploaded this file.'
				session['image'] = ''
				return HTTPFound(location = request.route_url('fyi'))
		
		
		user_id = getUserIdByName(DBSession, User, authenticated_userid(request))
		print '### user id = %s' %user_id
		log = LogFile(tmp_name, user_id)
		DBSession.add(log)
		request.session.invalidate()
		
		# get dict intern_data
		if filename.lower().endswith('.csv') :
			intern_data = reader.dictReaderFile(request.params['the_input_file'].file)
		elif filename.lower().endswith('.xlsx') or filename.endswith(".xls"):
			intern_data = XlsDictAdapter.XlsDictReader(request.params['the_input_file'].file.read())
		else :
			session['fyi'] = 'The data you want to upload should have the csv format or xlsx\\xls format.'
			session['image'] = ''
			return HTTPFound(location = request.route_url('fyi'))

		# fill DB table intern_data
		for i in range(0, len(intern_data) ) :
			#print '###### %s. row read #####' %i
			intern_data[i]['seq'] = intern_data[i].pop('Sequence')
			intern_data[i]['run'] = intern_data[i].pop('Spectrum File')
			intern_data[i]['timestamp'] = tmp_name
			intern_data[i]['rest'] = str(dict((k, v) for k,v in intern_data[i].iteritems() if k not in ['seq','run']))
			intern_data[i] = dict((k, v) for k,v in intern_data[i].iteritems() if k in ['seq','run','rest','timestamp'])
				
		start = 0
		end = 5000
		
		while True :
			if end > len(intern_data) :
				end = len(intern_data)
				InternData.__table__.insert().execute(intern_data[start:end])
				break
			InternData.__table__.insert().execute(intern_data[start:end])
			start = start + 5000
			end = end + 5000
		
		log = getCurrentLog(DBSession, LogFile, tmp_name)
		log.message += '*rows:%s ' %len(intern_data)
		return HTTPFound(location = request.route_url('upload', action='source', attach=tmp_name))
		
	return dict(form = form, attach = tmp_name, logged_in =  authenticated_userid(request))

# Upload - Source ----------------------------------------------------------------------------
@view_config(route_name='upload', match_param='action=source', renderer='ligandomat:templates/wizard/source.mako', permission='edit')
def upload_source_page(request) :
	''' 
	* General *
	Used to map sources to ms runs.
	After comitting a specific source for some runs the user returns to this view. Important information for this logic is stored in a session.
	* workflow *
	- after first time loading this view, the session is initialized
	- user has two opions :
		1) selecting a known source -> source_id will be added to corresponding rows in InternData
		2) creating new source -> SourceData Instance and SourceHLA for typings are generated
	- after comitting the last runs the Prep page will appear.
	'''
		
	# giving session cookie name
	session = request.session
	form = Source(request.POST) 
	tmp_name = request.matchdict.get('attach')
	form.setChoices()
	# init source at first time loaded
	if not 'init_source' in session :
		# basic setup
		session['init_source'] = 'yes' 
		session['in_action'] = 'none'   
		session['num_hla'] = 0

		run_object = getknown_runsAndrun_list(DBSession, MSData, InternData, tmp_name)
		known_runs = run_object[0]
		run_list = run_object[1]
		
		# fill InternData at the place, where the runs are known with the corresponding ms_run_id	

		users_rows = getUserRows(DBSession, InternData, tmp_name)
		for row in users_rows :
			if row.run in known_runs :
				ms_id = DBSession.query(MSData).filter(MSData.filename == row.run).first().ms_run_id
				hit = Hit(row.rest, tmp_name, row.seq,ms_id, authenticated_userid(request))
				DBSession.add(hit)
				
		log = getCurrentLog(DBSession, LogFile, tmp_name)
		
		for known_run in known_runs :
			log.message += '!kRun:%s ' %known_run
			rows_with_known_runs = DBSession.query(InternData).filter(and_(InternData.timestamp == tmp_name, InternData.run == known_run)).all()
			ms_run_id = DBSession.query(MSData).filter(MSData.filename == known_run).first().ms_run_id
			for rowKR in rows_with_known_runs :
				rowKR.mass_spec_id = ms_run_id
			
		# if there are unknown runs, usual meta date collection
		if len(run_list) == 0 :
			# correct version
			session.invalidate()
			users_rows = getUserRows(DBSession, InternData, tmp_name)
			log = getCurrentLog(DBSession, LogFile, tmp_name)
			log.successful = b'1'
			log.message += 'All Runs were known. Added Hits.'
			session['fyi'] = 'Thank you for adding some new Hits to our data base. We linked them to the coressponding known MS runs.'
			session['image'] = ''
			return HTTPFound(location = request.route_url('fyi'))
		else :
			session['run_list'] = compressList(run_list)

		print 'init_source'
		return dict(form = form, 
					run_list = decompressList(session['run_list']), 
					num_hla = session['num_hla'], 
					list_hlas = getHLAAlleles(DBSession, HLAAllele),
					in_action = session['in_action'])
	else :
		# ADD and DELETE HLA #
		if 'button_add_hla' in request.params :
			hla = request.params['select_hla'] #string!
			allele = request.params['hla_allele']
			validated_typing = validation.correctTyping(allele)
			if not validated_typing[0] :
				session['fyi'] = 'Please enter a valid form of HLA Addition. They must be conform to the common Nomenclature which is [:III:II:IIL]. ("I" stands for a digit and "L" for a letter). For further information please see Help.'
				session['image'] = 'stop'
				return HTTPFound(location = request.route_url('fyi'))	 
			else :
				# validate HLAs : exaxt same HLA
				if (hla, validated_typing[1]) in form.HLAs :
					session['fyi'] = 'You submittied twice the HLA %s:%s' %(hla, validated_typing[1])
					session['image'] = 'stop'
					return HTTPFound(location = request.route_url('fyi'))	
				allele = hla[0]
				same = []
				for tuple in form.HLAs :
					a = tuple[0][0:2] #first 2 letters
					if a == allele :
						same.append(tuple[0] + ':' + tuple[1])
						if len(same) == 2 :
							session['fyi'] = 'Wow, are you sure, you have a case of Trisomy? %s , %s , %s' %(same[0], same[1], hla + ':' + validated_typing[1])
							session['image'] = 'stop'
							return HTTPFound(location = request.route_url('fyi'))	
				
				session['num_hla'] += 1
				form.HLAs.append((hla, validated_typing[1]))

		if 'button_delete_hla' in request.params :
			if session['num_hla'] > 0 :
				session['num_hla'] = session['num_hla'] -1
				form.HLAs.pop()

		# change modus
		if 'button_new_source' in request.params :
			session['in_action'] = 'add_source'
		if 'button_known_source' in request.params :
			session['in_action'] = 'source'
			
		if 'abort_upload' in request.params :
			log = getCurrentLog(DBSession, LogFile, tmp_name)
			log.message += '!abort at Source:'
			# remove new source / prep
			users_rows = getUserRows(DBSession, InternData, tmp_name)
			used_source_ids = []
			
			deleteUsersSources(DBSession, SourceData, tmp_name)
			deleteUsersTypings(DBSession, SourceHLA, tmp_name)
			'''
			for row in users_rows :
				if not row.source_id in used_source_ids and not row.source_id is None:
					used_source_ids.append(row.source_id)
					hlas = DBSession.query(SourceHLA).filter(SourceHLA.source_source_id == row.source_id).all()
					for typing in hlas :
						DBSession.delete(typing)
				
					s = DBSession.query(SourceData).get(row.source_id)
					if s.timestamp == tmp_name :
						print '- delete source with Id : %s' %s.source_id
						DBSession.delete(s)
			'''

			deleteUsersRows(DBSession, InternData, tmp_name)
			log.message += '- abort complete!'
			return HTTPFound(location = request.route_url('Ligandomat'))
			
		# SUBMIT SOURCE #
		if 'button_submit' in request.params:
			if session['in_action'] == 'none' :
				session['fyi'] = 'Please select known or new source.'
				session['image'] = ''
				return HTTPFound(location = request.route_url('fyi'))
			source = dict()
			# if 'add_source'
			if session['in_action'] == 'add_source' :
				source['celltype'] = request.params['cell_type']
				source['comment'] = request.params['comment1']
				source['num_hla'] = session['num_hla'] 
				for i in range(0, len(form.HLAs)) :
					source_hla_name = 'hla' + str(i)
					source[source_hla_name] = form.HLAs[i] # tuple of 2 u'strings: (selected hla name, text allele)
			
				source['new_source'] = request.params['new_source']
				source['organ'] = request.params['organ']
				source['organism'] = request.params['organism']
				source['tissue'] = request.params['tissue']
				source['dignity'] = request.params['dignity']  
				
			# validation
				valid = validation.validSource(source) 
				if not valid[0] :
					return Response(valid[1])
				db_source = SourceData(tmp_name, source)
				
				DBSession.add(db_source)
				log = getCurrentLog(DBSession, LogFile, tmp_name)
				log.message += '*s:%s ' %db_source.source_id
				print ('NEW source %s submitted' %db_source.name)
					
			# if 'source'
			if session['in_action'] == 'source' :			
				db_source = getSourceFromCollectInt(DBSession, SourceData, int(request.params['known_sources']))		
				print ('OLD source submitted')

			### adding source to checked runs -> remove them out of run_list ###
			used_runs = usedRuns(session['run_list'], request.params) #compressed
			
			intern_data_to_fill = rowsToFill(DBSession, InternData, tmp_name, used_runs)
			print 'FILL IN ROWS : view %s' %intern_data_to_fill
			
			# add HLAs to internData 
			for row in intern_data_to_fill :
				row.source_id = db_source.source_id
				row.hla_typing = str(form.HLAs)
				
			### reset ###
			session['in_action'] = 'none'

			#adding HLAs
			for hla in form.HLAs :
				typing = SourceHLA(tmp_name, db_source.source_id, hla[0], hla[1])
				DBSession.add(typing)
				
			for i in range(len(form.HLAs)):
				form.HLAs.pop()
			session['num_hla'] = 0
			session['run_list'] = throughOutUsedRuns(session['run_list'], used_runs)
			
			### start next ###
			if (len(session['run_list']) == 0) :
				session.invalidate()
				return HTTPFound(location = request.route_url('upload', action='prep', attach=tmp_name))
			else :
				print ('still runs %s in run_list' %len(session['run_list']))
				return dict(form = form, 
							run_list = decompressList(session['run_list']), 
							num_hla = session['num_hla'],
							list_hlas = getHLAAlleles(DBSession, HLAAllele),
							in_action = session['in_action'],)
		return dict(form = form, 
					run_list = decompressList(session['run_list']), 
					num_hla = session['num_hla'],
					list_hlas = getHLAAlleles(DBSession, HLAAllele),
					in_action = session['in_action'],)

 
# Upload - Prep ----------------------------------------------------------------------------------
@view_config(route_name='upload', match_param='action=prep', renderer='ligandomat:templates/wizard/prep.mako', permission='edit')
def upload_prep_page(request) :
	''' 
	* General *
	Used to map preperations to ms runs.
	* workflow *
	- after first time loading this view, the session is initialized
	- user has two opions :
		1) selecting a known prep -> prep_id will be added to corresponding rows in InternData
		2) creating new prep -> PrepData Instance is generated an
	- after comitting the last runs the MS page will appear.
	'''
	
	# giving session cookie name
	session = request.session
	form = Prep(request.POST) 
	form.setChoices(authenticated_userid(request))
	tmp_name = request.matchdict.get('attach')
	# init source at first time loaded
	if not 'init_prep' in session :
		# basic setup
		session['init_prep'] = 'yes' 
		session['in_action'] = 'none'   
		run_list = getknown_runsAndrun_list(DBSession, MSData, InternData, tmp_name)[1]
		session['run_list'] = compressList(run_list)
		
		print 'init_prep'
		return dict(form = form, 
					run_list = decompressList(session['run_list']), 
					in_action = session['in_action'])
	else :
		# change modus
		if 'button_new_prep' in request.params :
			session['in_action'] = 'add_prep'
		if 'button_known_prep' in request.params :
			session['in_action'] = 'prep'

		if 'abort_upload' in request.params :
			log = getCurrentLog(DBSession, LogFile, tmp_name)
			log.message += '!abort at Prep:'
			# remove new source / prep	
			
			deleteUsersPreps(DBSession, PrepData, tmp_name)			
			deleteUsersSources(DBSession, SourceData, tmp_name)
			deleteUsersTypings(DBSession, SourceHLA, tmp_name)
			deleteUsersRows(DBSession, InternData, tmp_name)
			
			log.message += '- abort complete!'
			return HTTPFound(location = request.route_url('Ligandomat'))
		# SUBMIT PREP #
		if 'button_submitted_prep' in request.params :
			if session['in_action'] == 'none' :
				session['fyi'] = 'Please select known or new prep'
				session['image'] = 'stop'
				return HTTPFound(location = request.route_url('fyi'))	
			prep = dict()
			# if 'add_prep'
			if session['in_action'] == 'add_prep' :
				prep['comment'] = request.params['comment2']
				prep['made_by'] = request.params['made_by']
				prep['sample_mass'] = request.params['sample_mass']
				prep['antibody'] = request.params['antibody']
				prep['antibody_mass'] = request.params['antibody_mass']
				if 'magna' in request.params :
					prep['magna'] = 1
				else :
					prep['magna'] = 0
				
				# validation
				valid = validation.validPrep(prep) 
				if not valid[0] :
					return Response(valid[1])
				
				used_run = usedRuns(session['run_list'], request.params)[0]
				db_prep = PrepData(tmp_name, prep)
				DBSession.add(db_prep)
				log = getCurrentLog(DBSession, LogFile, tmp_name)
				log.message += '*p:%s ' %db_prep.mhcpraep_id
				print ('NEW prep %s submitted' %db_prep.mhcpraep_id)
				
			# if 'prep'
			if session['in_action'] == 'prep' :		
				prep['known_prep'] = request.params['known_prep']
				index_of_kp = int(prep['known_prep'])
				id_of_clicked = getAllKnownPrep_Id(DBSession, PrepData)[index_of_kp]
				db_prep = DBSession.query(PrepData).filter(PrepData.mhcpraep_id == id_of_clicked).first()		
				print ('OLD prep submitted')

			### adding source to checked runs -> remove them out of run_list ###
			used_runs = usedRuns(session['run_list'], request.params)
			intern_data_to_fill = rowsToFill(DBSession, InternData, tmp_name, used_runs)
			
			# add to internData 
			for row in intern_data_to_fill :
				row.prep_id = db_prep.mhcpraep_id
				
			### reset and start next###
			session['in_action'] = 'none'
			session['run_list'] = throughOutUsedRuns(session['run_list'], used_runs)
			if (len(session['run_list']) == 0) :
				session.invalidate()
				return HTTPFound(location = request.route_url('upload', action='mass_spec', attach=tmp_name))
			else :
				print ('still runs %s in run_list' %len(session['run_list']))
				return dict(form = form, 
							run_list = decompressList(session['run_list']), 
							in_action = session['in_action'],)
		return dict(form = form, 
					run_list = decompressList(session['run_list']), 
					in_action = session['in_action'],)	


# Upload - Massspec ----------------------------------------------------------------------------------
@view_config(route_name='upload', match_param='action=mass_spec', renderer='ligandomat:templates/wizard/mass_spec.mako', permission='edit')
def upload_mass_spec_page(request) :
	''' 
	* General *
	Used to create ms_runs with specific information
	* workflow *
	- runs with same information(date, made_by, etc) can be added by the user at once. Intern for each ms_file there a MassSpec_Data will be created.
	- Hits from known runs are already added in the function upload_source_page
	- after submitting the overview is presented
	'''

	session = request.session
	form = Mass_spec(request.POST) 
	
	tmp_name = request.matchdict.get('attach')
	# if session becomes to big: request.session.invalidate() -> source lost and generate new
	if not 'init_mass_spec' in session :
		session['init_mass_spec'] = 'yes'
		
		run_object = getknown_runsAndrun_list(DBSession, MSData, InternData, tmp_name)
		
		session['run_list'] = compressList(run_object[1])
		Mass_spec.setChoices(form, decompressList(session['run_list'])[0], authenticated_userid(request)) 
		print 'init_mass_spec'
		return dict(form = form, 
					run_list = decompressList(session['run_list']), ) 
	else :
		Mass_spec.setChoices(form, decompressList(session['run_list'])[0], authenticated_userid(request)) 
		# SUBMIT MASS SPEC #
		if 'abort_upload' in request.params :
			log = getCurrentLog(DBSession, LogFile, tmp_name)
			log.message += '!abort at MS:'
			# remove new source / prep
			deleteUsersMS(DBSession, MSData, tmp_name)
			deleteUsersPreps(DBSession, PrepData, tmp_name)			
			deleteUsersSources(DBSession, SourceData, tmp_name)
			deleteUsersTypings(DBSession, SourceHLA, tmp_name)

			deleteUsersRows(DBSession, InternData, tmp_name)
			log.message += '- abort complete!'
			return HTTPFound(location = request.route_url('Ligandomat'))
			
		if 'button_submitted_mass_spec' in request.params :
			mass_spec = dict()
			#db_mass_spec
			mass_spec['comment'] = request.params['comment3']
			mass_spec['made_by'] = request.params['made_by']
			mass_spec['run_date'] = request.params['run_date']
			mass_spec['sample_share'] = request.params['sample_share']
			mass_spec['method'] = request.params['method']
			mass_spec['modification'] = request.params['modification']
			
			# validation
			valid = validation.validMS(mass_spec) 
			if not valid[0] :
				return Response(valid[1])
			mass_spec['run_date'] = parsing.makeADate(request.params['run_date'])
			
			# reset run_list
			used_runs = usedRuns(session['run_list'], request.params)#not compressed
			users_rows = getUserRows(DBSession, InternData, tmp_name)
			for used_run in used_runs :
				for row in users_rows :
					if row.run == used_run :
						source_id = row.source_id
						prep_id = row.prep_id
						break
				db_mass_spec = MSData(tmp_name, mass_spec, used_run, source_id, prep_id)
				DBSession.add(db_mass_spec)
				intern_data_to_fill = rowsToFill(DBSession, InternData, tmp_name, [used_run])
				# add to internData 
				for intern_row in intern_data_to_fill :
					intern_row.mass_spec_id = db_mass_spec.ms_run_id		
				
			### reset and start next ###
			session['run_list'] = throughOutUsedRuns(session['run_list'], used_runs)
			if not session['run_list'] == [] :
				Mass_spec.setChoices(form, decompressList(session['run_list'])[0], authenticated_userid(request)) 
			if (len(session['run_list']) == 0) :
				session.invalidate()
				return HTTPFound(location = request.route_url('upload', action='overview', attach=tmp_name))
			else :
				print ('still runs %s in run_list' %len(session['run_list']))
				return dict(form = form, 
							run_list = decompressList(session['run_list']), )
		return dict(form = form, 
					run_list = decompressList(session['run_list']), )	

# Upload - Overview ----------------------------------------------------------------------------------
@view_config(route_name='upload', match_param='action=overview', renderer='ligandomat:templates/wizard/overview.mako', permission='edit')
def upload_overview_page(request) :
	''' 
	This page shows all the selected information by the user.
	The user can commit the upload -> information stored permernently in DB, InternData Objects are being removed
	If the upload is rejected, all new Objects are deleted by tmp_name from InternData.
	'''
	tmp_name = request.matchdict.get('attach')
	users_rows = getUserRows(DBSession, InternData, tmp_name)
	
	table = []
	ms_run_ids = []
	
	for row in users_rows :
		if not row.mass_spec_id in ms_run_ids :
			ms_run_ids.append(row.mass_spec_id)
	
	for ms_id in ms_run_ids :
		
		ms = DBSession.query(MSData).get(ms_id)
		p = DBSession.query(PrepData).get(ms.mhcpraep_mhcpraep_id)
		s = DBSession.query(SourceData).get(ms.source_source_id)
		typings = getTypingsBySourceId(DBSession, SourceHLA, s.source_id)
		
		if len(typings) > 0 :
			d = dict()
			d['filename'] = ms.filename
			d['antibody'] = p.antibody_set
			d['source_name'] = s.name
			typing = ''
			for type in typings :
				typing += DBSession.query(HLAAllele).get(type.hlaallele_hlaallele_id).gene_group
				typing += ' /'

			d['allele'] = typing
			table.append(d)
		else :
			d = dict()
			d['filename'] = ms.filename
			d['antibody'] = p.antibody_set
			d['source_name'] = s.name
			d['allele'] = 'n/a'
			table.append(d)
			
	if 'reject_upload' in request.params :
		print '###REJECTED UPLOAD###'
		log = getCurrentLog(DBSession, LogFile, tmp_name)
		log.message += '!start rejection:'
		# remove new source / prep
		users_rows = getUserRows(DBSession, InternData, tmp_name)
		usedMSIds = []
		for row in users_rows :					
			if not row.mass_spec_id in usedMSIds :
				usedMSIds.append(row.mass_spec_id)
				ms = DBSession.query(MSData).get(row.mass_spec_id)
				if ms.timestamp == tmp_name :
					print '- delete MS with Id : %s' %ms.ms_run_id
					DBSession.delete(ms)
					
		usedPrepIds = []
		for row in users_rows :
			if not row.prep_id in usedPrepIds :
				usedPrepIds.append(row.prep_id)
				p = DBSession.query(PrepData).get(row.prep_id)
				if p.timestamp == tmp_name :
					print '- delete prep with Id : %s' %p.mhcpraep_id
					DBSession.delete(p)	
					
		used_source_ids = []
		for row in users_rows :
			if not row.source_id in used_source_ids :
				used_source_ids.append(row.source_id)
				hlas = DBSession.query(SourceHLA).filter(SourceHLA.source_source_id == row.source_id).all()
				for typing in hlas :
					DBSession.delete(typing)
			
				s = DBSession.query(SourceData).get(row.source_id)
				if s.timestamp == tmp_name :
					print '- delete source with Id : %s' %s.source_id
					DBSession.delete(s)

		deleteUsersRows(DBSession, InternData, tmp_name)
		log.message += '!rejected'
		return HTTPFound(location = request.route_url('Ligandomat'))

	if 'submit_upload' in request.params:
		print '###SUBMITTED UPLOAD###'
		# adding hits!
		users_rows = getUserRows(DBSession, InternData, tmp_name)
		for row in users_rows :
			hit = Hit(row.rest, tmp_name, row.seq, row.mass_spec_id, authenticated_userid(request))
			DBSession.add(hit)
		
		deleteUsersRows(DBSession, InternData, tmp_name)
		log = getCurrentLog(DBSession, LogFile, tmp_name)
		log.successful = b'1'
		log.message += '!submitted'
		return HTTPFound(location = request.route_url('statistics'))
		
	return dict(tmp_name = tmp_name, table = table)
				
# Wizard - Help ---------------------------------------------------------------------------------------------------------
@view_config(route_name='wizard_help', renderer='ligandomat:templates/wizard/help.mako', permission='view')
def wizard_help_page(request) :
	return {}


