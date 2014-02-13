
		
# used in wizard overview
def generateKey(internData) :
	s = 'source=' + str(internData.source_id)
	s +='prep=' + str(internData.prep_id)
	s += 'ms=' +str(internData.mass_spec_id)
	return s
	
def makeItFloat(string) :
	if string == '' :
		return 0.0
	else :
		return float(string.replace(',', '.'))
		
def getMass_g(string) :
	s = string.replace('g', '').replace(',', '.').replace(' ', '')
	return float(s)

def getVolume_ml(string) :
	s = string.replace('ml', '').replace(',', '.').replace(' ', '')
	return float(s)

# date making	
def makeADate(date) :
	if '.' in date :
		dmy = date.split('.')
		d = dmy[0]
		m = dmy[1]
		y = dmy[2]
		return makeADateDMY(d, m, y)
	if '/' in date :
		ymd = date.split('/')
		d = ymd[2]
		m = ymd[1]
		y = ymd[0]
		return makeADateDMY(d, m, y)
	if (len(date) == 6 and date.isdigit()):
		y1 = int(date[0:2])
		if (90 < y1 and y1 <= 99) :
			y2 = '19'
			if len(str(y1)) == 1 :
				y2 += '0'
				y2 += str(y1)
			else :
				y2 += str(y1)
		else :
			y2 = '20'
			if len(str(y1)) == 1 :
				y2 += '0'
				y2 += str(y1)
			else :
				y2 += str(y1)
		y3 = str(y2)
		m = date[2:4]
		d = date[4:]
		return makeADateDMY(d, m, y3)
		
def makeADateDMY(d, m, y) :
	date = ''
	date += y
	date += '-'
	date += m
	date += '-'
	date += d
	return date
