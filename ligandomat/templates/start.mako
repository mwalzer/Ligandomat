<%inherit file='ligandomat:templates/layout.mako'/>
<script></script>

<div>
<font size="5">Hello ${logged_in}! </font><br>


<br><br>
</div>


<table>
	<tr>
		<td><a href=${request.route_url('upload', action='load_list', attach='_')}><input type='button' value='Upload'></a></td>
		<td>You have collected some sequence data via MS? <br> Please, upload them straight away - our data base is hungry!</td>
	</tr>
	<tr>
		<td><a href=${request.route_url('data_access', action='query')}><input type='button' value='Data access'></a></td>
		<td>Gain deep knowledge of cells' ligandome!<br> Here you access our data base</td>
	</tr>

</table>


<style type="text/css">

td {
  height: 50px;
  padding-left : 20px;
}

a {
  text-decoration : none;
}

</style>

