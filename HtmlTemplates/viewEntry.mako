<%def name="title()">View Entries - ftc16072 </%def>
<%def name="head()"></%def>
<%inherit file = "base.mako"/>
<a href="index">Back</a> <br>
<body>
    <h1>${pageTitle}</h1>
    <table>
        <tr>
            <th>Task</th>
            <th>Team Member</th>
            <th>Accomplished</th>
            <th>Learned</th>
            <th>Next Steps</th>
            <th>Picture</th>
        </tr>
        
        % for item, entries in minutes.getTasksDictionary().items():
            % for entry in entries:
                <tr>
                    <td>${item}</td>
                    <td>${entry['team_member']}</td>
                    <td>${entry['accomplished']}</td>
                    <td>${entry['learning']}</td>
                    <td>${entry['next_steps']}</td>
                % if entry['photo']:
                    <td><IMG SRC="${minutes.getPhotoLink(entry['photo'])}" ALT="Photo"/></td>
                % endif
            % endfor
            </tr>
        % endfor
    </table>
</body>