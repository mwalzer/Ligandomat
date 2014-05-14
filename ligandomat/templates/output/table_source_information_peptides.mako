## TODO: Limit ouptput table

    <form action="ligandomat_output.xls" method="post">

        Download the result in .xls format: <input style="font-size:14px" value="Download" type="submit" name="download_xls" /><br>

        <table border="1" frame="border" rules="all" id='table_all_infos'>

            <thead>
            <tr>
                <th>Name</th>
                <th>Organ</th>
                <th>Dignity</th>
                <th>Tissue</th>
                <th>Hla-type</th>
                <th>Number of Peptides</th>
            </tr>
            </thead>

            % for key, row in enumerate(rows):
                <tr align="center" valign="middle">
                    <td> ${row['name']} </td>
                    <td> ${row['organ']} </td>
                    <td> ${row['dignity']} </td>
                    <td> ${row['tissue']} </td>
                    <td> ${row['hlatype']} </td>
                    <td> ${row['number_of_peptides']}</td>
                </tr>
            %endfor
        </table>
    </form>