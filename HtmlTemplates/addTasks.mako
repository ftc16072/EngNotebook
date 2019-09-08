<%def name="title()">Test </%def>
<%def name="head()"></%def>
<%inherit file = "base.mako"/>
<a href="tasksForm">Back</a> <br> 
<form action="addTasks" method="post" enctype="multipart/form-data">
    <label for="task">Task Name:</label>
    <input name="task" type="textarea"> <br>
    <label for="stage">stage:</label>
    <select name="stage">
    <option>Working On</option>
    <option>Completed</option>
    <option>Abandonded</option>
    </select> <br>
    <input type="submit" value="Add">
</form>
