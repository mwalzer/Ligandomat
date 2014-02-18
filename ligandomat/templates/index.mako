<%inherit file='ligandomat:templates/layout.mako'/>
<script></script>



<div id="frame">
<img  class='peptide' src="${request.static_url('ligandomat:static/peptidgraubunt.jpg')}" width="120" />
<div id="welcome" align="center">

<font size="20">Welcome to Ligandomat </font>

<br>
<br>
<font size="5">Finally! </font><br>
<br>
This is the (temporary) final version of the Ligandomat.
<br>
Feel free to use gently!<br>
<br>
If you have any questions visit the help site.<br>
In case it does not help, rethink.<br>
<br>
<br>
<br>
<br>
<i>

The Ligandomat finds,<br>
what the elk binds!<br>
</i>
<br>
Hit <a href="${request.route_url('login')}">Login</a><br>
<br>

</div>
<img  class='peptide'src="${request.static_url('ligandomat:static/peptidgraubunt.jpg')}" width="120" />

</div>



<style type="text/css">

.peptide {
  float : left;
  margin-top : 20px;
  position : relative;
}

#welcome {
  float : left;
  width : 700px;
  margin: 20px;
  padding : 20px;
  background-color : #DDDDDD;
}


#frame{
  position: relative;
  left : 50%;
  margin-left:-325px;
}



</style>



