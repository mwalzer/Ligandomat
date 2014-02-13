<%inherit file='ligandomat:templates/layout_wizard.mako'/>

<div id="header">
Metadata for preparation
</div>

<form method="post" >
<div id="frame">






<div class="box"id="input">

 % if (in_action == 'none') : 
 Please select 
  <input type="submit" name="button_known_prep" value="Known Prep" /> or
  <input type="submit" name="button_new_prep" value="New Prep" />
 % endif

  %if in_action == 'add_prep' :
<div align="right"><input  type="submit" name="button_known_prep" value="Go to known prep" /></div>
   <b>Information about the Prep</b><br>
  
<table>
 <tr>
    <th>Made by :  </th><th> ${form.made_by}</th>
 </tr>
 <tr>
    <th>Sample mass / volume :  </th><th>${form.sample_mass}[g/ml]</th>
 </tr>
 <tr>
    <th>Antibody :  </th><th> ${form.antibody}</th>
 </tr>
 <tr>
    <th>Antibody mass :   </th><th> ${form.antibody_mass}[mg]</th>
 </tr>
 <tr>
    <th>Magna :  </th><th>  ${form.magna}</th>
 </tr>
 <tr>
       <th>Comment : </th><th> ${form.comment2}</th>
 </tr>
 </table>
   %endif

  % if in_action == 'prep' : 
 <div align="right"><input  type="submit" name="button_new_prep" value="Go to new prep" /></div>
  <b>Select preperation</b><br>
    ${form.known_prep()} 
  % endif



</div><br><!-- end inputs-->


<div class="box" id="run_div">
  % for run_name in run_list :
    <input type="checkbox" name=${run_name}  />
    ${run_name} <br>
  % endfor
</div>
<br>
  <input type="submit" name="button_submitted_prep" value="Submit Prep" />
  <input type='submit' name='abort_upload' value='Abort Upload'/>

</div><!-- end frame-->
</form>






<style type="text/css">
 #header{
 width:800px;
 padding: 20px;
 border-width: 2px;
 border-style: solid;
 border-color: #FFFF00;
 background-color: #FDFD96;
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
 border-color: #FFFF00;
 background-color: #FDFD96;
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








