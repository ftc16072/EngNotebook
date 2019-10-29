<%def name="title()">Home Page - ftc16072</%def>
<%def name="head()"></%def>
<%inherit file = "base.mako"/>


<form action=viewEntry method="post" enctype="multipart/form-data">
        <label for="filename">What date</label>
                <select name="filename">
                        % for file in files:
                                <option value=${file}>${file[5:-5]}</option>
                        % endfor
                </select>
        <br/>
        <input type="radio" name="destination" value="Screen" checked>Screen</input>
        <input type= "radio" name="destination" value="Printer">Printer</input>
        <br/><input type="submit" value="Select"/>
</form>