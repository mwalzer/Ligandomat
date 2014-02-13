

aminoacids = dict(G = 'Glycine',  g = 'Glycine', 
				A = 'Alanin',  a = 'Alanin',
				V='Valine', v='Valine', 
				L='Leucine', l='Leucine', 
				I='Isoleucine', i='Isoleucine', 
				S='Serine', s='Serine', 
				T='Theronine', t='Theronine', 
				C='Cysteine', c='Cysteine', 
				M='Methonine', m='Methonine', 
				P='Proline', p='Proline', 
				D='Aspartic acid', d='Aspartic acid', 
				N='Asparagine', n='Asparagine', 
				E='Glutamic acid', e='Glutamic acid', 
				Q='Glutamine', q='Glutamine',
				K='Lysine', k='Lysine', 
				R='Aragine', r='Aragine', 
				H='Histidine', h='Histidine', 
				F='Phenylalanine', f='Phenylalanine', 
				Y='Tyrosine', y='Tyrosine', 
				W='Tryptophan', w='Tryptophan', 
				U='Selenocysteine', u='Selenocysteine')

# 0 = unpolar , 1 = polar and uncharged, 2 = elelectrically charged, 3 = special
'''
groups = dict(0 = ['A', 'V', 'L', 'I', 'Y', 'F', 'M', 'W'],
			1 = ['S', 'T', 'N', 'Q'],
			2 = ['R', 'H', 'K', 'D', 'E'],
			3 = ['C', 'U', 'G', 'P'])
'''
def getPatternPeptides(pattern, DBSession, Peptide) :
	print '*** PATTERN = %s' %pattern
	allPep = DBSession.query(Peptide).all()
	startAt = 0
	for i in range(0, len(pattern)) :
		if pattern[i] ==  '*':
			startAt = startAt + 1
		else :
			break
	
	if startAt == len(pattern) :
		return allPep
	
	if '(' in pattern :
		patternListList = makePatternList(pattern)
	
	patternPeps = []
	
	
	for pep in allPep :
		if not '(' in pattern :
			lastIndex = len(pattern) -1
			for i in range(startAt, len(pattern)) :
				# lenght distriction
				if len(pattern)  > len(pep.sequence) :
					break
				# no differences with /
				if pattern[i] == '*' and i < lastIndex :
					continue
				if pattern[i] == '*' and i == lastIndex :
					patternPeps.append(pep)
					break
				if pattern[i] != str(pep.sequence[i]) :
					break
				else :
					if (i == lastIndex and pattern[i] == str(pep.sequence[i])) :
						patternPeps.append(pep)
		else :
			lastIndex = len(patternListList) -1
			for i in range(0, len(patternListList)) :
				
				if len(patternListList)  > len(pep.sequence) :
					break
				motivList = patternListList[i]	
				if '*' in motivList and i < lastIndex :
					continue
				if '*' in motivList and i == lastIndex :
					patternPeps.appen(pep)
					break
					
				if not pep.sequence[i] in motivList :
					break
				else :
					if pep.sequence[i] in motivList and i == lastIndex :
						patternPeps.append(pep)
	return patternPeps
		
		
def makePatternList(pattern) :
	patternListList = []
	patternStrings = pattern.split(')')
	if '' in patternStrings :
		patternStrings.pop(patternStrings.index(''))
	
	for string in patternStrings :
		stack = []
		inBrackets = False
		for i in range(0, len(string)) :
			if string[i] == '(' :
				inBrackets = True
				continue
			if (string[i] in aminoacids or string[i] == '*') and  i != len(string)-1:
				if inBrackets :
					stack.append(string[i])
				else :
					patternListList.append([string[i]])
			if (string[i] in aminoacids  or string[i] == '*') and i == len(string)-1 :
				if inBrackets :
					stack.append(string[i])
					patternListList.append(stack)
					inBrackets = False
					stack = []
				else :
					patternListList.append([string[i]])
	return patternListList
	
	
	
	
	