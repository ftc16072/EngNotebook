<%def name="title()">FTC16072 - ${pageTitle}</%def>
<%def name="head()">
</%def>
<%inherit file = "base.mako"/>
    <a href="/"><button>Home</button></a>
    <h1>Hours</h1>
    <table class="Hours">
        <tr>
            <th class="date">Date</th>
            <th class="student">Student</th>
            <th class="hours">Hours</th>
            <th class="task">Task</th>
        </tr>
        % for entry in entries:
        <tr>
            <td>${entry.date}</td>
            <td>${entry.memberName}</td>
            <td>${entry.hours}</td>
            <td>${entry.taskName}</td>
        </tr>
        % endfor
    </table>