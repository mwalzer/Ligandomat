<%inherit file='ligandomat:templates/layout.mako'/>
<html >
<head>
    <title>test</title>
    <script src="../../static/jquery-2.1.0.js"></script>

    <script>
        function appendCriteria() {
            $(document).ready(function () {
                        var e = document.getElementById("query");
                        var strUser = e.options[e.selectedIndex].value;

                        if (strUser == "sequence") {
                            if ($("#sequence").length === 0) {
                                var element =
                                        '<tr id = "sequence" name = "sequence">' +

                                                '<td>Sequence:</td> '+
                                        '<td><input style="font-size:14px" name="sequence" type="text" /></td>' +

                                        '<td><input type="image" src="../../static/minus.png" height="22" id = "sequence" onclick=removeCriteria("sequence")></td>' +
                                '</tr>';
                                $("tr:first").append(element);
                            }
                        }
                        else if (strUser == "run_name") {
                            if ($("#run_name").length === 0) {
                                var element = '<tr id = "run_name" name = "run_name">' +
                                        '<td>Runname: </td>'+


                                        '<td><input style="font-size:14px" name="run_name" type="text" /></td>' +

                                        '<td><input type="image" src="../../static/minus.png" height="22" id = "run_name" onclick=removeCriteria("run_name")></td>' +
                                        '</tr>';
                                $("tr:first").append(element);
                            }
                        }
                        else if (strUser == "source_name") {
                            if ($("#source").length === 0) {
                                var element = '<tr id = "source_name" name = "source">' +
                                        '<td>Source name: </td>'+


                                        '<td><input style="font-size:14px" name="source_name" type="text" /></td>' +

                                        '<td><input type="image" src="../../static/minus.png" height="22" id = "source_name" onclick=removeCriteria("source_name")></td>' +
                                        '</tr>';
                                $("tr:first").append(element);
                            }
                        }
                        else if (strUser == "organ") {
                            if ($("#organ").length === 0) {
                                var element = '<tr id = "organ" name = "organ">' +
                                        '<td>Organ: </td>'+


                                        '<td><input style="font-size:14px" name="organ" type="text" /></td>' +

                                        '<td><input type="image" src="../../static/minus.png" height="22" id = "organ" onclick=removeCriteria("organ")></td>' +
                                        '</tr>';
                                $("tr:first").append(element);
                            }
                        }
                        else if (strUser == "tissue") {
                            if ($("#tissue").length === 0) {
                                var element = '<tr id = "tissue" name = "tissue">' +
                                        '<td>Tissue: </td>'+

                                        '<td><input style="font-size:14px" name="tissue" type="text" /></td>' +

                                        '<td><input type="image" src="../../static/minus.png" height="22" id = "tissue" onclick=removeCriteria("tissue")></td>' +
                                        '</tr>';
                                $("tr:first").append(element);
                            }
                        }
                        else if (strUser == "dignity") {
                            if ($("#dignity").length === 0) {
                                var element = '<tr id = "dignity" name = "dignity">' +
                                        '<td>Dignity: </td>'+


                                        '<td><input style="font-size:14px" name="dignity" type="text" /></td>' +

                                        '<td><input type="image" src="../../static/minus.png" height="22"  id = "dignity" onclick=removeCriteria("dignity")></td>' +
                                        '</tr>';
                                $("tr:first").append(element);
                            }
                        }
                        else if (strUser == "researcher") {
                            if ($("#researcher").length === 0) {
                                var element = '<tr id = "researcher" name = "researcher">' +
                                        '<td>Researcher: </td>'+


                                        '<td><input style="font-size:14px" name="researcher" type="text" /></td>' +

                                        '<td><input type="image" src="../../static/minus.png" height="22"  id = "researcher" onclick=removeCriteria("researcher")></td>' +
                                        '</tr>';
                                $("tr:first").append(element);
                            }
                        }
                        else if (strUser == "source_hla_typing") {
                            if ($("#source_hla_typing").length === 0) {
                                var element = '<tr id = "source_hla_typing" name = "source_hla_typing">' +
                                        '<td>Source hla typing: </td>'+


                                        '<td><input style="font-size:14px" name="source_hla_typing" type="text" /></td>' +

                                        '<td><input type="image" src="../../static/minus.png" height="22"  id = "source_hla_typing" onclick=removeCriteria("source_hla_typing")></td>' +
                                        '</tr>';
                                $("tr:first").append(element);
                            }
                        }


                    }
            )
        }

        function removeCriteria(selected_id) {
            $('[id^="' + selected_id + '"]').remove()
        }


    </script>


</head>

<body>
<table style="width:500px" id="ul_navigation">
    <tr></tr>

</table>
<table>
    <tr><td>
<select id="query" style="font-size:14px" name="query">
    <option value="sequence" selected="selected">Sequence</option>
    <option value="run_name">Run name</option>
    <option value="source_name">Source name</option>
    <option value="organ">Organ</option>
    <option value="tissue">Tissue</option>
    <option value="dignity">Dignity</option>
    <option value="researcher">Researcher</option>
    <option value="source_hla_typing">Source hla typing</option>

</select></td><td>
<input type="image" src="../../static/plus.png" height="22" onclick="appendCriteria()">
    </td>
<td width ="150"></td>
<td>
    <input style="font-size:14px" value="Search Database" type="submit" name="search" >
</td>

    </tr>
</table>
<br><br>
<hr width="100%"><br>
<table style="width:400px" id="filter_list">
<tr><td><b>Filter:</b></td></tr>
<tr><td>Ion score </td><td>< </td> <td><input style="font-size:14px" name="ionscore" type="text" value="20" /></td></tr>

<tr><td>e-Value </td><td><   </td><td><input style="font-size:14px" name="e-Value" type="text" value="1"/></td></tr>

<tr><td>q-Value </td><td><  </td> <td><input style="font-size:14px" name="q-Value" type="text" value="1" /></td></tr>


</table>



</body>
</html>

