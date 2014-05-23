

    <form action="ligandomat_output.xls" method="post">

        Showing only 100 peptides at maximum.<br>
        Download the full result in .xls format: <input style="font-size:14px" value="Download" type="submit" name="download_xls" /><br>

        <table border="1" frame="border" rules="all" id='table_all_infos'>

            <thead>
            <tr>
                % for head in headers:
                     % if "170414" in head:
                            <th>
                                <% temp= head.replace("_170414","") %>
                                ${temp}
                            </th>
                        %else:
                            <th> ${head} </th>
                        % endif
                % endfor

            </tr>
            </thead>

            % for key, row in enumerate(rows):
                % if key == 1000:
                    <% return %>
                % endif
                <tr align="center" valign="middle">
                    % for head in headers:
                        % if head == "uniprot_accession":
                            <td>
                           % for acc in row['uniprot_accession'].split(', '):
                             <a href="http://www.uniprot.org/uniprot/${acc}">${acc}</a>
                            % endfor
                            </td>
                        %else:
                            <td>${row[head]}</td>
                        % endif
                    % endfor

                </tr>
            %endfor
        </table>
    </form>