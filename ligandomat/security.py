from .models import (
	DBSession,
	User,
	)

def groupfinder(userid, request): 
	session = DBSession()
	ug  =list()
	for instance in session.query(User).filter(User.username==userid):
		in_group = 'group:'+instance.in_group  
		ug.append(in_group)
	return ug