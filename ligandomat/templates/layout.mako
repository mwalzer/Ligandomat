
<html>
<head>
<title>Ligandomat</title>
<!<link rel="stylesheet" type="text/css" href="${request.static_url('ligandomat:static/wizard.css')}" />
</head>





<body>
<div id='header'>
<img id="logo" src="${request.static_url('ligandomat:static/elch_logo.jpg')}" width="70" />



<div id='headertext'>
User currently logged in : ${logged_in} <br>

% if (str(logged_in) == "None") :
<a class="logbutton"  href="${request.route_url('login')}"><input type='button' value='Login'></a>
% else :
<a class="logbutton" href="${request.application_url}/logout"><input type='button' value='Logout'></a>
% endif
<br>
</div>
</div><!-- end header-->


<div id="wizard">
${next.body()}
<div>

</body>

</html>



<style type="text/css">

#logo {
 position:absolute;
 margin: 10px;
}

.logbutton{
 float:right;
}


#wizard{
 position:absolute;
 margin-top: 20px;
 margin-left:70px;
}

#headertext{
 padding : 20px;
 float: right;
 margin-right:50px;

}

#header{
 margin : -5px;
 border-style : solid;
 border-width : 0px 0px 2px 0px;
 border-color : black;
 height: 100px
}

</style>


