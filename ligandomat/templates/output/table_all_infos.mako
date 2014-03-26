

    <form action="ligandomat_output.xls" method="post">

        Download the result in .xls format: <input style="font-size:14px" value="Download" type="submit" name="download_xls" /><br>

        <table border="1" frame="border" rules="all" id='table_all_infos'>

            <thead>
            <tr>
                <th>Sequence</th>
                <th>Uniprot</th>
                <th>sourcename</th>
                <th>hlatype</th>
                <th>MIN RT</th>
                <th>MAX RT</th>
                <th>MIN MZ</th>
                <th>MAX MZ</th>
                <th>MIN ion score</th>
                <th>MAX ion score</th>
                <th>MIN e-value</th>
                <th>MAX e-value</th>
                <th>file occurrences</th>
                <th>antibody_set</th>
                <th>organ</th>
                <th>tissue</th>
                <th>dignity</th>
            </tr>
            </thead>

            % for row in rows:

                <tr align="center" valign="middle">
                    <td>${row['sequence']}</td>
                    <td> -</td>
                    <td> ${row['sourcename']} </td>
                    <td> ${row['hlatype']} </td>
                    <td> ${row['min_RT']} </td>
                    <td> ${row['max_RT']} </td>
                    <td> ${row['min_MZ']} </td>
                    <td> ${row['max_MZ']} </td>
                    <td> ${row['min_Score']} </td>
                    <td> ${row['max_Score']} </td>
                    <td> ${row['min_Evalue']} </td>
                    <td> ${row['max_Evalue']} </td>
                    <td> ${row['runnames']} </td>
                    <td> ${row['antibody_set']} </td>
                    <td> ${row['organ']} </td>
                    <td> ${row['tissue']} </td>
                    <td> ${row['dignity']} </td>
                </tr>
            %endfor
        </table>
    </form>