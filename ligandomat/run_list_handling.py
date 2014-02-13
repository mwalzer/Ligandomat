from sqlalchemy import and_
from DBtransfer import *
from zlib import *

#retrun compressed
def generateFromDB(DBSession, InternData, tmp_name) :
	run_list=[]
	user_data = DBSession.query(InternData).filter(InternData.timestamp == tmp_name)
	for data in user_data :
		if  not data.run in run_list :
			run_list.append(data.run)
	return compressList(run_list)
	
	
def getknown_runsAndrun_list(DBSession, Mass_specData, InternData, tmp_name) : #CR: rename to splitKnownAndTodo
	#~ knownRuns = [] # devide runs from upload into known runs (in DB) ...
	#~ runList = [] #...and the usual run_list, to get data from these runs
	
	#CR: 
	runs_in_upload = decompressList(generateFromDB(DBSession, InternData, tmp_name)) 
	
	#~ known_runs = [x for x in DBSession.query(Mass_specData.filename).all() if x in runs_in_upload]
	known_runs = [x.filename for x in DBSession.query(Mass_specData).filter(Mass_specData.filename.in_(runs_in_upload))]
	run_list =  [x for x in runs_in_upload if x not in known_runs]
	
	#~ allRuns = getAllRuns_Filename(DBSession, Mass_specData)# in DB saved runs
	
	#~ decomruns_in_upload = decompressList(runs_in_upload)
	
	#~ for run in decomruns_in_upload :
		#~ if run in allRuns :
			#~ knownRuns.append(run)
		#~ else :
			#~ runList.append(run)	
	return (known_runs, run_list)
	
	
#input compressed
#output not compressed
def usedRuns(run_list, params) :
	list_of_used_runs = []
	runs = decompressList(run_list)

	for i in range(0, len(runs)) :
		if runs[i] in params : 
			list_of_used_runs.append(runs[i])
	return list_of_used_runs

# input not compressed	
# output InternData objects
def rowsToFill(DBSession, InternData, tmp_name, used_runs) : 
	users_rows = getUserRows(DBSession, InternData, tmp_name)
	rows = []
	for row in users_rows :
		if row.run in used_runs :
			rows.append(row)
	return rows

#input compressed, not compressed
def throughOutUsedRuns(run_list, used_runs) : # not compressed
	rl = decompressList(run_list)
	for run in used_runs :
		rl.pop(rl.index(run))
	if len(rl) > 0 :
		return compressList(rl)
	else :
		return []
		
#
def compressList(list) :
	return compress('$$'.join(list))
	
#input compressed
def decompressList(run_list) :
	return decompress(run_list).split('$$')
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
