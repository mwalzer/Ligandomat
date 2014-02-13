import csv

#***** THE function *****

# path -> list of dicts
def cleverDictReader(path) :
    file_of_path = open(path, 'rb')
    delimiter = cleverSniff(path)
    dict_reader = csv.DictReader(file_of_path, delimiter=delimiter)
    list_individuals = []
    for row in dict_reader :
        list_individuals.append(row)
    #print list_individuals
    return list_individuals

def commaDictReader(path) :
    file_of_path = open(path, 'rb')
    delimiter = ','
    dict_reader = csv.DictReader(file_of_path, delimiter=delimiter)
    list_individuals = []
    for row in dict_reader :
        list_individuals.append(row)
    return list_individuals

#    returns delimiter or error
def cleverSniff(path) :
	file_of_path = open(path, 'rb')
	reader = file_of_path.read()
	# saved data (is stocked if next round of cleverSniffIn is sufficiant)
	lines = []
	dictList = []

	# first try with first 10 rows
	lines = getLinesFrom(reader, 0, 9)
	dictList = makeDictsFor(lines)
	possibilities = compareForPossibilities(dictList[0], dictList[1:len(dictList)])
	print "After the first round following possibilities were detected : %s" %possibilities	
        if len(possibilities) == 1 :
            return possibilities[0]
        else :
            print 'Took %s as delimiter' %findBestDelimiter(possibilities)
            return findBestDelimiter(possibilities)

def findBestDelimiter(possis) :
    if ',' in possis :
        return ','
    else :
        return possis[0]

# returns whole rows i until j as strings in a list
# if j is greater than len(lines_in_input_file) -> only read as many as possible
def getLinesFrom(reader, i, j) :
    lines = []
    line = ''
    for char in reader :
        if char == '\n' :
            lines.append(line)
            line = ''
            i = i+1
            if i == j :
                break
        else :
            line += char
    return lines	

# returns a list of dicts corresponding to input lines
def makeDictsFor(lines) :
	dicts = []
	i=0
	for line in lines :
		#make a dict!
		d = dict()
		dicts.append(d)
		i = i+1	
		### srt.count
		for character in line :		
			# key exists already -> #char = #char +1
			if (character in d) :
				d[character] = d[character] + 1
			# key does not exist -> new entry & #char = 1
			else :
				d[character] = 1
	return dicts
	

# returns all possibilities for delimiter
# compare dict of first line to all other dicts
#  idea : #char of delimiter must(!) be same in all lines
def compareForPossibilities(dictCompare, dicts) :
	possibilities = []
	dullKey = False
	
	for key in dictCompare :
		dullKey = False
		# check for all other dicts
		for dict in dicts :
			# precondition
			if key in dict :
				if not dict[key] == dictCompare[key] :
					# key of ANY dict not matching  -> wrong key
					dullKey = True
					break
			else :
				# key of ANY dict NOT in dict -> wrong key
				dullKey = True
				break
		# if not broke jet (dullKey) -> found possible key
		if not dullKey :
			possibilities.append(key)

	return possibilities
