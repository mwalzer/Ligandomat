import cleverSniff
import csv


def dictReaderFile(file) :
    delimiter = cleverSniff.cleverSniffFile(file)
    dict_reader = csv.DictReader(file, delimiter=delimiter, quotechar='"')
    #file.close()
    ''' save each individual as a dict in a list'''
    list_individuals = []
    for row in dict_reader :
        list_individuals.append(row)
    return list_individuals
    
    
def dictWriter(dicts, filename) :
	file = open(filename, 'w')
	fieldnames = []
	for i in range(0, 24) :
		fieldnames.append(i)
	dict_writer = csv.DictWriter(file, delimiter=',', fieldnames=fieldnames)
	for d in dicts :
		dict_writer.writerow(d)

