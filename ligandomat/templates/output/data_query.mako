<%inherit file='ligandomat:templates/layout.mako'/>

<form method="post" >


<table>
	<tr>
		<td> PEPTIDE
		</td>
	</tr>

	<tr>
		<td>
			List of all Peptides : 
		</td>
		<td>
		</td>
		<td>
			<input type='submit' name='button_peptide_all' value='All Peptides'>
		</td>
	</tr>
	<tr>
		<td>
			Get Info about the peptide :
		</td>
		<td>
			${form.peptide_info} 
		</td>
		<td>
			<input type="submit" name="button_peptide_info" value="Get info" />
		</td>
	</tr>
	<tr>
		<td>
			Get all Peptides with Pattern :
		</td>
		<td>
			${form.peptide_pattern} 
		</td>
		<td>
			<input type="submit" name="button_peptide_pattern" value="Get PatternPeptides" />
		</td>
	</tr>
	<tr>
		<td> * * * * *
		</td>
	</tr>
	<tr>
		<td> SOURCE
		</td>
	</tr>
	<tr>
		<td>
			Show details of source : 
		</td>
		<td>
			${form.source_detail}
		</td>
		<td>
			<input type='submit' name='button_source_detail' value='Source details'>
		</td>
	</tr>
	<tr>
		<td>
			Show peptides of source : 
		</td>
		<td>
			${form.source_peptides}
		</td>
		<td>
			<input type='submit' name='button_source_peptides' value='Source peptides'>
		</td>
	</tr>
	
</table>
<br><br><br>

<input type='submit' name='button_get_mining_csv' value='Get mining csv'>



</form>

<style type="text/css">
td {
	height:30px;
}

a {
	text-decoration:none;
}
</style>