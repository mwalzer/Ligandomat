from models import *
import string
from decimal import Decimal
from pyramid.response import Response

def correctTyping(allele) :
	if len(allele) == 0 :
		return (True, '')
		
	if len(allele) == 2 :
		return (allele.isdigit(), allele)
		
	if len(allele) == 3 :
		if allele[0] == ':' :
			return (allele[1:3].isdigit(), allele[1:3])
		if int(allele[0:2]) == 0:
			return (allele.isdigit(), allele[1:3])
		return (allele.isdigit(), allele)
		
	if len(allele) == 4 :
		if allele[0] == ':' :
			if int(allele[1]) == 0 :
				return (allele[2:4].isdigit(), allele[2:4])
			else :
				return (allele[1:4].isdigit(), allele[1:4])
		else :
			return (False, 'Wrong HLA Typing')
	#detailed Typing needs more specific typing form needed = :III:II:IIB
	if len(allele) == 7 :
		return (allele[0] == ':' and allele[1:4].isdigit() and allele[4] == ':' and allele[5:7].isdigit(), allele[1:])
	if len(allele) == 10  :
		return (allele[0] == ':' and allele[1:4].isdigit() and allele[4] == ':' and allele[5:7].isdigit() and allele[7] == ':' and allele[8:10].isdigit(), allele[1:])
	if len(allele) == 11 :
		return (allele[0] == ':' and allele[1:4].isdigit() and allele[4] == ':' and allele[5:7].isdigit() and allele[7] == ':' and allele[8:10].isdigit() and allele[10].isalpha(), allele[1:])
	return (False, 'Wrong Typing')

def validSource(source) :
	# source name
	name = source['new_source']
	if len(name) < 1 :
		return (False, 'Please enter a name for your new source.')
	if name in getAllKnownSource_Name(DBSession, SourceData) :
		return (False, 'The source name %s is already taken. How about choosing a differnt name? :)' %name)
	# *valid Source*	
	return (True, 'Alright ;)')
	
def validPrep(prep) :

	# sample mass
	mass = prep['sample_mass']
	if mass == "" :
		return (True, 'Noting entered')
	
	if not ('g' in mass or 'ml' in mass) :
		return (False, 'Please enter sample mass or volume with "g" or  "ml" - or leave it empty')
	
	mass2 = mass.replace(',', '.').replace('g', '').replace('ml', '').replace(' ', '')
	mass3 = mass2.replace('.', '')
		
	if not mass3.isdigit() :
		return (False, 'Please enter a number for sample mass')
	if not (0.1 <= float(mass2) and float(mass2) < 100) :
		return (False, 'That is a heavy sample of %s g / ml !' %mass)

	# antibody mass
	abmass = prep['antibody_mass']
	if abmass == "" :
		return (True, 'Noting entered')
		
	abmass2 = abmass.replace(',', '.')
	abmass3 = abmass2.replace('.', '')
	
	if not abmass3.isdigit() :
		return (False, 'Please enter a number for antibody mass')
	if not (0.1 <= float(abmass2) and float(abmass2) < 100) :
		return (False, 'You used antibodies with a huge mass of %s mg!' %abmass)
	# *valid Prep*
	return (True, 'Alright ;)')

def validMS(mass_spec) :
	# prep date
	dateVal = validDateString(mass_spec['run_date'])
	if not  dateVal[0]:
		return dateVal
	share = mass_spec['sample_share']
	if not share.isdigit() :
		return (False, 'Please enter a number for sample share')
	if not (int(share) > 0 and int(share) <= 100) :
		return (False, 'Please enter a number between 1 and 100 for attribute sample share')
	# *valid Mass_spec*
	return (True, 'Alright ;)')



# validation a date	
def validDateString(date) :
	if '.' in date :
		dmy = string.split(date, '.')
		d = dmy[0]
		m = dmy[1]
		y = dmy[2]
		return validDMY(d, m, y)
	if '/' in date :
		ymd = string.split(date, '/')
		d = ymd[2]
		m = ymd[1]
		y = ymd[0]
		return validDMY(d, m, y)
	if (len(date) == 6 and date.isdigit()):
		y = date[0:2]
		m = date[2:4]
		d = date[4:]
		return validDMY(d, m, y)
	else :
		return (False, 'No proper date')
		
def validDMY(d, m, y) :
	if not (d.isdigit() and m.isdigit() and y.isdigit()) :
		return (False, 'Are you sure you want to enter a date with characters - not numbers?')
	intd = int(d)
	if not(0 < intd and intd < 32) :
		return (False, 'Uuuupps, you entered a funny day : %s' %intd)
	intm = int(m)
	if not(0 < intm and intm < 13) :
		return (False, 'Uuuupps, you entered a funny month : %s' %intm)
	inty = int(y)
	if not((1990 < inty and inty < 2050) or (0 <= inty and inty < 100)) :	
		return (False, 'Uuuupps, you entered a funny year : %s' %inty)	
	return (True, 'Valid date')
	

def rowInDB(row) :
	if row.seq in getAllPeptide_Sequence(DBSession, Peptide) :
		peptide = getPeptideBySeq(DBSession, Peptide, row.seq)
		hits = DBSession.query(Hit).filter(Hit.peptide_peptide_id == peptide.peptide_id).all()
		restRow = ast.literal_eval(row.rest)
		for hit in hits :
			if (float(hit.MZ) == float(restRow['m/z [Da]']) and 
					float(hit.RT) == float(restRow['RT [min]']) and 
					float(hit.e_value) == float(restRow['Exp Value'] ) and 
					float(hit.PEP) == float(restRow['PEP']) and 
					float(hit.injectiontime) == float(restRow['Ion Inject Time [ms]']) and 
					float(hit.q_value) == float(restRow['q-value']) and 
					float(hit.precursorarea) == float(restRow['Precursor Area']) ):
				return True
	else :
		return False
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	