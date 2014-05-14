## TODO: Limit ouptput table

    <form action="ligandomat_output.xls" method="post">

        Download the result in .xls format: <input style="font-size:14px" value="Download" type="submit" name="download_xls" /><br>

        <table border="1" frame="border" rules="all" id='table_all_infos'>

            <thead>
            <tr>
                <th>Filename</th>
                <th>Name</th>
                <th>Organ</th>
                <th>Dignity</th>
                <th>Tissue</th>
                <th>Date</th>
                <th>Sample mass</th>
                <th>Antibody mass</th>
                <th>Antibody set</th>
                <th>Hla-type</th>
            </tr>
            </thead>

            % for key, row in enumerate(rows):
                <tr align="center" valign="middle">
                    <td>${row['filename']}</td>
                    <td> ${row['name']} </td>
                    <td> ${row['organ']} </td>
                    <td> ${row['dignity']} </td>
                    <td> ${row['tissue']} </td>
                    <td> ${row['date']} </td>
                    <td> ${row['sample_mass']} </td>
                    <td> ${row['antibody_mass']} </td>
                    <td> ${row['antibody_set']} </td>
                    <td> ${row['hlatype']} </td>
                </tr>
            %endfor
        </table>
    </form>