<%inherit file='ligandomat:templates/layout_wizard.mako'/>
<form method="post" >
OWERVIEW :<br>
<br>
Finally you have entered all data - hopefully correct... <br>
Please check all data once again and then you can upload them! <br>
<br>

<table>

<tr>
%for col in table[0].keys() :
	<th>| ${col} |</th>
%endfor
</tr>

 % for dict in table :
	<tr>
	% for key in dict :
		<td>
			${dict[key]}
		</td>
	%endfor
	</tr>
%endfor
 
 </table>
 
<div id='buttonDiv'>
<br>
<input type='submit' name='submit_upload' value='Submit Upload!'/>
<input type='submit' name='reject_upload' value='Reject Upload!'/>
<br>
</div>

</form>
<style type="text/css">

#wholeData{
float:left;


}

.dataRow{
 height:300px;
 margin-button : 10px;
}

#buttonDiv{
 padding : 10px;
position : absolute;
margin-left : 400px;
}


#runBlock{
  padding : 10px;
  margin-right : 10px;
}

.dataBlock{
  background-color: #FAFAFA;
  float : left;
  padding : 10px;
  margin-right : 10px;
}

.new{
  border-color : red;
  border-width : 0px 0px 2px 0px;
  border-style : solid;
  margin-button : -2px;
}


</style>




