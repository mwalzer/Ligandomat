
<html>
<head>
<title>Ligandomat</title>
<!--link rel="stylesheet" type="text/css" href="${request.static_url('ligandomat:static/wizard.css')}" />  -->
</head>





<body>
<div id="wizard_frame">
 <img id="logo" src="${request.static_url('ligandomat:static/elch_logo.jpg')}" width="50" /><br>
 <div class='linkbox'>
	<a href="${request.route_url('wizard_help')}">HELP</a>
 </div>
  <img  id='peptide' src="${request.static_url('ligandomat:static/peptidgraubunt.jpg')}" width="120" />
</div>
<div id="wizard">
${next.body()}
<div>

</body>

</html>



<style type="text/css">
.linkbox{
	margin-top:5px;
	padding:5px;
	width:100px;
	font-size:16px;
	border-style:solid;
	border-width:1px;
	border-color:#888888;
	background-color:#E8E8E8;
}

a{
	color:black;
	text-decoration:none;

}

a:hover{
	color:red;
	
}

#peptide{
	margin-top:20px;
}

#wizard_frame {
	text-align:center;
	position : absolute;
	float:left;
	margin:20px;
	width: 120px;
	border-style:solid;
	border-width:0px;
	border-color:#DDDDDD;
	padding:10px;

}

#wizard{
	float:left;
	position:relative;
	left : 50%;
	margin-left : -400px;
	margin-top: 20px;
}

</style>


