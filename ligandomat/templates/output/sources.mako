<%inherit file='ligandomat:templates/layout.mako'/>


<form>
--- ${message} --- <br>
<br>


<table>

	% for item in table :
	<tr>
		<td>${item}</td>
		
	</tr>
	%endfor
	
 </table>
<input type='submit' name='button_change_source' value='Change Source'/>

</form>

<style type="text/css">

</style>


