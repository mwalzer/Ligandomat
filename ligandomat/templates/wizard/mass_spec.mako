<%inherit file='ligandomat:templates/layout_wizard.mako'/>

<div id="header">
Metadata for mass spectrometry run
</div>

<form method="post" >
<div id="frame">


<div class="box"id="input">


 <b>Massspectrometry attributes</b><br>
<table>
 <tr>
    <th>Made by :  </th><th> ${form.made_by}</th>
 </tr>
 <tr>
    <th>Date :  </th><th> ${form.run_date}</th>
 </tr>
 <tr>
    <th>Sample share : </th><th> ${form.sample_share}[%]</th>
 </tr>
 <tr>
    <th>Method : </th><th> ${form.method}</th>
 </tr>
 <tr>
    <th>Modification : </th><th> ${form.modification}    </th>
 </tr>
 <tr>
    <th>Comment : </th><th> ${form.comment3}</th>
 </tr>
 </table>
 
</div><br><!-- end inputs-->


<div class="box" id="run_div">
  % for run_name in run_list :
    <input type="checkbox" name=${run_name}  />
    ${run_name} <br>
  % endfor
</div>
<br>
  <input type="submit" name="button_submitted_mass_spec" value="Submit MS" />
  <input type='submit' name='abort_upload' value='Abort Upload'/>

</div><!-- end frame-->
</form>






<style type="text/css">
 #header{
 width:800px;
 padding: 20px;
 border-width: 2px;
 border-width: 2px;
 border-style: solid;
 border-color: #FF0000;
 background-color: #F78181;
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
 border-color: #FF0000;
 background-color: #F77777;
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








