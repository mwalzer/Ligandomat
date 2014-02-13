<%inherit file='ligandomat:templates/layout.mako'/>
<script></script>

<div id='infobox'>

	<div id='fyi'>
		FYI
	</div>

	${message}

</div>

<div id='imagebox'>
% if image == 'stop' :
	<img class='infoimg' src="${request.static_url('ligandomat:static/stopthink.jpg')}" width="200" />
% endif
% if image == 'onejob' :
	<img class='infoimg' src="${request.static_url('ligandomat:static/onejobtoilet.jpg')}" width="300" />
% endif
</div>


<style type="text/css">

#infobox{
	position: absolute;
	margin-left : 400px;
	border-style : solid;
	border-color: red;
	border-width:5px;
	padding : 20px;
	width: 400px;
	float : left;
}

a{
	text-decoration : none;
}

#imagebox {
	position: absolute;
	float:left;
}

#fyi {
	align:center;
	height:50px;
	
	text-align: center;
	font-size: 30px;
}
</style>