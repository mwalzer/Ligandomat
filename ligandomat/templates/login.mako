<%inherit file='ligandomat:templates/layout.mako'/>




<div id="border1">

<div id="border2">

<div id="border3">

<div id="login">
          <font size="5">Login </font>
	  <br>	${message}
	<br>
	<br>
        <form action="${url}" method="post">
          <input type="hidden" name="came_from" 
		 value="${came_from}"/>
          <input type="text" name="login" 
		 value="${login}"/><br/>
          <input type="password" name="password"
                 value="${password}"/><br/>
		<br>
          <input type="submit" name="form.submitted" value="ok"/>
        </form>
	
</div>
	
</div></div></div>


<style type="text/css">


#login{
  
  margin-left : -200px;
  width : 400px;
  margin: 20px;
  padding : 20px;
  background-color : #DDDDDD;
}


#border1{
	float : left;
	position : relative;
	left : 50%;
	padding:2px;
	background-color: #F77777;
}

#border2{
	position: relative;
	padding:2px;
	background-color: #FDFD96;
}
#border3{
position: relative;
	padding:20px;
	background-color: #819FF7;
}



</style>
