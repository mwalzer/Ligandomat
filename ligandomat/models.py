from sqlalchemy import (
	Column,
	Integer,
	Float,
	Unicode,
	String,
	Date,
	)
	
from sqlalchemy.dialects.mysql import (
        BIGINT, BINARY, BIT, BLOB, BOOLEAN, CHAR, DATE, 
        DATETIME, DECIMAL, DECIMAL, DOUBLE, ENUM, FLOAT, INTEGER, 
        LONGBLOB, LONGTEXT, MEDIUMBLOB, MEDIUMINT, MEDIUMTEXT, NCHAR, 
        NUMERIC, NVARCHAR, REAL, SET, SMALLINT, TEXT, TIME, TIMESTAMP, 
        TINYBLOB, TINYINT, TINYTEXT, VARBINARY, VARCHAR, YEAR
)

from datetime import *
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
	scoped_session,
	sessionmaker,
	)

from zope.sqlalchemy import ZopeTransactionExtension

from pyramid.security import (
	Allow,
	Everyone,
	)
	
from ast import *
import parsing
import transformer
from DBtransfer import *
from sqlalchemy import and_
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

from DBtransfer import *


class HLAAllele(Base) :
	__tablename__ = 'hlaallele'
	
	hlaallele_id = Column(INTEGER, primary_key=True)
	gene_group = Column(TINYTEXT)
	
	
class SourceData(Base):
	''' equivalent to the table "source" in DB
	'''
	__tablename__ = 'source'	

	source_id = Column(INTEGER, primary_key=True)
	name = Column(VARCHAR(50))
	comment = Column(TEXT)
	timestamp = Column(CHAR(255))
	celltype = Column(VARCHAR(255))
	
	organ = Column(String(25))
	organism = Column(String(25))
	tissue = Column(String(25))
	dignity = Column(String(25))
	
	def __init__(self, tmp_name, source) :
		self.name = source['new_source']
		if source['comment'] != '' :
			self.comment = source['comment']
		self.timestamp = tmp_name
		if source['celltype'] != '' :
			self.celltype = source['celltype']
		self.adaptWizardToDB(source)
		
	def adaptWizardToDB(self, source) :
		con = Connection()
		source_types = con.getType('source', ['organ', 'organism', 'tissue', 'dignity'])
		index = int(source['organ'])
		self.organ = source_types['organ'][index]
		index = int(source['organism'])
		self.organism = source_types['organism'][index]
		index = int(source['tissue'])
		self.tissue = source_types['tissue'][index]
		index = int(source['dignity'])
		self.dignity = source_types['dignity'][index]

	def stringIt(self):
		l = []
		l.append('Source = %s' %str(self.name))
		
		all_typings = DBSession.query(SourceHLA)#.filter(SourceHLA.source_source_id == self.source_id).all()
		typings = []
		for t in all_typings :
			if t.source_source_id == self.source_id:
				typings.append(t)

		hlas = 'HLAs = '
		for typ in typings :
			allele = DBSession.query(HLAAllele).filter(HLAAllele.hlaallele_id == typ.hlaallele_hlaallele_id).first()
			hlas += allele.gene_group
			if not typ.specific_protein is None :
				hlas += ':'
				hlas += str(typ.specific_protein)
			if not typ.dna_coding is None :
				hlas += ':'
				hlas += str(typ.dna_coding)
			if not typ.dna_noncoding is None :
				hlas += ':'
				hlas += str(typ.dna_noncoding)
			if not typ.expression_suffix is None :
				hlas += str(typ.expression_suffix)
			hlas += ' / '
		#XXX
		l.append(hlas)
		l.append('Organ = %s' %str(self.organ))
		l.append('Organism = %s' %str(self.organism))
		l.append('Tissue = %s' %str(self.tissue))
		l.append('Dignity = %s' %str(self.dignity))
		l.append(stringItDBEntryNullable(self.celltype, 'Celltype'))
		l.append(stringItDBEntryNullable(self.comment, 'Comment'))
		return l

def stringItDBEntryNullable(entry, string) :
	if entry is None :
		return ('%s = None' %string)
	else :
		return ('%s = %s') %(string, entry)

class SourceHLA(Base) :
	''' equivalent to source_hlatyping in DB
	foreach entry by the user, a new object is created.
	they are validated and commited in "overview" after user submits upload
	'''
	__tablename__ = 'source_hlatyping'

	hlaallele_hlaallele_id = Column(INTEGER, primary_key=True)
	source_source_id = Column(INTEGER, primary_key=True)
	
	timestamp = Column(CHAR(255))
	
	specific_protein = Column(SMALLINT(6))
	dna_coding = Column(TINYINT(4))
	dna_noncoding = Column(TINYINT(4))
	expression_suffix = Column(VARCHAR(3))
	
	def __init__(self, tmp_name, source_id, hlaallele, hlatext):
		allele = DBSession.query(HLAAllele).filter(HLAAllele.gene_group == hlaallele).first()
		self.hlaallele_hlaallele_id = allele.hlaallele_id
		self.source_source_id = source_id
		self.timestamp = tmp_name
		if len(hlatext) > 0 :
			typing = hlatext.split(':')
			for i in range(0, len(typing)) :
				if i == 0 :
					self.specific_protein = int(typing[0])
				if i == 1 :
					self.dna_coding = int(typing[1])
				if i == 2 :
					self.dna_noncoding = int(typing[2][0:2])
					if len(typing[2]) == 3 :
						self.expression_suffix = typing[2][2:]
	
class PrepData(Base) :
	''' equivalent to "mhcpraep" in DB
	has foreign key to source
	'''
	__tablename__ = 'mhcpraep'
	
	mhcpraep_id = Column(INTEGER, primary_key=True, autoincrement=True)
	
	person_person_id = Column(INTEGER)

	sample_mass = Column(DOUBLE)
	sample_volume = Column(DOUBLE)
	antibody_set = Column(String(255))	
	antibody_mass	= Column(DOUBLE) 
	magna = Column(TINYINT(1))
	comment	= Column(TEXT)
	timestamp = Column(CHAR(255))

	
	def __init__(self, tmp_name, prep) :
		if ('g' in prep['sample_mass']) :
			self.sample_mass = parsing.getMass_g(prep['sample_mass'])
		if ('ml' in prep['sample_mass']) :
			self.sample_volume = parsing.getVolume_ml(prep['sample_mass'])
			
		index = int(prep['antibody'])
		con = Connection()
		ab_types =con.getType('mhcpraep', ['antibody_set'])['antibody_set']
		self.antibody_set = ab_types[index]
		
		if not (prep['antibody_mass'] == '' or prep['antibody_mass'] == 0) :
			self.antibody_mass = float(prep['antibody_mass'])
		self.magna = prep['magna']
		if prep['comment'] != '' :
			self.comment = prep['comment']
		self.timestamp = tmp_name
		self.person_person_id = getPersonIdFromCollectInt(DBSession, Person, int(prep['made_by']))
		
	def stringIt(self) :
		l = []
		
		l.append('Person = %s'% getPersonById_Name(DBSession, Person, self.person_person_id))
		if not self.sample_mass is None :
			l.append('Sample Mass = %s g' %str(self.sample_mass)[0:4])
		else :
			l.append('Sample Mass = n/a')
		l.append('Antibody = %s' %str(self.antibody_set))
		
		if not self.antibody_mass is None :
			l.append('Antibody Mass = %s mg' %str(self.antibody_mass)[0:4])
		else :
			l.append('Antibody Mass = n/a')
		if int(self.magna) == 0 :
			l.append('Magna = False')
		else :
			l.append('Magna = True')
		l.append(stringItDBEntryNullable(self.comment, 'Comment'))
		return l

class MSData(Base) :
	''' equivalent to ms_run in DB
	for each run, that needs to be check while wizarding a new object is created
	corresponding to filename.
	'''
	__tablename__ = 'ms_run'
	
	ms_run_id = Column(Integer, primary_key=True, autoincrement=True)
	filename = Column(String(255))
	date = Column(Date)
	used_share = Column(Float)
	comment = Column(String(255))
	timestamp = Column(String(255))
	
	mhcpraep_mhcpraep_id = Column(Integer)
	source_source_id = Column(Integer)
	
	gradient_gradient_id = Column(Integer)
	person_person_id = Column(Integer)
	ms_run_modification_ms_run_modification_id = Column(Integer)
	
	def __init__(self, tmp_name, mass_spec, run, source_id,  prep_id) :
		self.filename =  run
		self.date = mass_spec['run_date']
		self.used_share = mass_spec['sample_share']
		if mass_spec['comment'] != '' :
			self.comment = mass_spec['comment']
		self.timestamp = tmp_name
		
		self.mhcpraep_mhcpraep_id = prep_id
		self.source_source_id = source_id
		self.gradient_gradient_id = getMethodIdFromCollectInt(DBSession, Gradient, int(mass_spec['method']))
		self.person_person_id = getPersonIdFromCollectInt(DBSession, Person, int(mass_spec['made_by']))
		modId = getModificationIdFromCollectInt(DBSession, Modification, int(mass_spec['modification']))
		if not modId == 1 :
			self.ms_run_modification_ms_run_modification_id  = modId
		
	def stringIt(self) :
		l = []
		l.append('Filename = %s' %self.filename)
		l.append('Person = %s'% getPersonById_Name(DBSession, Person, self.person_person_id))
		l.append('Date = %s' %str(self.date))
		l.append('Used share = %s' %str(self.used_share))
		l.append('Method = %s'%str(getMethodById_Name(DBSession, Gradient, self.gradient_gradient_id)))
		if not self.ms_run_modification_ms_run_modification_id is None :
			l.append('Modification = %s' %str(getModificationById_Name(DBSession, Modification, self.ms_run_modification_ms_run_modification_id)))
		else :
			l.append('Modification = None')
		l.append(stringItDBEntryNullable(self.comment, 'Comment'))
		return l


class Hit(Base) :
	
	__tablename__ = 'spectrum_hit'
	
	spectrum_hit_id = Column(INTEGER, primary_key=True, autoincrement=True)
	RT = Column(DOUBLE)
	MZ = Column(DOUBLE)
	charge = Column(INTEGER)
	ionscore = Column(INTEGER)
	e_value = Column(DOUBLE)
	PEP = Column(DOUBLE)
	q_value = Column(DOUBLE)
	precursorarea = Column(DOUBLE)
	injectiontime = Column(DOUBLE)
	first_scan = Column(INTEGER)
	last_scan = Column(INTEGER)
	
	comment = Column(TEXT)
	timestamp = Column(CHAR(255))
	
	person_person_id = Column(INTEGER)
	peptide_peptide_id = Column(INTEGER)
	ms_run_ms_run_id = Column(INTEGER)
	
	def __init__(self, rest, tmp_name, seq, ms_run_id, username) :
		d = ast.literal_eval(rest)
		self.timestamp = tmp_name
		self.RT = transformer.getFromRestKey(d, 'RT [min]')
		self.MZ = transformer.getFromRestKey(d, 'm/z [Da]')
		self.charge = transformer.getFromRestKey(d, 'Charge')
		self.ionscore = transformer.getFromRestKey(d, 'IonScore')
		self.e_value = transformer.getFromRestKey(d, 'Exp Value')
		self.PEP = transformer.getFromRestKey(d, 'PEP')
		self.q_value = transformer.getFromRestKey(d, 'q-Value')
		if 'Precursor Area' in d.keys() :
			self.precursorarea = transformer.getFromRestKey(d, 'Precursor Area')
		self.injectiontime = transformer.getFromRestKey(d, 'Ion Inject Time [ms]')
		self.last_scan = transformer.getFromRestKey(d, 'Last Scan')
		self.first_scan = transformer.getFromRestKey(d, 'First Scan')
		
		peptides = DBSession.query(Peptide).filter(Peptide.sequence == seq).all()
		if len(peptides) == 1 :
			self.peptide_peptide_id= peptides[0].peptide_id
			#~ print "***pepid: ",self.peptide_peptide_id
		else :
			if len(peptides) == 0 :
				new_peptide = Peptide(seq, tmp_name)
				DBSession.add(new_peptide)
				self.peptide_peptide_id=DBSession.query(Peptide).filter(Peptide.sequence == seq).first().peptide_id
				#~ self.peptide_peptide_id=new_peptide.peptide_id
				#~ print "lalabla", type(new_peptide.peptide_id),new_peptide.peptide_id				
			else :
				print '[ERROR] models.Hit : to many Peptides!'
				#TODO hiwi:andreas implement rollback and error 
		self.person_person_id = DBSession.query(User).filter(User.username == username).first().person_person_id
		self.ms_run_ms_run_id = ms_run_id
		
class Peptide(Base) :
	
	__tablename__ = 'peptide'
	
	peptide_id = Column(INTEGER, primary_key=True, autoincrement=True)
	
	sequence = Column(VARCHAR(255))
	comment = Column(TEXT)
	timestamp = Column(CHAR(255))
	calc_weight = Column(DOUBLE)
	
	def __init__(self, seq, tmp_name) :
		self.sequence = seq
		self.timestamp = tmp_name

class Gradient(Base) :
	__tablename__ = 'gradient'
	
	gradient_id = Column(Integer, primary_key=True)
	name = Column(String(255))
	comment = Column(String(255))

class Modification(Base) :
	''' equivalent to ms_run_modification in DB
	first Object must be 'None' ! This is adapted in class MSData to make it nullable!
	'''
	
	__tablename__ = 'ms_run_modification'
	
	ms_run_modification_id = Column(Integer, primary_key = True)
	name = Column(String(255))



class Person(Base) :
	__tablename__ = 'person'
	
	person_id = Column(Integer, primary_key=True)
	first_name = Column(String(255))
	last_name = Column(Unicode(255))
	timestamp = Column(String(255))
		
class InternData(Base):
	__tablename__ = 'intern_data' # das muesste eigentl. in __init__
	__table_args__ = {'prefixes': ['TEMPORARY']}
	
	id = Column(Integer, primary_key=True)
	timestamp = Column(String(255))
	seq = Column(Integer)
	run = Column(String(255))
	rest = Column(String(255))
	
	source_id = Column(Integer)
	hla_typing = Column(String(255))
	prep_id = Column(Integer)
	mass_spec_id = Column(Integer)
		
	def __init__(self, timestamp, seq, run, rest) :
	   self.timestamp = timestamp
	   self.seq = seq
	   self.run = run
	   self.rest = rest
	   

class LogFile(Base) :
	__tablename__ = 'log_file'
	
	log_file_id = Column(INTEGER, primary_key=True)
	tmp_name = Column(CHAR(255))
	action = Column(CHAR(255))
	#~ successful = Column(BOOLEAN) #booleans not supported anymore in sqlalchemy?
	successful = Column(INTEGER)
	message = Column(TEXT)
	
	users_users_id = Column(INTEGER)
	
	def __init__(self, tmp_name, user_id) :
		self.tmp_name = tmp_name
		self.users_users_id = user_id
		self.message = ''
		self.action = 'upload'
		#~ self.successful = b'0' #booleans not supported anymore in sqlalchemy?
		self.successful = 0
	

class User(Base):
	__tablename__ = 'users'
	
	id = Column(Integer, primary_key=True)
	username = Column(String(255), unique=True)
	password = Column(String(255), nullable=False)
	in_group = Column(String(255), nullable=False)
	person_person_id = Column(INTEGER)

	def __init__(self, name, password, in_group):

		self.name = name
		self.password = password
		self.in_group = in_group

class RootFactory(object):
	#__name__ = 'root'
	__acl__ = [ (Allow, Everyone, 'view'),
				(Allow, 'group:editors', 'edit') ]
	def __init__(self, request):
		pass
		
		
		
		
