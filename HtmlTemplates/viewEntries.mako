<%def name="title()">View Entries - ftc16072 </%def>
<%def name="head()"></%def>
<%inherit file = "base.mako"/>
<a href="index">Back</a> <br>
<body>
    <table>
        <tr>
            <th>Task</th>
            <th>Team Member</th>
            <th>Accomplished</th>
            <th>Learned</th>
            <th>Next Steps</th>
            <th>Picture</th>
        </tr>
        
        % for item, entries in tasksDict.items():
            % for entry in entries:
                <tr>
                    <td>${item}</td>
                    <td>${entry['team_member']}</td>
                    <td>${entry['accomplished']}</td>
                    <td>${entry['learning']}</td>
                    <td>${entry['next_steps']}</td>
                    <td>${entry['photo']}</td>
            % endfor
            </tr>
        % endfor
    </table>
</body>