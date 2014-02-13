<%inherit file='ligandomat:templates/layout.mako'/>

<form method="post" accept-charset="utf-8" enctype="multipart/form-data">
This is your upload page.<br>
First, please select the file and afterwards hit the button :<br><br>


    ${form.the_input_file}

    <input type="submit" name="form.submitted2" value="Upload this file" /><br><br>
    
    
Tadaaaa!
</form>
