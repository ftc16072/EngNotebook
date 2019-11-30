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
    <option value=${TaskStages.workingOn.value}>Working On</option>
    <option value=${TaskStages.completed.value}>Completed</option>
    <option value=${TaskStages.abandoned.value}>Abandoned</option>
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
    % for task in taskList:
    <tr>
        <td >${task.name}</td> 
        % for stage in [TaskStages.workingOn, TaskStages.completed, TaskStages.abandoned]:
            <td style="text-align:center">
            <input type="radio" name="${task.taskId}" value="${stage.value}"
                              ${"checked" if task.stage == stage else ""}>

            </td>
        % endfor    
      </tr>
    % endfor
    </table>
    <input type="submit" value="Update">
</form>
</fieldset>
