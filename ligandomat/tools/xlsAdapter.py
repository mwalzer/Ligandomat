import xlrd
import xlwt
from xlutils.copy import copy

def xlsDictReader(filename, sheet_index = 0) :
	book = xlrd.open_workbook(filename)
	sheet = book.sheet_by_index(sheet_index)
	headers = dict((i, sheet.cell_value(0,i)) for i in range(sheet.ncols) )
	ret = list()
	for i in range(1, sheet.nrows) :
		ret.append( dict((headers[j], sheet.cell_value(i,j)) for j in headers))
	return ret