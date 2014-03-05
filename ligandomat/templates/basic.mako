##<%inherit file='ligandomat:templates/layout.mako'/>
##<script></script>

<head>
<title>test</title>
<link type="text/css" href="static/query.css" rel="stylesheet">

</head>


<body>
<div id='header'>
    <picfloatL><img src="elch_logo.jpg" height="100" /></picfloatL>
    <span>Ligandosphere</span>
    <picfloatR><img src="logo-uni-tuebingen.png" height="100" /></picfloatR>
    </div>

<p></p>

<div id='navigation' >
<h3>
<a href="/" >Start</a>&nbsp;&nbsp;&nbsp;
<a href="query" >Database</a>&nbsp;&nbsp;&nbsp;
<a href="prediction" >Peptide Prediction</a>&nbsp;&nbsp;&nbsp;
<a href="hlatyping"> HLA Typing </a>&nbsp;&nbsp;&nbsp;
<!--<a href="http://192.168.123.136:9999/Mslots">Mascot slots status</a>&nbsp;&nbsp;&nbsp;-->
<a href="http://192.168.123.136/mascot/x-cgi/ms-status.exe">Mascot slots status</a>&nbsp;&nbsp;&nbsp;
<a href="http://192.168.123.136:9999/Mupdate">Mascot slot update</a></h3>
</div>

<div id='content'>
<form action="/query" method="post">
  <table >

   <!-- SEARCH FOR A SEQUENCE -->
   <!--
   <tr>
   <td>Search for a sequence:</td>
   <td><input  style="font-size:14px" name="sequence" type="text" /></td>
   </tr>

   <tr>
   <td>Sort the result by: <select style="font-size:14px" name="sorting_seq">
       <option value="sequence" selected="selected">sequence</option>
       <option value="sourcename">source</option>
       <option value="runname">runname</option>
       </select></td>
   <td><input style="font-size:14px" value="Go!" type="submit", name="search_by_seq" /></td>
   </tr>

   <td>&nbsp;</td>
   -->

   <!-- SEARCH FOR A SUBSEQUENCE -->
   <tr>
   <td>Search for a sequence:</td>
   <td><input style="font-size:14px" name="subsequence" type="text" /></td>
   </tr>

   <tr>
   <td>Sort the result by: <select style="font-size:14px" name="sorting_pat">
       <option value="sequence" selected="selected">sequence</option>
       <option value="sourcename">source</option>
       <option value="runname">runname</option>
       </select></td>
   <td><form>
    <p>
    <input type="button" name="wildcard-info" value="Wildcard Info"
  onclick="alert('For each character use _ as wildcard, for many characters use % as wildcard');">
    </p>
    </form>
    <input style="font-size:14px" value="Go!" type="submit", name="search_by_subsequence" /></td>
   </tr>

   <td>&nbsp;</td>

    <!-- SEARCH FOR MS_RUNS -->
   <tr>
   <td>Search for ms_runs:</td>

   <td><input style="font-size:14px" name="runname_subsequence" type="text" /></td>
   </tr>

   <tr>
   <td>Sort the result by: <select style="font-size:14px" name="sorting_runname">
       <option value="sequence" selected="selected">sequence</option>
       <option value="sourcename">source</option>
       <option value="runname">runname</option>
       </select></td>
   <td><form>
    <p>
    <input type="button" name="wildcard-info" value="Wildcard Info"
  onclick="alert('For each character use _ as wildcard, for many characters use % as wildcard');">
    </p>
    </form><input style="font-size:14px" value="Go!" type="submit", name="search_by_runname" /></td>
   </tr>


   <td>&nbsp;</td>

        <!-- SEARCH FOR organ -->
   <tr>
   <td>Search for organ:</td>

   <td><input style="font-size:14px" name="organ_subsequence" type="text" /></td>
   </tr>

   <tr>
   <td>Sort the result by: <select style="font-size:14px" name="sorting_organ">
       <option value="sequence" selected="selected">sequence</option>
       <option value="sourcename">source</option>
       <option value="runname">runname</option>
       </select></td>
   <td><form>
    <p>
    <input type="button" name="wildcard-info" value="Wildcard Info"
  onclick="alert('For each character use _ as wildcard, for many characters use % as wildcard');">
    </p>
    </form><input style="font-size:14px" value="Go!" type="submit", name="search_by_organ" /></td>
   </tr>



   <td>&nbsp;</td>
    <!-- SEARCH FOR tissue -->
   <tr>
   <td>Search for tissue:</td>

   <td><input style="font-size:14px" name="tissue_subsequence" type="text" /></td>
   </tr>

   <tr>
   <td>Sort the result by: <select style="font-size:14px" name="sorting_tissue">
       <option value="sequence" selected="selected">sequence</option>
       <option value="sourcename">source</option>
       <option value="runname">runname</option>
       </select></td>
   <td><form>
    <p>
    <input type="button" name="wildcard-info" value="Wildcard Info"
  onclick="alert('For each character use _ as wildcard, for many characters use % as wildcard');">
    </p>
    </form><input style="font-size:14px" value="Go!" type="submit", name="search_by_tissue" /></td>
   </tr>



   <td>&nbsp;</td>

    <!-- SEARCH FOR ALL PEPTIDES -->
    <tr>
   <td>Get all peptides from the database:</td>
   <td><input style="font-size:14px" value="Go!" type="submit", name="search_all" /></td>
   </tr>

   </table>
</form>
</div>
    <p>&nbsp;</p>
</body>
