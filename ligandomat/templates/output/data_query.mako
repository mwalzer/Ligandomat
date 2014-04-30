<%inherit file='ligandomat:templates/layout.mako'/>

<html xmlns="http://www.w3.org/1999/html">
<head>
<title>data_query</title>
<script src="../../static/jquery-2.1.0.js"></script>

<script>

    ## Combines all query inputs
        function combine_peptide_query() {
    var element_values = ["sequence_input", "run_name_input", "source_name_input", "organ_input", "tissue_input",
        "dignity_input", "researcher_input", "source_hla_typing_input", "ionscore_input",
        "e_value_input", "q_value_input"];
    var values_string = "{";
    for (var i = 0; i < element_values.length; i++){
        if (document.getElementById(element_values[i]) != null) {
            values_string = values_string + "'" + element_values[i] + "':'" + document.getElementById(element_values[i]).value + "',";
        }
    }
    values_string = values_string.substring(0, values_string.length - 1)
    document.getElementById("search").value = values_string + "}";
    }

    function combine_run_name_source_query(){
        if (document.getElementById("filter_list_box") != null){
            ## Which query?
            if (document.getElementById("search_run_name_id") != null){
                var element_values = ["run_name", "ionscore_input","e_value_input", "q_value_input"];
            }
            else if (document.getElementById("search_source_id") != null){
                var element_values = ["source", "ionscore_input","e_value_input", "q_value_input"];
            }
            ## Get the items
            var values_string = "{";
            for (var i = 0; i < element_values.length; i++){
                if (document.getElementById(element_values[i]) != null) {
                   values_string = values_string + "'" + element_values[i] + "':'" + document.getElementById(element_values[i]).value + "',";
               }
            }
            ## set the values
            if (document.getElementById("search_run_name_id") != null){
                document.getElementById("search_run_name_id").value = values_string + "}";
            }
            else if (document.getElementById("search_source_id") != null){
                document.getElementById("search_source_id").value = values_string + "}";
            }
        }else{
            if (document.getElementById("run_name") != null){
                 document.getElementById("search_run_name_id").value = document.getElementById("run_name").value;
        }
        if (document.getElementById("source") != null){
                 document.getElementById("search_source_id").value = document.getElementById("source").value;
        }
        }


    }

    function run_name_query_creator(){
        if (document.getElementById("run_name") != null){
                 document.getElementById("search_run_name_id").value = document.getElementById("run_name").value;
        }
    }

    function source_query_creator(){
        if (document.getElementById("source") != null){
                 document.getElementById("search_source_id").value = document.getElementById("source").value;
        }
    }

    function add_filter(){
    $(document).ready(function(){
                if (document.getElementById("filter_list_box") != null) {
                            document.getElementById("filter_list_box").remove();
                }else{
                    var filter_list =
                '<fieldset id="filter_list_box">' +
                '<table style="width:400px" id="filter_list">' +
                '<tr><td><b>Filter:</b></td></tr>' +
                '<tr><td>Ion score </td><td>> </td> <td><input style="font-size:14px" id="ionscore_input" name="ionscore" type="text" value="20" /></td></tr>' +

                '<tr><td>e-Value </td><td><   </td><td><input style="font-size:14px" id="e_value_input" name="e-Value" type="text" value="1"/></td></tr>' +

                '<tr><td>q-Value </td><td><  </td> <td><input style="font-size:14px" id="q_value_input" name="q-Value" type="text" value="1" /></td></tr>' +
                '</table>' +
                '</fieldset>' +
                '</fieldset>';

                $("#source_query_box").append(filter_list);
                $("#run_name_query_box").append(filter_list);


                }

            }

    )
    }


    ## Selects the query type
        function select_query_type() {
    $(document).ready(function () {
                var e = document.getElementById("query_type");
                var strUser = e.options[e.selectedIndex].value;


                if (strUser == "detailed_peptide_list") {
                    if (document.getElementById("peptide_query_box") == null) {

                        if (document.getElementById("run_name_query_box") != null) {
                            document.getElementById("run_name_query_box").remove();
                        }
                        if (document.getElementById("source_query_box") != null) {
                        document.getElementById("source_query_box").remove();
                        }

                        var detailed_peptide_list =
                                '<fieldset id="peptide_query_box">' +
                                        '<fieldset id="peptide_query_box">' +
                                    <!-- Empty table which is filled with query options --> +
                                        '<table style="width:500px" id="ul_navigation">' +

                                        '<tr></tr>' +

                                        '</table>' +

                                    <!-- Select a query option menu -->
                                        '<table>' +
                                        '    <tr><td>' +
                                        '<select id="query" style="font-size:14px" name="query">' +
                                        '    <option value="sequence" selected="selected">Sequence</option>' +
                                        '    <option value="run_name">Run name</option>' +
                                        '    <option value="source_name">Source name</option>' +
                                        '    <option value="organ">Organ</option>' +
                                        '    <option value="tissue">Tissue</option>' +
                                        '    <option value="dignity">Dignity</option>' +
                                        '    <option value="researcher">Researcher</option>' +
                                        '    <option value="source_hla_typing">Source hla typing</option>' +

                                        '</select></td><td>' +
                                    <!-- Add button. Uses the appendCriteria() js function-->
                                        '<input type="image" src="../../static/plus.png" height="22" onclick="appendCriteria()" id="append_criteria">' +
                                        '    </td>' +
                                        '<td width ="150"></td>' +


                                        '<td>' +
                                        '    <form method="post" action=query name="query">' +
                                    <!-- Starts the query -->
                                        '    <input style="font-size:14px" value = "Search Database" onclick = "combine_peptide_query()"  id="search" type="submit" name="search" >' +
                                        '        </form>' +

                                        '</td>' +

                                        '    </tr>' +
                                        '</table>' +
                                        '    </fieldset>' +
                                        '<br><br>' +

                                    <!-- Filter criteria -->
                                        '<fieldset id="filter_list_box">' +
                                        '<table style="width:400px" id="filter_list">' +
                                        '<tr><td><b>Filter:</b></td></tr>' +
                                        '<tr><td>Ion score </td><td>> </td> <td><input style="font-size:14px" id="ionscore_input" name="ionscore" type="text" value="20" /></td></tr>' +

                                        '<tr><td>e-Value </td><td><   </td><td><input style="font-size:14px" id="e_value_input" name="e-Value" type="text" value="1"/></td></tr>' +

                                        '<tr><td>q-Value </td><td><  </td> <td><input style="font-size:14px" id="q_value_input" name="q-Value" type="text" value="1" /></td></tr>' +
                                        '</table>' +
                                        '</fieldset>' +
                                        '</fieldset>';
                        ##detailed_peptide_list.insertAfter($("#query_type_box"));
                        $("#query_type_box").append(detailed_peptide_list);
                        ##$("fieldset:first").append(detailed_peptide_list);
                        }

                } else if (strUser == "Run_information") {
                    ## Remove already selected types
                    if (document.getElementById("peptide_query_box") != null) {
                        document.getElementById("peptide_query_box").remove();
                    }
                    if (document.getElementById("source_query_box") != null) {
                        document.getElementById("source_query_box").remove();
                    }

                    if (document.getElementById("run_name_query_box") == null) {
                        var run_name_search = '<fieldset id="run_name_query_box">' +
                                        '<form method="post" action=query name="query_runname_name">' +
                                        '<table> <td><tr>' +
                                        '<p style="font-size:16px"> Runname:' +
                                        '<input type="text" style="font-size:16px" id="run_name">' +
                                        '<input  style="font-size:14px"  value="Search Database" onclick= "combine_run_name_source_query()" id="search_run_name_id" type="submit" name="search_run_name_name"> ' +
                                        '<input type="checkbox" name="peptide_count" value="True" onclick="add_filter()"> Count peptides'+
                                        '</p></tr></td></table>' +
                                        '</form>' +
                                        '</fieldset>';
                        $("#query_type_box").append(run_name_search);
                    }


                } else if (strUser == "Source_information") {
                    ## Remove already selected types
                    if (document.getElementById("peptide_query_box") != null) {
                        document.getElementById("peptide_query_box").remove();
                    }
                    if (document.getElementById("run_name_query_box") != null) {
                        document.getElementById("run_name_query_box").remove();
                    }

                    if (document.getElementById("source_query_box") == null) {
                        var source_search = '<fieldset id="source_query_box">' +
                                        '<form method="post" action=query name="query_source_name">' +
                                        '<table> <td><tr>' +
                                        '<p style="font-size:16px"> Source:' +
                                        '<input type="text" style="font-size:16px" id="source">' +
                                        '<input  style="font-size:14px"  value="Search Database" onclick= "combine_run_name_source_query()" id="search_source_id" type="submit" name="search_source_name"> ' +
                                        '<input type="checkbox" name="peptide_count" value="True" onclick="add_filter()"> Count peptides'+
                                        '</p></tr></td></table>' +
                                        '</form>' +

                                        '</fieldset>';
                        $("#query_type_box").append(source_search);
                    }


                }

            }
    )
}


    ## Adds the selected query to the query list
        function appendCriteria() {
    $(document).ready(function () {
                var e = document.getElementById("query");
                var strUser = e.options[e.selectedIndex].value;

                ## Add sequence query
                        if (strUser == "sequence") {
                    if ($("#sequence").length === 0) {
                        var element =

                                '<tr id = "sequence" name = "sequence">' +
                                        '<form>' +


                                        '<td>Sequence:</td> ' +
                                        '<td><input style="font-size:14px" name="sequence" id="sequence_input" type="text" /></td>' +
                                        '</form>' +

                                        '<td><input type="image" src="../../static/minus.png" height="22" id = "sequence" onclick=removeCriteria("sequence")></td>' +
                                        '</tr>';
                        $("tr:first").append(element);
                    }
                }
                    ## Add Run name query
                        else if (strUser == "run_name") {
                    if ($("#run_name").length === 0) {
                        var element = '<tr id = "run_name" name = "run_name">' +
                                '<td>Runname: </td>' +


                                '<td><input style="font-size:14px" id = "run_name_input" name="run_name" type="text" /></td>' +

                                '<td><input type="image" src="../../static/minus.png" height="22"  onclick=removeCriteria("run_name")></td>' +
                                '</tr>';
                        $("tr:first").append(element);
                    }
                }
                    ## Add source name query
                        else if (strUser == "source_name") {
                    if ($("#source").length === 0) {
                        var element = '<tr id = "source_name" name = "source">' +
                                '<td>Source name: </td>' +


                                '<td><input style="font-size:14px" id = "source_name_input" name="source_name" type="text" /></td>' +

                                '<td><input type="image" src="../../static/minus.png" height="22"  onclick=removeCriteria("source_name")></td>' +
                                '</tr>';
                        $("tr:first").append(element);
                    }
                }
                    ## Add organ query
                        else if (strUser == "organ") {
                    if ($("#organ").length === 0) {
                        var element = '<tr id = "organ" name = "organ">' +
                                '<td>Organ: </td>' +


                                '<td><input style="font-size:14px" id = "organ_input" name="organ" type="text" /></td>' +

                                '<td><input type="image" src="../../static/minus.png" height="22"  onclick=removeCriteria("organ")></td>' +
                                '</tr>';
                        $("tr:first").append(element);
                    }
                }
                    ## Add tissue query
                        else if (strUser == "tissue") {
                    if ($("#tissue").length === 0) {
                        var element = '<tr id = "tissue" name = "tissue">' +
                                '<td>Tissue: </td>' +

                                '<td><input style="font-size:14px"  id = "tissue_input" name="tissue" type="text" /></td>' +

                                '<td><input type="image" src="../../static/minus.png" height="22" onclick=removeCriteria("tissue")></td>' +
                                '</tr>';
                        $("tr:first").append(element);
                    }
                }
                    ## Add dignity query
                        else if (strUser == "dignity") {
                    if ($("#dignity").length === 0) {
                        var element = '<tr id = "dignity" name = "dignity">' +
                                '<td>Dignity: </td>' +


                                '<td><input style="font-size:14px"  id = "dignity_input" name="dignity" type="text" /></td>' +

                                '<td><input type="image" src="../../static/minus.png" height="22"  onclick=removeCriteria("dignity")></td>' +
                                '</tr>';
                        $("tr:first").append(element);
                    }
                }
                    ## Add researcher query
                        else if (strUser == "researcher") {
                    if ($("#researcher").length === 0) {
                        var element = '<tr id = "researcher" name = "researcher">' +
                                '<td>Researcher: </td>' +


                                '<td><input style="font-size:14px" id = "researcher_input" name="researcher" type="text" /></td>' +

                                '<td><input type="image" src="../../static/minus.png" height="22"   onclick=removeCriteria("researcher")></td>' +
                                '</tr>';
                        $("tr:first").append(element);
                    }
                }
                    ## Add hla typing of the source query
                        else if (strUser == "source_hla_typing") {
                    if ($("#source_hla_typing").length === 0) {
                        var element = '<tr id = "source_hla_typing" name = "source_hla_typing">' +
                                '<td>Source hla typing: </td>' +


                                '<td><input style="font-size:14px"  id = "source_hla_typing_input" name="source_hla_typing" type="text" /></td>' +

                                '<td><input type="image" src="../../static/minus.png" height="22"  onclick=removeCriteria("source_hla_typing")></td>' +
                                '</tr>';
                        $("tr:first").append(element);
                    }
                }


            }
    )
}

    ## removes the query object
        function removeCriteria(selected_id) {
    $('[id^="' + selected_id + '"]').remove();
}


</script>
</head>

<body>
<fieldset id="query_type_box">

    <select id="query_type" style="font-size:14px" name="query_type_name">
        <option value="detailed_peptide_list" selected="selected">Detailed list of peptides</option>
        <option value="Run_information">Run information</option>
        <option value="Source_information">Source information</option>
    </select>
    <input type="button" style="font-size:14px" id="query_type_selector" value="Select Type"
           onclick="select_query_type()">

</fieldset>

</body>
</html>

