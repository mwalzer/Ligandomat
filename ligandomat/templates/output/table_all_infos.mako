## TODO: Limit ouptput table

    <form action="ligandomat_output.xls" method="post">

        Showing only 100 peptides at maximum.<br>
        Download the full result in .xls format: <input style="font-size:14px" value="Download" type="submit" name="download_xls" /><br>

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
                <th>MIN q-value</th>
                <th>MAX q-value</th>
                <th>file occurrences</th>
                <th>antibody_set</th>
                <th>organ</th>
                <th>tissue</th>
                <th>dignity</th>
            </tr>
            </thead>

            % for key, row in enumerate(rows):
                % if key == 1000:
                    <% return %>
                % endif
                ##% uniprot = ${row['uniprot_accession']}.split(', ')

                <tr align="center" valign="middle">
                    <td>${row['sequence']}</td>
                    <td>
                    % for acc in row['uniprot_accession'].split(', '):
                        <a href="http://www.uniprot.org/uniprot/${acc}">${acc}</a>
                    % endfor
                    </td>
                    <td> ${row['sourcename']} </td>
                    <td> ${row['hlatype']} </td>
                    <td> ${row['minRT']} </td>
                    <td> ${row['maxRT']} </td>
                    <td> ${row['minMZ']} </td>
                    <td> ${row['maxMZ']} </td>
                    <td> ${row['minScore']} </td>
                    <td> ${row['maxScore']} </td>
                    <td> ${row['minE']} </td>
                    <td> ${row['maxE']} </td>
                    <td> ${row['minQ']} </td>
                    <td> ${row['maxQ']} </td>
                    <td> ${row['runnames']} </td>
                    <td> ${row['antibody_set']} </td>
                    <td> ${row['organ']} </td>
                    <td> ${row['tissue']} </td>
                    <td> ${row['dignity']} </td>
                </tr>
            %endfor
        </table>
    </form>