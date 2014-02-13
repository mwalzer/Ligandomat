<%inherit file='ligandomat:templates/layout.mako'/>



--- ${message} --- <br>
<br>

%for info in table[len(table)-1] :
	%if info != 'cols' :
		${info}  : ${table[len(table)-1][info] }<br>
	%endif
%endfor
<br>

<table>

<tr>
%for col in table[len(table)-1]['cols'] :
	<th>| ${col} |</th>
%endfor
</tr>

 % for i in range(0, len(table)-1) :
	<tr>
	% for col in table[len(table)-1]['cols']:
		<td> 
			%if col != 'typings' :
				${table[i][col]}
			%else :
				%for j in range(0, len(table[i][col])) :
					${table[i][col][j]}
					%if j < len(table[i][col])-1 :
						/
					%endif
				%endfor
			%endif
					
		</td>
	%endfor
	</tr>
%endfor
 
 </table>

<style type="text/css">
#runBlock{
  padding : 10px;
  
  margin: 0px 0px 10px 0px ;
  border-style : solid;
  border-width : 2px;
  border-color : blue;
  float:left;
}

.dataBlock{
  background-color: #FAFAFA;
  float : left;
  padding : 10px;
  margin-right : 10px;
}
</style>


