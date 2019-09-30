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
            <tr>
                    <td>${item}</td>
                    <%
                        teamMembers = ""
                        accomplished = ""
                        learning = ""
                        next_steps = ""
                        photos = {}
                    %>
            % for entry in entries:
                    <%
                        if entries.index(entry) == len(entries) - 1:
                            comma = " "
                        else:
                            comma = ", "
                        teamMembers += entry['team_member'] + comma
                        if entry['accomplished']:
                            accomplished += entry['team_member'] + "-" + entry['accomplished'] + comma
                        if entry['learning']:
                            learning += entry['team_member'] + "-" + entry['learning'] + comma
                        if entry['next_steps']:
                            next_steps += entry['team_member'] + "-" + entry['next_steps'] + comma
                        if entry['photo']:
                            photos[entry['team_member']] = minutes.getPhotoLink(entry['photo'])

                        print(photos)
                    %>
            % endfor
            <td>${teamMembers}</td>
            <td>${accomplished}</td>
            <td>${learning}</td>
            <td>${next_steps}</td>
            <td>
            %for member, photo in photos.items():
                ${member}: <br/><IMG SRC=${photo} ALT="Photo"/> <br/>
            %endfor
            </td>
            </tr>
        % endfor
    </table>
</body>