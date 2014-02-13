<%inherit file='ligandomat:templates/layout.mako'/>




Currently you have ${nSeqs} Peptides in your data base! <br><br>
##Show all peptides after upload is also used when All Peptides are clicked
##% for s in seqs :
	##	${s}
##% endfor

<br><br>
<a href=${request.route_url('Ligandomat')}><input type='button' value='Back to Options'></a>

<br><br>
<br><br>