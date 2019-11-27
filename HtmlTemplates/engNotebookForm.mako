<%def name="title()">Entry Form-ftc16072</%def>
<%def name="head()"></%def>
<%inherit file = "base.mako"/>
<a href="index">Back<a>
<form action="addEntry" method="post" enctype="multipart/form-data">
    <label for="Team_member">Your Name:</label> 
    <select name ="Team_member">
        % for member in members:
            <option value=${member.memberId}>${member.name}</option>
        % endfor
    </select>
    <br/>
    <label for="Task">What did you work on?</label> <br/>
    <select name ="Task">
        % for task in tasks:
            <option value=${task.taskId}>${task.name}</option>
        % endfor
    </select>
    <br/>
    <label for="Accomplished">What did you do?</label>
    <br/>
    <textarea name="Accomplished" rows="5" cols="30"></textarea>
    <br/>
    <label for="Learning">What did you learn?</label>
    <br/>
    <textarea name="Learning" rows="5" cols="30"></textarea>
    <br/>
    <label for="Next_steps">Next Steps?</label>
    <br/>
    <textarea name="Next_steps" rows="5" cols="30"></textarea>
    <br/>
    <label for="Photo">Photo?</label>
    <br/>
    <input name="Photo" type="file" accept="image/*"/>
    <br/><br/>
    <input type="submit" value="Submit">

</form>