<%def name="title()">Tasks Form - ftc16072 </%def>
<%def name="head()"></%def>
<%inherit file = "base.mako"/>
<a href="index">Back</a> <br> <br> <br>
<fieldset> <legend>Add Task</legend>
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
</fieldset> <br/>
<fieldset> <legend>Update Tasks</legend>
<form action="updateTasks" method="post" enctype="multipart/form-data">
    <br/>
    <label for="Task">Tasks:</label> <br/>
    <table style="width:75%">
    <tr>
    <th>Name</th>
    <th>Working On</th> 
    <th>Completed</th>
    <th>Abandonded</th>
  </tr>
    % for task in sorted(tasks, key = lambda i: i['stage'], reverse=True):
    <tr>
        <td >${task['name']}</td> 
        % if task["stage"] == 'Working On':
            <td style="text-align:center"><input type="radio" name=${task['name']} value="Working On" checked></td>
            <td style="text-align:center"><input type="radio" name=${task['name']} value="Completed"></td>
            <td style="text-align:center"><input type="radio" name=${task['name']} value="Abandonded"></td>
        % endif
        % if task["stage"] == 'Completed':
            <td style="text-align:center"><input type="radio" name=${task['name']} value="Working On" ></td>
            <td style="text-align:center"><input type="radio" name=${task['name']} value="Completed" checked></td>
            <td style="text-align:center"><input type="radio" name=${task['name']} value="Abandonded"></td>
        % endif
        % if task["stage"] == 'Abandonded':
            <td style="text-align:center"><input type="radio" name=${task['name']} value="Working On" ></td>
            <td style="text-align:center"><input type="radio" name=${task['name']} value="Completed"></td>
            <td style="text-align:center"><input type="radio" name=${task['name']} value="Abandonded" checked></td>
        % endif
    </tr>
    % endfor
    </table>
    <input type="submit" value="Update">
</form>
</fieldset>
