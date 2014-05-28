<%inherit file='ligandomat:templates/layout.mako'/>

<html xmlns="http://www.w3.org/1999/html">
<head>
<title>data_query</title>
<script src="../../static/jquery-2.1.0.js"></script>

<script>
var prediction_code =
        '<optgroup label="HLA-A">' +
                '<option value="A*01:01">A*01:01</option>' +
                '<option value="A*02:01">A*02:01</option>' +
                '<option value="A*02:02">A*02:02</option>' +
                '<option value="A*02:03">A*02:03</option>' +
                '<option value="A*02:06">A*02:06</option>' +
                '<option value="A*02:11">A*02:11</option>' +
                '<option value="A*02:12">A*02:12</option>' +
                '<option value="A*02:16">A*02:16</option>' +
                '<option value="A*02:17">A*02:17</option>' +
                '<option value="A*02:19">A*02:19</option>' +
                '<option value="A*02:50">A*02:50</option>' +
                '<option value="A*03:01">A*03:01</option>' +
                '<option value="A*11:01">A*11:01</option>' +
                '<option value="A*23:01">A*23:01</option>' +
                '<option value="A*24:02">A*24:02</option>' +
                '<option value="A*24:03">A*24:03</option>' +
                '<option value="A*25:01">A*25:01</option>' +
                '<option value="A*26:01">A*26:01</option>' +
                '<option value="A*26:02">A*26:02</option>' +
                '<option value="A*26:03">A*26:03</option>' +
                '<option value="A*29:02">A*29:02</option>' +
                '<option value="A*30:01">A*30:01</option>' +
                '<option value="A*30:02">A*30:02</option>' +
                '<option value="A*31:01">A*31:01</option>' +
                '<option value="A*32:01">A*32:01</option>' +
                '<option value="A*32:07">A*32:07</option>' +
                '<option value="A*32:15">A*32:15</option>' +
                '<option value="A*33:01">A*33:01</option>' +
                '<option value="A*33:03">A*33:03</option>' +
                '<option value="A*66:01">A*66:01</option>' +
                '<option value="A*68:01">A*68:01</option>' +
                '<option value="A*68:02">A*68:02</option>' +
                '<option value="A*68:23">A*68:23</option>' +
                '<option value="A*69:01">A*69:01</option>' +
                '<option value="A*80:01">A*80:01</option>' +
                '</optgroup>' +
                '<optgroup label="HLA-B">' +
                '<option value="B*07:02">B*07:02</option>' +
                '<option value="B*08:01">B*08:01</option>' +
                '<option value="B*08:02">B*08:02</option>' +
                '<option value="B*08:03">B*08:03</option>' +
                '<option value="B*13:02">B*13:02</option>' +
                '<option value="B*14:02">B*14:02</option>' +
                '<option value="B*15:01">B*15:01</option>' +
                '<option value="B*15:02">B*15:02</option>' +
                '<option value="B*15:03">B*15:03</option>' +
                '<option value="B*15:09">B*15:09</option>' +
                '<option value="B*15:10">B*15:10</option>' +
                '<option value="B*15:16">B*15:16</option>' +
                '<option value="B*15:17">B*15:17</option>' +
                '<option value="B*18:01">B*18:01</option>' +
                '<option value="B*27:05">B*27:05</option>' +
                '<option value="B*27:09">B*27:09</option>' +
                '<option value="B*27:20">B*27:20</option>' +
                '<option value="B*35:01">B*35:01</option>' +
                '<option value="B*35:03">B*35:03</option>' +
                '<option value="B*37:01">B*37:01</option>' +
                '<option value="B*38:01">B*38:01</option>' +
                '<option value="B*39:01">B*39:01</option>' +
                '<option value="B*39:02">B*39:02</option>' +
                '<option value="B*40:01">B*40:01</option>' +
                '<option value="B*40:02">B*40:02</option>' +
                '<option value="B*40:13">B*40:13</option>' +
                '<option value="B*41:01">B*41:01</option>' +
                '<option value="B*42:01">B*42:01</option>' +
                '<option value="B*44:02">B*44:02</option>' +
                '<option value="B*44:03">B*44:03</option>' +
                '<option value="B*45:01">B*45:01</option>' +
                '<option value="B*46:01">B*46:01</option>' +
                '<option value="B*47:01">B*47:01</option>' +
                '<option value="B*48:01">B*48:01</option>' +
                '<option value="B*49:01">B*49:01</option>' +
                '<option value="B*50:01">B*50:01</option>' +
                '<option value="B*51:01">B*51:01</option>' +
                '<option value="B*53:01">B*53:01</option>' +
                '<option value="B*54:01">B*54:01</option>' +
                '<option value="B*57:01">B*57:01</option>' +
                '<option value="B*58:01">B*58:01</option>' +
                '<option value="B*58:02">B*58:02</option>' +
                '<option value="B*73:01">B*73:01</option>' +
                '<option value="B*83:01">B*83:01</option>' +
                '</optgroup>' +
                '<optgroup label="HLA-C">' +
                '<option value="C*03:03">C*03:03</option>' +
                '<option value="C*04:01">C*04:01</option>' +
                '<option value="C*05:01">C*05:01</option>' +
                '<option value="C*06:01">C*06:01</option>' +
                '<option value="C*06:02">C*06:02</option>' +
                '<option value="C*07:01">C*07:01</option>' +
                '<option value="C*07:02">C*07:02</option>' +
                '<option value="C*08:02">C*08:02</option>' +
                '<option value="C*12:03">C*12:03</option>' +
                '<option value="C*14:02">C*14:02</option>' +
                '<option value="C*15:02">C*15:02</option>' +
                '</optgroup>' +
                '<optgroup label="HLA-E">' +
                '<option value="E*01:01">E*01:01</option>' +
                '</optgroup>' +
                '</select>' +
                '</td>'


    ## Help alert box
    function help_alert(s) {
    if (s == "select_help") {
        alert("Please select a type of output: \n -Detailed list of peptides = Returns a table of peptides \n -Run information = Get information about your MS run \n -Source information = Get information about your source");
    } else if (s == "filter_help") {
        alert("The filter section avoids unsignificant hits in the results.\n\nSetting loose filter parameters results in longer computation times.");
    } else if (s == "add_criteria_help") {
        alert("Choose a parameter out of the list and add it.\n\nYou can combine all parameters with each other.");
    } else if (s == "source_hla_typing_help") {
        alert("The HLA-Typing does NOT allow wildcards!\nExamples:\nA*01\nA*02:01\nA*02:101:01:02N");
    }


}

    ## Combines all query inputs
        function combine_peptide_query() {
    var element_values = ["sequence_input", "sequence_logic",
        "run_name_input", "run_name_logic",
        "source_name_input", "source_name_logic",
        "organ_input", "organ_logic",
        "tissue_input", "tissue_logic",
        "dignity_input", "dignity_logic",
        "researcher_input", "researcher_logic",
        "source_hla_typing_input", "source_hla_typing_logic",
        "protein_input", "protein_logic",
        "netMHC_information", "netMHC_input", "netMHC_logic", "netMHC_comparison",
        "syfpeithi_information", "syfpeithi_input", "syfpeithi_logic", "syfpeithi_comparison",
        "prediction_information",
        "aa_length_start","aa_length_end",
        "ionscore_input", "q_value_input"];
    var values_string = "{";
    for (var i = 0; i < element_values.length; i++) {
        if (document.getElementById(element_values[i]) != null) {
            values_string = values_string + "'" + element_values[i] + "':'" + document.getElementById(element_values[i]).value + "',";
        }
    }
    values_string = values_string.substring(0, values_string.length - 1);
    document.getElementById("search").value = values_string + "}";
}

function combine_run_name_source_query() {
    if (document.getElementById("filter_list_box") != null) {
        ## Which query?
            var element_values = [];
        if (document.getElementById("search_run_name_id") != null) {
            element_values = ["run_name", "prediction_information", "aa_length_start","aa_length_end", "ionscore_input", "e_value_input", "q_value_input"];
        }
        else if (document.getElementById("search_source_id") != null) {
            element_values = ["source", "prediction_information", "aa_length_start","aa_length_end","ionscore_input", "e_value_input", "q_value_input"];
        }
        ## Get the items
            var values_string = "{";
        for (var i = 0; i < element_values.length; i++) {
            if (document.getElementById(element_values[i]) != null) {
                values_string = values_string + "'" + element_values[i] + "':'" + document.getElementById(element_values[i]).value + "',";
            }
        }
        ## set the values
            if (document.getElementById("search_run_name_id") != null) {
            document.getElementById("search_run_name_id").value = values_string + "}";
        }
        else if (document.getElementById("search_source_id") != null) {
            document.getElementById("search_source_id").value = values_string + "}";
        }
    } else {
        if (document.getElementById("run_name") != null) {
            document.getElementById("search_run_name_id").value = document.getElementById("run_name").value;
        }
        if (document.getElementById("source") != null) {
            document.getElementById("search_source_id").value = document.getElementById("source").value;
        }
    }


}

function run_name_query_creator() {
    if (document.getElementById("run_name") != null) {
        document.getElementById("search_run_name_id").value = document.getElementById("run_name").value;
    }
}

function source_query_creator() {
    if (document.getElementById("source") != null) {
        document.getElementById("search_source_id").value = document.getElementById("source").value;
    }
}
function toggle_usage() {
    $(document).ready(function () {
                if (document.getElementById("usage_box") != null) {
                    document.getElementById("usage_box").remove();
                } else {
                    var usage =
                            '<fieldset id="usage_box">' +
                                    '<legend>Usage:</legend>' +
                                    '<b>General usage:</b>' +
                                    '<ol>' +
                                    '<li>Select the output type.</li>' +
                                    '<li>Detailed peptide list:' +
                                    '<ol>' +
                                    '<li>Choose search parameters and add these.</li>' +
                                    '<li>If you can choose between "OR" and "AND" it is possible for multiple inputs. Seperate the elements with a ";" (no quotes!).</li>' +
                                    '<li>All parameters can be combined.</li>' +
                                    '</ol>' +
                                    '</li>' +
                                    '<li>Run and source information:' +
                                    '<ol>' +
                                    '<li>Write your run or source into the box (Wildcards allowed).</li>' +
                                    '<li>If you select "Count peptides" please set the filter parameters.</li>' +
                                    '</ol>' +
                                    '</li>' +
                                    '</ol>' +
                                    '<b>Wildcards:</b>' +
                                    '<ul>' +
                                    '<li>All non numerical parameters can be used with wildcards.</li>' +
                                    '<li>For one character use "_".</li>' +
                                    '<li>For many characters use "%".</li>' +
                                    '</ul>' +

                                    '</fieldset>';

                    $("#toggle_usage_button").append(usage);


                }

            }

    )
}

## Adds the selected  HLA to the input box. type defines which input box
function add_hla_to_prediction_list(selected_hla, type) {
    if (document.getElementById(type + "_information") != null) {
        for (var option = 0; option < selected_hla.options.length; option++) {
            if (selected_hla.options[option].selected) {
                var toAdd = selected_hla.options[option].value;

                if (document.getElementById(type + "_information").value == '') {
                    document.getElementById(type + "_information").value = toAdd;
                } else {
                    if (document.getElementById(type + "_information").value.indexOf(toAdd) == -1) {
                        document.getElementById(type + "_information").value += ";" + toAdd;
                    }
                }
            }
        }
    }
}


function toggle_prediction() {
    $(document).ready(function () {
                if (document.getElementById("prediction_box") != null) {
                    document.getElementById("prediction_box").remove();
                } else {
                    ##onclick = "combine_peptide_query()
                    var usage =
                            '<fieldset id="prediction_box" style="padding:0px;margin:0px">' +
                                    '<table style="width:400px" id="hla_list">' + '<tr><td>' +
                                    'Choose HLA for prediction:</td><td>' +
                                    '<select multiple name="selected_hla_type" size="10" onclick ="add_hla_to_prediction_list(this, \'prediction\')">' +
                                    prediction_code +
                                    '<td><input style="font-size:14px" id="prediction_information" name="prediction" type="text" value="" /></td>' +
                                    '</tr>' +
                                    '</table>' +
                                    '</fieldset>';

                    $("#toggle_prediction_button").append(usage);


                }

            }

    )
}

function add_filter() {
    $(document).ready(function () {
                if (document.getElementById("filter_list_box") != null) {
                    document.getElementById("filter_list_box").remove();
                } else {
                    var filter_list =
                            '<fieldset id="filter_list_box">' +
                                        '<legend>Filter:</legend>' +
                                        '<table id="filter_list">' +
                                        '<tr><td >Ion score </td><td>>= </td> <td><input style="font-size:14px" id="ionscore_input" name="ionscore" size="3" type="text" value="20" /></td></tr>' +

                                        '<tr><td>q-Value </td><td><=  </td> <td><input style="font-size:14px" id="q_value_input" name="q-Value" size="3" type="text" value="0.05" />' +



                                       '</td></tr>' +
                                        '</table>' +
                                        'Peptide length between: <input style="font-size:14px" id="aa_length_start" name="aa_length_start_name" size="3" type="text" value="8" /> and <input style="font-size:14px" id="aa_length_end" name="aa_length_end_name" size="3" type="text" value="12" />'+
                                        '<button onclick="help_alert(\'filter_help\')" style="font-size:14px">?</button>' +
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
                        if (document.getElementById("filter_list_box") != null) {
                            document.getElementById("filter_list_box").remove();
                        }

                        var detailed_peptide_list =
                                '<fieldset id="peptide_query_box" style="border:0px; padding:0px;margin:0px">' +
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
                                        '    <option value="protein">Protein ID</option>' +
                                        '    <option value="netMHC_prediction">netMHC Prediction</option>' +
                                        '    <option value="syfpeithi_prediction">Syfpeithi Prediction</option>' +

                                        '</select></td><td>' +
                                    <!-- Add button. Uses the appendCriteria() js function-->
                                        '<input type="image" src="../../static/plus.png" height="22" onclick="appendCriteria()" id="append_criteria">' +
                                        '    </td>' +

                                        '<td><button onclick="help_alert(\'add_criteria_help\')" style="font-size:14px">?</button></td>' +
                                        '<td width ="150"></td>' +


                                        '<td>' +
                                        '    <form method="post" action=query name="query">' +
                                    <!-- Starts the query -->
                                        '    <input style="font-size:14px" value = "Search Database" onclick = "combine_peptide_query()"  id="search" type="submit" name="search" >' +
                                        '        </form>' +

                                        '</td>' +

                                        '    </tr>' +
                                        '</table>' +

                                    <!-- Filter criteria -->
                                        '<fieldset id="filter_list_box">' +
                                        '<legend>Filter:</legend>' +
                                        '<table id="filter_list">' +
                                        '<tr><td >Ion score </td><td>>= </td> <td><input style="font-size:14px" id="ionscore_input" name="ionscore" size="3" type="text" value="20" /></td></tr>' +
                                        '<tr><td>q-Value </td><td><=  </td> <td><input style="font-size:14px" id="q_value_input" name="q-Value" size="3" type="text" value="0.05" />' +



                                       '</td></tr>' +
                                        '</table>' +
                                        'Peptide length between: <input style="font-size:14px" id="aa_length_start" name="aa_length_start_name" size="3" type="text" value="8" /> and <input style="font-size:14px" id="aa_length_end" name="aa_length_end_name" size="3" type="text" value="12" />'+
                                        '<button onclick="help_alert(\'filter_help\')" style="font-size:14px">?</button>' +
                                        '</fieldset>' +
                                        '<div id="toggle_prediction_button">' +
                                        '<button onclick="toggle_prediction()" style="font-size:14px">Select HLA epitope prediction</button>' +
                                        '</div>' +
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
                        var run_name_search = '<fieldset id="run_name_query_box"  style="border:0px; padding:0px;margin:0px">' +
                                '<form method="post" action=query name="query_runname_name">' +
                                '<table> <td><tr>' +
                                '<p style="font-size:16px"> Runname:' +
                                '<input type="text" style="font-size:16px" id="run_name">' +
                                '<input  style="font-size:14px"  value="Search Database" onclick= "combine_run_name_source_query()" id="search_run_name_id" type="submit" name="search_run_name_name"> ' +
                                '<input type="checkbox" style="font-size:14px" name="peptide_count" value="True" onclick="add_filter()"> Count peptides' +
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
                        var source_search = '<fieldset id="source_query_box"  style="border:0px; padding:0px;margin:0px">' +
                                '<form method="post" action=query name="query_source_name">' +
                                '<table> <td><tr>' +
                                '<p style="font-size:16px"> Source:' +
                                '<input type="text" style="font-size:16px" id="source">' +
                                '<input  style="font-size:14px"  value="Search Database" onclick= "combine_run_name_source_query()" id="search_source_id" type="submit" name="search_source_name"> ' +
                                '<input type="checkbox" style="font-size:14px" name="peptide_count" value="True" onclick="add_filter()"> Count peptides' +
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
                var element = "";
                ## Add sequence query
                        if (strUser == "sequence") {
                    if ($("#sequence").length == 0) {
                        element =

                                '<tr id = "sequence" name = "sequence">' +


                                        '<td>Sequence:</td> ' +
                                        '<td><input style="font-size:14px" name="sequence" id="sequence_input" type="text" /></td>' +
                                        '<td> <select id="sequence_logic" style="font-size:14px" name="sequence_logic_name">' +
                                        '<option value="AND" selected="selected">AND</option>' +
                                        '<option value="OR">OR</option>' +
                                        '</select>' +

                                        '<td><input type="image" src="../../static/minus.png" height="22" id = "sequence" onclick=removeCriteria("sequence")></td>' +
                                        '</tr>';
                        $("tr:first").append(element);
                    }
                }
                    ## Add Run name query
                        else if (strUser == "run_name") {
                    if ($("#run_name").length == 0) {
                        element = '<tr id = "run_name" name = "run_name">' +
                                '<td>Runname: </td>' +


                                '<td><input style="font-size:14px" id = "run_name_input" name="run_name" type="text" /></td>' +
                                '<td> <select id="run_name_logic" style="font-size:14px" name="run_name_logic_name">' +
                                '<option value="AND" selected="selected">AND</option>' +
                                '<option value="OR">OR</option>' +
                                '</select>' +

                                '<td><input type="image" src="../../static/minus.png" height="22"  onclick=removeCriteria("run_name")></td>' +
                                '</tr>';
                        $("tr:first").append(element);
                    }
                }
                    ## Add source name query
                        else if (strUser == "source_name") {
                    if ($("#source_name").length == 0) {
                        element = '<tr id = "source_name" name = "source">' +
                                '<td>Source name: </td>' +


                                '<td><input style="font-size:14px" id = "source_name_input" name="source_name" type="text" /></td>' +
                                '<td> <select id="source_name_logic" style="font-size:14px" name="source_name_logic_name">' +
                                '<option value="AND" selected="selected">AND</option>' +
                                '<option value="OR">OR</option>' +
                                '</select>' +

                                '<td><input type="image" src="../../static/minus.png" height="22"  onclick=removeCriteria("source_name")></td>' +
                                '</tr>';
                        $("tr:first").append(element);
                    }
                }
                    ## Add organ query
                        else if (strUser == "organ") {
                    if ($("#organ").length == 0) {
                        element = '<tr id = "organ" name = "organ">' +
                                '<td>Organ: </td>' +


                                '<td><input style="font-size:14px" id = "organ_input" name="organ" type="text" /></td>' +
                                '<td> <select id="organ_logic" style="font-size:14px" name="organ_logic_name">' +
                                '<option value="AND" selected="selected">AND</option>' +
                                '<option value="OR">OR</option>' +
                                '</select>' +

                                '<td><input type="image" src="../../static/minus.png" height="22"  onclick=removeCriteria("organ")></td>' +
                                '</tr>';
                        $("tr:first").append(element);
                    }
                }
                    ## Add tissue query
                        else if (strUser == "tissue") {
                    if ($("#tissue").length == 0) {
                        element = '<tr id = "tissue" name = "tissue">' +
                                '<td>Tissue: </td>' +

                                '<td><input style="font-size:14px"  id = "tissue_input" name="tissue" type="text" /></td>' +
                                '<td> <select id="tissue_logic" style="font-size:14px" name="tissue_logic_name">' +
                                '<option value="AND" selected="selected">AND</option>' +
                                '<option value="OR">OR</option>' +
                                '</select>' +

                                '<td><input type="image" src="../../static/minus.png" height="22" onclick=removeCriteria("tissue")></td>' +
                                '</tr>';
                        $("tr:first").append(element);
                    }
                }
                    ## Add dignity query
                        else if (strUser == "dignity") {
                    if ($("#dignity").length == 0) {
                        element = '<tr id = "dignity" name = "dignity">' +
                                '<td>Dignity: </td>' +


                                '<td><input style="font-size:14px"  id = "dignity_input" name="dignity" type="text" /></td>' +
                                '<td> <select id="dignity_logic" style="font-size:14px" name="dignity_logic_name">' +
                                '<option value="AND" selected="selected">AND</option>' +
                                '<option value="OR">OR</option>' +
                                '</select>' +

                                '<td><input type="image" src="../../static/minus.png" height="22"  onclick=removeCriteria("dignity")></td>' +
                                '</tr>';
                        $("tr:first").append(element);
                    }
                }
                    ## Add researcher query
                        else if (strUser == "researcher") {
                    if ($("#researcher").length == 0) {
                        element = '<tr id = "researcher" name = "researcher">' +
                                '<td>Researcher (last name): </td>' +


                                '<td><input style="font-size:14px" id = "researcher_input" name="researcher" type="text" /></td>' +
                                '<td> <select id="researcher_logic" style="font-size:14px" name="researcher_logic_name">' +
                                '<option value="AND" selected="selected">AND</option>' +
                                '<option value="OR">OR</option>' +
                                '</select>' +


                                '<td><input type="image" src="../../static/minus.png" height="22"   onclick=removeCriteria("researcher")></td>' +
                                '</tr>';
                        $("tr:first").append(element);
                    }
                }
                    ## Add hla typing of the source query
                        else if (strUser == "source_hla_typing") {
                    if ($("#source_hla_typing").length == 0) {
                        element = '<tr id = "source_hla_typing" name = "source_hla_typing">' +
                                '<td>Source HLA typing: </td>' +
                                '<td><input style="font-size:14px"  id = "source_hla_typing_input" name="source_hla_typing" type="text" /></td>' +
                                '<td> <select id="source_hla_typing_logic" style="font-size:14px" name="source_hla_typing_logic_name">' +
                                '<option value="AND" selected="selected">AND</option>' +
                                '<option value="OR">OR</option>' +
                                '</select>' +
                                '<td><input type="image" src="../../static/minus.png" height="22"  onclick=removeCriteria("source_hla_typing")></td>' +
                                '<td><button onclick="help_alert(\'source_hla_typing_help\')" style="font-size:14px">?</button></td>' +
                                '</tr>';
                        $("tr:first").append(element);
                    }
                }
                    ## Add protein query
                        else if (strUser == "protein") {
                    if ($("#protein").length == 0) {
                        element = '<tr id = "protein" name = "protein">' +
                                '<td>Protein ID: </td>' +
                                '<td><input style="font-size:14px"  id = "protein_input" name="protein" type="text" /></td>' +
                                '<td> <select id="protein_logic" style="font-size:14px" name="protein_logic_name">' +
                                '<option value="AND" selected="selected">AND</option>' +
                                '<option value="OR">OR</option>' +
                                '</select>' +
                                '<td><input type="image" src="../../static/minus.png" height="22"  onclick=removeCriteria("protein")></td>' +
                                '</tr>';
                        $("tr:first").append(element);
                    }
                }

                    ## Add netMHC_prediction query
                        else if (strUser == "netMHC_prediction") {
                    if ($("#netMHC_prediction").length == 0) {
                        element = '<table style="width:400px" id="netMHC_prediction">' +
                                '<tr><td>' +
                                'Choose HLA for netMHC:</td><td>' +
                                '<select multiple name="selected_hla_type" size="10" onclick = "add_hla_to_prediction_list(this, \'netMHC\')">' +
                                prediction_code +
                                '<td><input style="font-size:14px" id="netMHC_information" name="prediction" type="text" value="" /></td>' +
                                '<td> <select id="netMHC_comparison" style="font-size:14px" name="netMHC_comparison_name">' +
                                '<option value="<" selected="selected"><</option>' +
                                '<option value=">">></option>' +
                                '<option value="=">=</option>' +
                                '</select>' +
                                '<td>Score:</td><td><input style="font-size:14px"  id = "netMHC_input" name="netMHC_input" type="text" /></td>' +
                                '<td> <select id="netMHC_logic" style="font-size:14px" name="netMHC_logic_name">' +
                                '<option value="AND" selected="selected">AND</option>' +
                                '<option value="OR">OR</option>' +
                                '</select>' +
                                '<td><input type="image" src="../../static/minus.png" height="22"  onclick="removeCriteria(\'netMHC_prediction\')"></td>' +
                                '</tr>' +
                                '</table>'

                        $("tr:first").append(element);
                    }
                }
                    ## Add syfpeithi_prediction query
                        else if (strUser == "syfpeithi_prediction") {
                    if ($("#syfpeithi_prediction").length == 0) {
                        element = '<table style="width:400px" id="syfpeithi_prediction">' +
                                '<tr><td>' +
                                'Choose HLA for Syfpeithi:</td><td>' +
                                '<select multiple name="selected_hla_type" size="10" onclick = "add_hla_to_prediction_list(this,\'syfpeithi\')">' +
                                prediction_code +
                                '<td><input style="font-size:14px" id="syfpeithi_information" name="prediction" type="text" value="" /></td>' +
                                '<td> <select id="syfpeithi_comparison" style="font-size:14px" name="syfpeithi_comparison_name">' +
                                '<option value="<" selected="selected"><</option>' +
                                '<option value=">">></option>' +
                                '<option value="=">=</option>' +
                                '</select>' +
                                '<td>Score:</td><td><input style="font-size:14px"  id = "syfpeithi_input" name="syfpeithi_input" type="text" /></td>' +
                                '<td> <select id="syfpeithi_logic" style="font-size:14px" name="syfpeithi_logic_name">' +
                                '<option value="AND" selected="selected">AND</option>' +
                                '<option value="OR">OR</option>' +
                                '</select>' +
                                '<td><input type="image" src="../../static/minus.png" height="22"  onclick="removeCriteria(\'syfpeithi_prediction\')"></td>' +
                                '</tr>' +
                                '</table>'

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
    <legend>Database Query</legend>

    <select id="query_type" style="font-size:14px" name="query_type_name">
        <option value="detailed_peptide_list" selected="selected">Detailed list of peptides</option>
        <option value="Run_information">Run information</option>
        <option value="Source_information">Source information</option>
    </select>
    <input type="button" style="font-size:14px" id="query_type_selector" value="Select Type"
           onclick="select_query_type()">
    <button onclick="help_alert('select_help')" style="font-size:14px">?</button>

</fieldset>
<div id="toggle_usage_button">
    <br>
    <button onclick="toggle_usage()" style="font-size:14px">Usage information</button>

</div>
</body>
</html>

