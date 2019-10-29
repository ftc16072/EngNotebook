<%def name="title()">View Entries - ftc16072 </%def>
<%def name="head()"></%def>
<%inherit file = "base.mako"/>
    <h1>${pageTitle}</h1>
    <table class="Minutes">
        <tr>
            <th class="task">Task</th>
            <th class="details">Details</th>
            <th class="picture">Picture</th>
        </tr>
        
        % for item, entries in minutes.getTasksDictionary().items():
            <tr>
                    <td class="header">${item}</td>
                    <%
                        teamMembers = []
                        accomplished = []
                        learning = []
                        next_steps = []
                        photos = {}
                        for entry in entries:
                            if entries.index(entry) == len(entries) - 1:
                                comma = " "
                            else:
                                comma = ", "
                            teamMembers.append(entry['team_member'] + comma)
                            if entry['accomplished']:
                                accomplished.append(entry['team_member'] + "-" + entry['accomplished'] + comma)
                            if entry['learning']:
                                learning.append(entry['team_member'] + "-" + entry['learning'] + comma)
                            if entry['next_steps']:
                                next_steps.append(entry['team_member'] + "-" + entry['next_steps'] + comma)
                            if entry['photo']:
                                photos[entry['team_member']] = minutes.getPhotoLink(entry['photo'])

                            print(photos)
                    %>
            
            <td>
                <table class="details">
                    <tr>
                        <th>Accomplished</th>
                        <td>
                            %for item in accomplished:
                                ${item} <br/>
                            %endfor
                        </td>
                        
                    </tr>
                    <tr>
                        <th>Learning</th>
                        
                        <td>
                            %for item in learning:
                                ${item} <br/>
                            %endfor
                        </td>
                        
                    </tr>
                    <tr>
                    <th>Next Steps</th>
                    <td>
                            %for step in next_steps:
                                ${step} <br/>
                            %endfor
                        </td>
                    </tr>

                </table>
            </td>
            <td>
            %for member, photo in photos.items():
                ${member}: <br/><div class="image-container">
                <IMG SRC=${photo} ALT="Photo" />
                </div> <br/>
            %endfor
            </td>
            </tr>
        % endfor
    </table>