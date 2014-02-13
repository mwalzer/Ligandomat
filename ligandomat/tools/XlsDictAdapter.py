import xlrd
import xlwt
from xlutils.copy import copy
#from django.utils.encoding import smart_str, smart_unicode

#read from file content needed for file handler  
def XlsDictReader(f, sheet_index=0, sheet_name='', no_header = False):
  """f is a file content, sheet_index is the index of the sheet to access"""
  book    = xlrd.open_workbook(file_contents=f)
  sheet = None
  if sheet_name:
    for i in range(0,book.nsheets):
      sheet = book.sheet_by_index(i)
      if sheet.name == sheet_name: 
        break
        sheet = None
  else:
    sheet = book.sheet_by_index(sheet_index)
  if no_header:
    k = 0
    import string
    lt = list(string.uppercase)
    #boast lt to size of sheet.ncols
    if(len(lt)<sheet.ncols):
        for k in range(sheet.ncols-len(lt)):
            lt.append(lt[k]+"A") 
    headers = dict( (i, lt[i] ) for i in range(sheet.ncols) ) 
  else:
    headers = dict( (i, sheet.cell_value(0, i) ) for i in range(sheet.ncols) )
    k = 1
  ret = list()
  for i in range(k, sheet.nrows):
    ret.append( dict( (headers[j], sheet.cell_value(i, j)) for j in headers ) )
  return ret


def XlsDictWriter(f, ld, sheet_name='sheet'):
	""""f is a string for a filename, sheet_name is the name of the sheet to be written, can't be overwritten. ld is limited to 65536 rows due to xlwt."""
	try:
		tmp = xlrd.open_workbook(f)
		book = copy(tmp)
	except:
		book = xlwt.Workbook(encoding = 'UTF-8')
	sheet = book.add_sheet(sheet_name)
	if len(ld) > 0:
		header = set()
		for row in ld:
			for r in row.keys():
				header.add(r)
		for i,key in enumerate(header):
			sheet.write(0, i, label = key)
		for i,r in enumerate(ld):
			for j,key in enumerate(header):
				try:
					sheet.write(i+1, j, label = r[key])
				except:
					sheet.write(i+1, j, label = "N/A")
		book.save(f)
		return True
	#~ if len(ld) > 0:
		#~ ks = ld[0].keys()
		#~ for i,key in enumerate(ks):
			#~ sheet.write(0, i, label = str(key))
		#~ for i,r in enumerate(ld):
			#~ for j,key in enumerate(ks):
				#~ sheet.write(i+1, j, label = str(r[key]))
	else:
		return False