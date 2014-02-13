# -*- coding: utf-8 -*-

from sqlalchemy import distinct
from wtforms import Form, Label, TextField, BooleanField, TextAreaField, validators, HiddenField, SelectField, SelectMultipleField, FieldList, DateField, IntegerField, FileField
from wtforms.widgets import Input
from .DBtransfer import Connection
from .models import *

from wtforms.validators import *

# access_data form

class DataQuery(Form) :
	peptide_info = TextField('Peptide Info')
	peptide_pattern = TextField('Peptide Supertype', default='You personal PRR')
	
	source_detail = SelectField('Source detail', coerce=int)
	source_peptides = SelectField('Source peptides', coerce=int)

	def setChoices(self) :
		self.source_detail.choices = generateValues(getAllKnownSource_Name(DBSession, SourceData))
		self.source_peptides.choices= generateValues(getAllKnownSource_Name(DBSession, SourceData))



# wizard forms


class Upload(Form) :
	the_input_file = FileField('Input')

class Source(Form) :
	''' Form that collects meta data about the source 
	'''

	known_sources = SelectField('Known Source', coerce=int)

	new_source = TextField('New Source')
	organ = SelectField('Organ', coerce=int)
	organism = SelectField('Organism', coerce=int)
	tissue = SelectField('Tissue', coerce=int)
	dignity = SelectField('Dignity', coerce=int)
	cell_type = TextField('Celltype')
	comment1 = TextField('Comment')
	HLAs = []
	hla_allele = TextField('HLA allele')

	def setChoices(self) :
		self.known_sources.choices = generateValues(getAllKnownSource_Name(DBSession, SourceData))
		
		conn = Connection()
		source_types = conn.getType('source', ['organ', 'organism', 'tissue', 'dignity'])
		
		self.organ.choices = generateValues(source_types['organ'])
		self.organism.choices = generateValues(source_types['organism'])
		self.tissue.choices = generateValues(source_types['tissue'])
		self.dignity.choices = generateValues(source_types['dignity'])

class Prep(Form) :
	''' Form that collects meta data about the preperation 
	'''

	known_prep = SelectField('Known Prep', coerce=int) #db

	made_by = SelectField('Made by',  coerce=int, default = 5)
	sample_mass = IntegerField('Sample mass')
	antibody = SelectField('Antibody', coerce=int)
	antibody_mass = IntegerField('Antibody mass')
	magna = BooleanField('Magna')
	comment2 = TextField('Comment')

	
		
	# static init
	def setChoices(self, user_id) :
		self.known_prep.choices = generateValues(getAllKnownPrep_Name(DBSession, PrepData, SourceData, Person))
		self.made_by.choices = generateValues(getAllPerson_Name(DBSession, Person))
		self.made_by.data = getIntOfUserPerson(user_id)
		con = Connection()
		antis = con.getType('mhcpraep', ['antibody_set'])
		self.antibody.choices = generateValues(antis['antibody_set'])



def getIntOfUserPerson(user_name) :
	user = getUserByName(DBSession, User, user_name) 
	person = getPersonById(DBSession, Person, user.person_person_id)
	person_name = person.first_name + ' ' + person.last_name
	persons = getAllPerson_Name(DBSession, Person)
	for i in range(0, len(persons)) :
		if person_name == persons[i] :
			print 'found'
			return i
	return 0

class Mass_spec(Form) :
	''' Form that collects meta data about the MS run
	'''

	made_by = SelectField('Made by', coerce=int)
	run_date = TextField('Date of run')
	sample_share = TextField('Sample Share')
	comment3 = TextField('Comment')
	method = SelectField('Method of run', coerce=int)
	modification = SelectField('Modifications', coerce=int)
	
	def setChoices(self, run_name, user_name) :
		self.made_by.data = getIntOfUserPerson(user_name)
		if run_name[0:6].isdigit() :
			self.run_date.data = run_name[0:6]
		self.sample_share.data = "0"
		if '%' in run_name :
			p = run_name.split('%')[0][-3:]
			print '#########in with p = %s' %p
			if p.isdigit() :
				self.sample_share.data = p
			else :
				if p[1:].isdigit() :
					self.sample_share.data = p[1:]
				else :
					if p[2:].isdigit() :
						self.sample_share.data = p[2:]
			
		self.made_by.choices = generateValues(getAllPerson_Name(DBSession, Person))
		self.method.choices = generateValues(getAllMethod_Name(DBSession, Gradient))
		self.modification.choices = generateValues(getAllModification_Name(DBSession, Modification))
		


def generateValues(list) :
	''' generates the tuple values, needed as choices in SelectFields, given a list
	'''
	values = []
	i=0
	for item in list :
		new_item = (i, list[i])
		values.append(new_item)
		i = i + 1
	return values












