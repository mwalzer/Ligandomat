<%inherit file='ligandomat:templates/layout_wizard.mako'/>

<div id="header">
Metadata for source
</div>

<form method="post" >
<div id="frame">




<div class="box" id="input">

 % if ( in_action == 'none') : 
  Please select 
  <input type="submit" name="button_known_source" value="Known source" /> or 
  <input type="submit" name="button_new_source" value="New source" />
 % endif
 
%if in_action == 'add_source' :
<div align="right"><input type="submit" name="button_known_source" value="Go to Known source" /></div>
  <b>Information about the Source</b><br>
<table>
 <tr>
    <th>New Source : </th><th>${form.new_source}</th>
 </tr>
 <tr>
    <th>Organ : </th><th>${form.organ}</th>
 </tr>
 <tr>
    <th>Organism : </th><th>${form.organism}</th>
 </tr>
 <tr>
    <th>Tissue : </th><th>${form.tissue}</th>
 </tr>
 <tr>
    <th>Dignity : </th><th>${form.dignity}</th>  
 </tr>
 <tr>
    <th>Cell Type : </th><th>${form.cell_type}</th>
 </tr>
 <tr>
    <th>Comment : </th><th>${form.comment1}</th>
 </tr>
</table><br>

    
  <div  id="hla_box">
  <b>Expressed HLAs</b><br>
     <select name='select_hla' size="1">
      % for allele in list_hlas :
      <option>${allele}</option>
      % endfor 
    </select>
    ${form.hla_allele} 
    <input type="submit" name="button_add_hla" value="Add" /> <input type="submit" name="button_delete_hla" value="Delete last" /><br>
     
    You selected ${num_hla} HLAs: <br>
     % if not num_hla == 0 : 
      % for i in range(0, num_hla) :
        %if len(form.HLAs[i][1]) > 0 :
		${form.HLAs[i][0]}:${form.HLAs[i][1]}
	% else :
		${form.HLAs[i][0]}${form.HLAs[i][1]}
	%endif
        % if i != num_hla-1 :
          //
        % endif  
      % endfor
     % endif 
  </div> <!-- end hla_box -->

%endif <!-- end add_source -->

% if in_action == 'source' : 
 <div align="right"><input  type="submit" name="button_new_source" value="Go to new source" /></div>
<b>Select Source</b><br>
    Known Source : ${form.known_sources()} <br>
% endif


</div><br><!-- end inputs -->

<div class="box" id="run_div">
  % for run_name in run_list :
    <input type="checkbox" name=${run_name} />
    ${run_name} <br>
  % endfor
</div><br>

<input type="submit" name="button_submit" value="Submit source" />
<input type="submit" name="abort_upload" float="right" value="Abort Upload!"/>
</div>  <!-- end frame -->

</form>




<style type="text/css">
 #header{
 width:800px;
 padding: 20px;
 border-width: 2px;
 border-width: 2px;
 border-style: solid;
 border-color: #0000FF;
 background-color: #819FF7;
 text-align : center;
 font-style:oblique;
 font-size:24px;
}

#frame {
 float:left;
 margin:30px 0px;
 padding: 20px;
 width: 800px;
 border-width: 2px;
 border-style: solid;
 border-color: #0000FF;
 background-color: #819FF7;
}

/*  inputs  */

#selectBox{
 float:right-top;
 background-color : blue;
}

table {
 
}

.box {
 padding:10px;
 margin:5px;
 border-width: 1px;
 border-style: solid;
 border-color: #888888;
 background-color: #E8E8E8;
}

#hla_box {
 height: 120px;
}

th{
 text-align : left;	
 font-weight: normal;
}
    

</style>














