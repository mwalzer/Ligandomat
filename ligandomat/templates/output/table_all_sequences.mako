%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<table>
      <tr>
      <th>Sequence:</th>
      </tr>
    %for row in rows:
      <tr>
      %for col in row:
        <td>{{col}}</td>
      %end
      </tr>
    %end
</table>

<a href="javascript:history.back()">back.</a>