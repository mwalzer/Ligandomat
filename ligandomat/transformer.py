def getSeq(row) :
	if 'Sequence' in row :
		return row['Sequence']
	if ' Sequence' in row :
		return row[' Sequence']
	if 'Sequence ' in row :
		return row['Sequence ']
		
def getRun(row) :
	if 'Spectrum File' in row :
		return row['Spectrum File']
	if ' Spectrum File' in row :
		return row[' Spectrum File']
	if 'Spectrum File ' in row :
		return row['Spectrum File ']
		
def getRest(row, seq, run) :
	d = row.copy()
	for item in row :
		if row[item] == seq :
			d.pop(item)
		if row[item] == run :
			d.pop(item)
	return d
	
#------------
	
def getFromRestKey(dict, key) :
	try :
		value = dict[key]
		return value
	except:
		print '[ERROR in transformer] got no key *%s*' %key
		raise
	

		