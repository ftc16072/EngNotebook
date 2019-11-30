<%def name="title()">Entry Form-ftc16072</%def>
<%def name="head()"></%def>
<%inherit file = "base.mako"/>
<a href="index">Back<a>
<form action="addEntry" method="post" enctype="multipart/form-data">
    <label for="memberId">Your Name:</label> 
    <select name ="memberId">
        % for member in members:
            <option value=${member.memberId}>${member.name}</option>
        % endfor
    </select>
    <br/>
    <label for="taskId">What did you work on?</label> <br/>
    <select name ="taskId">
        % for task in tasks:
            <option value=${task.taskId}>${task.name}</option>
        % endfor
    </select>
    <br/>
    <label for="accomplished">What did you do?</label>
    <br/>
    <textarea name="accomplished" rows="5" cols="30"></textarea>
    <br/>
    <label for="learning">What did you learn?</label>
    <br/>
    <textarea name="learning" rows="5" cols="30"></textarea>
    <br/>
    <label for="next_steps">Next Steps?</label>
    <br/>
    <textarea name="next_steps" rows="5" cols="30"></textarea>
    <br/>
    <label for="photo">Photo?</label>
    <br/>
    <input name="photo" type="file" accept="image/*"/>
    <br/><br/>
    <input type="submit" value="Submit">

</form>