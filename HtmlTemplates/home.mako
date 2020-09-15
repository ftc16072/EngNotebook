<%def name="title()">Home Page - ftc16072</%def>
<%def name="head()"></%def>
<%inherit file = "base.mako"/>
<table>
<tr>
<th><button onclick= "window.location.href = '/newEntry';">Create New Entry</button></th>
<th><button onclick= "window.location.href = '/tasksForm';">Update/Add Tasks</button></th>
</tr>
<tr>
<td>
<form action=viewEntry method="post" enctype="multipart/form-data">
        <label for="dateString">What date</label>
                <select name="dateString">
                        % for dateItem in dateList:
                                <option value=${dateItem}>${dateItem}</option>
                        % endfor
                </select>
        <br/>
        <input type="radio" name="destination" value="Screen" checked>Screen</input>
        <input type= "radio" name="destination" value="Printer">Printer</input>
        <br/><input type="submit" value="View Entry"/>
</form>
</tr>
<td>
<form action=viewTask method="post" enctype="multipart/form-data">
        <label for="task">What Task</label>
        <select name="taskId">
                        % for task in taskList:
                                <option value=${task.taskId}>${task.name}</option>
                        % endfor
                </select>
        <br/>
        <input type="radio" name="destination" value="Screen" checked>Screen</input>
        <input type= "radio" name="destination" value="Printer">Printer</input>
        <br/><input type="submit" value="View Task"/>
</form>
</td>
</tr>
<tr><td><button onclick= "window.location.href = '/hours';">View Hours</button></td></tr>

</table>