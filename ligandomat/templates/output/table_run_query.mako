##template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<table border="1" frame="border" rules="all">
    <thead>
      <tr>
      <th>Sequence</th>
      <th>RT</th>
      <th>MZ</th>
      <th>ion score</th>
      <th>e-value</th>
      <th>antibody_set</th>
      <th>sourcename</th>
      <th>organ</th>
      <th>tissue</th>
      <th>dignity</th>
      <th>gene_group</th>
      </tr>
    </thead>
    %for row in rows:
      <tr align="center" valign="middle">
      %for col in row:
        <td width="100">${col}</td>
      %endfor
      </tr>
    %endfor
</table>
