
import MySQLdb
import ast
from sqlalchemy import and_
import config

# used to get types out of DB
class Connection() :
		
	def getType(self , table, query) :
		_dbconnection = MySQLdb.connect(host =  config.host, user = config.user, passwd = config.passwd, db = config.db, port = config.port)
		_dbconnection.autocommit(False)
		c = _dbconnection.cursor()
		result = dict()
		for enum in query :
			c.execute("SELECT COLUMN_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'LigandosphereDB_dev' AND TABLE_NAME = '" + table + "' AND COLUMN_NAME = '" + enum + "' ")
			res = c.fetchone()
			if res:
				row_result = res[0].split('\'')[1::2]
			result[enum] = row_result
		return result
		
		
	def getMiningTable(self, filename) :
		_dbconnection = MySQLdb.connect(host =  config.host, user = config.user, passwd = config.passwd, db = config.db, port = config.port)
		_dbconnection.autocommit(False)
		c = _dbconnection.cursor()
		
		c.execute("SELECT * FROM ( SELECT * FROM (SELECT ms_run_ms_run_id as peptidems_id, sequence, RT, MZ, ionscore, e_value FROM spectrum_hit INNER JOIN " + 
			"peptide ON peptide_id = peptide_peptide_id) peptide INNER JOIN (SELECT ms_run_id, source_source_id as mssource_id, filename as runname, antibody_set, " + 	
			"sample_mass, sample_volume FROM ms_run INNER JOIN mhcpraep ON mhcpraep_mhcpraep_id = mhcpraep_id ) ms ON ms_run_id = peptidems_id) peprun INNER JOIN (SELECT " + 
			"source_id, name as sourcename, organ, tissue, dignity, typing_source_id, gene_group, specific_protein, dna_coding, dna_noncoding, expression_suffix FROM source " +				"INNER JOIN(SELECT source_source_id as typing_source_id, gene_group, specific_protein, dna_coding, dna_noncoding, expression_suffix FROM source_hlatyping " +
			"INNER JOIN hlaallele ON hlaallele_hlaallele_id = hlaallele_id) typing ON source_id = typing_source_id) source ON source_id = mssource_id ORDER BY sequence ASC")
		res = c.fetchall()
		import csv
		file = open(filename, 'w')
		writer = csv.writer(file)
		header = ["peptidems_id", "sequence", "RT", "MZ", "ionscore", "e_value", "ms_run_id","mssource_id","runname","antibody_set","sample_mass","sample_volume","source_id","sourcename","organ","tissue","dignity","typing_source_id","gene_group","specific_protein","dna_coding","dna_noncoding","expression_suffix"]
		writer.writerow(header)
		for line in res :
			writer.writerow(line)
		

# used in wizard_views  for creating new Source / Prep
# used in forms to init widgets
def getAllKnownSource_Name(DBSession, SourceData) :
	ks = []
	db_sources = DBSession.query(SourceData)
	for source in db_sources :
		ks.append(source.name)
	return ks
	
def getAllKnownPrep_Id(DBSession, PrepData) :
	kp = []
	db = DBSession.query(PrepData)
	for prep in db :
		kp.append(prep.mhcpraep_id)
	return kp
	
def getAllKnownPrep_Name(DBSession, PrepData, SourceData, Person) :
	prep_names = [] 
	prep_data = DBSession.query(PrepData).all()
	for prep in prep_data :
		name = ''
		name += str(prep.antibody_set)
		name += ' '
		if prep.antibody_mass != None :
			name += ' with '
			name += str(prep.antibody_mass)[0:4]
			name += ' mg - '
		name += getPersonById_Name(DBSession, Person, prep.person_person_id)
		if prep.sample_mass != None :
			name += ' - sm: %s g' %str(prep.sample_mass)[0:4]
		if prep.sample_volume != None :
			name += ' - sv: %s ml' %str(prep.sample_volume)[0:4]
		if prep.comment != None :
			name += ' - %s' %str(prep.comment)
			
		prep_names.append(name)
	return prep_names
	
def getAllPerson_Name(DBSession, Person):
	person_names = [] 
	for person in DBSession.query(Person).all() :
		show_name = person.first_name
		show_name += ' '
		show_name += person.last_name
		person_names.append(show_name)
	return person_names
	
def getAllMethod_Name(DBSession, Gradient) :
	methods = []
	for method in DBSession.query(Gradient).all() :
		methods.append(method.name)
	return methods
	
def getAllModification_Name(DBSession, Modification) :
	mods = []
	for mod in DBSession.query(Modification).all() :
		mods.append(mod.name)
	return mods
		
def getHLAAlleles(DBSession, HLAAllele) :
	h = []
	db_hlas = DBSession.query(HLAAllele)
	for object in db_hlas :
		h.append(object.gene_group)
	return h	

def getAllPeptide_Sequence(DBSession, Peptide) :
	s = []
	peptides = DBSession.query(Peptide).all()
	for p in peptides :
		s.append(p.sequence)
	return s
	
def getAllHitsOfPeptide(DBSession, Peptide, Hit, peptide) :
	hits = []
	peptide_id = peptide.peptide_id
	allHits = DBSession.query(Hit).all()
	for hit in allHits :
		if hit.peptide_peptide_id == peptide_id :
			hits.append(hit)
	return hits
	
	
def getAllRuns_Filename(DBSession, MSData) :
	runs = []
	ms_runs = DBSession.query(MSData).all() #CR: attributes only?! #CR: filter for current runs from file - see https://groups.google.com/forum/#!topic/sqlalchemy/4KWTktoHTVQ
	for run in ms_runs :
		if not run.filename in runs :
			runs.append(run.filename)
	return runs
	
def getAllTmps(DBSession, LogFile) :
	l = []
	#debug
	#~ print LogFile
	for log in DBSession.query(LogFile) :
		l.append(log.tmp_name)
	return l
	

# used in models in stringIt()
def getSourceById(DBSession, SourceData, id) :
	source = DBSession.query(SourceData).filter(SourceData.source_id == id).first()
	return source
	
def getTypingsBySourceId(DBSession, SourceHLA, id) :
	typings = []
	allTyp = DBSession.query(SourceHLA).all()
	for typ in allTyp :
		if typ.source_source_id == id :
			typings.append(typ)
	return typings

def getHLAAlleleById(DBSession, HLAAllele, id) :
	allele = DBSession.query(HLAAllele).filter(HLAAllele.hlaallele_id == id).first()
	return allele

def getPrepById(DBSession, PrepData, id) :
	prep = DBSession.query(PrepData).filter(PrepData.mhcpraep_id == id).first()
	return prep
	
def getMSById(DBSession, MSData, id) :
	ms = DBSession.query(MSData).filter(MSData.ms_run_id == id).first()
	return ms

def getHitById(DBSession, Hit, id) :
	hit = DBSession.query(Hit).filter(Hit.spectrum_hit_id == id).first()
	return hit
	
def getUserByID(DBSession, User, id) :
	user = DBSession.query(User).filter(User.id == id).first()
	return user
	
def getPersonById(DBSession, Person, id) :
	person = DBSession.query(Person).filter(Person.person_id == id).first()
	return person

def getUserByName(DBSession, User, name) :
	user = DBSession.query(User).filter(User.username == name).first()
	return user

def getPersonById_Name(DBSession, Person, id) :
	person = DBSession.query(Person).get(id)
	return person.first_name + ' ' + person.last_name
	
def getMethodById_Name(DBSession, Gradient, id) :
	method = DBSession.query(Gradient).filter(Gradient.gradient_id == id).first()
	return method.name

def getModificationById_Name(DBSession, Modification, id) :
	modification = DBSession.query(Modification).filter(Modification.ms_run_modification_id == id).first()
	return modification.name

def getPeptideBySeq(DBSession, Peptide, seq) :
	return DBSession.query(Peptide).filter(Peptide.sequence == seq).first()
	
# used in models to get ids from collect int (got from forms)
def getPersonIdFromCollectInt(DBSession, Person, i) :
	person = DBSession.query(Person).all()
	p = person[i]
	return p.person_id

def getMethodIdFromCollectInt(DBSession, Gradient, i) :
	methods = DBSession.query(Gradient).all()
	return methods[i].gradient_id
	
def getModificationIdFromCollectInt(DBSession, Modification, i) :
	mods = DBSession.query(Modification).all()
	return mods[i].ms_run_modification_id
	
def getSourceFromCollectInt(DBSession, SourceData, i) :
	name_of_clicked = getAllKnownSource_Name(DBSession, SourceData)[i]				
	return DBSession.query(SourceData).filter(SourceData.name == name_of_clicked).first()
	
# specific gets
	
def getUserRows(DBSession, InternData, tmp_name):
	return DBSession.query(InternData).filter(InternData.timestamp == tmp_name).all()
	
def deleteUsersRows(DBSession, InternData, tmp_name) :
	users_rows = getUserRows(DBSession, InternData, tmp_name)
	for userRow in users_rows :
		DBSession.delete(userRow)
		
def deleteUsersSources(DBSession, SourceData, tmp_name) :
	DBSession.delete(DBSession.query(SourceData).filter(SourceData.timestamp == tmp_name).all())
	
def deleteUsersTypings(DBSession, SourceHLA, tmp_name) :
	DBSession.delete(DBSession.query(SourceHLA).filter(SourceHLA.timestamp == tmp_name).all())
	
def deleteUsersPreps(DBSession, PrepData, tmp_name) :
	DBSession.delete(DBSession.query(PrepData).filter(PrepData.timestamp == tmp_name).all())
	
def deleteUsersMS(DBSession, MSData, tmp_name) :
	DBSession.delete(DBSession.query(MSData).filter(MSData.timestamp == tmp_name).all())
		
def getUserIdByName(DBSession, User, name) :
	return DBSession.query(User).filter(User.username == name).first().id
	
def getCurrentLog(DBSession, LogFile, tmp_name) :
	return DBSession.query(LogFile).filter(LogFile.tmp_name == tmp_name).first()
	
def getLogByFilename(DBSession, LogFile, filename):
	logs = DBSession.query(LogFile).all()
	for log in logs :
		log_filename = log.tmp_name.split(']*[')[2]
		if log_filename == filename :
			return log
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
