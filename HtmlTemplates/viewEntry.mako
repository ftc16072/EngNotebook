<%def name="title()">FTC16072 Entries - ${pageTitle}</%def>
<%def name="head()"></%def>
<%inherit file = "base.mako"/>
    % if destination == "Screen":
        % if previousEntry:
            <a href="/viewEntry?filename=${previousEntry}&destination=${destination}"><button>${previousEntry[5:-5]}</button></a>
        % endif
        <a href="/"><button>Home</button></a>
        % if nextEntry:
            <a href="/viewEntry?filename=${nextEntry}&destination=${destination}"><button>${nextEntry[5:-5]}</button></a>
        % endif
    % endif
    <h1>${pageTitle}</h1>
    <table class="Minutes">
        <tr>
            <th class="task">Task</th>
            <th class="details">Details</th>
            <th class="picture">Picture(s)</th>
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
                                comma = " "
                            teamMembers.append(entry['team_member'] + comma)
                            if entry['accomplished']:
                                accomplished.append(entry['team_member'] + ": " + entry['accomplished'] + comma)
                            if entry['learning']:
                                learning.append(entry['team_member'] + ": " + entry['learning'] + comma)
                            if entry['next_steps']:
                                next_steps.append(entry['team_member'] + ": " + entry['next_steps'] + comma)
                            if entry['photo']:
                                photos[entry['team_member']] = minutes.getPhotoLink(entry['photo'])

                            print(photos)
                    %>
            <td><UL>
               <LI>Accomplished
               <UL>
                 %for item in accomplished:
                      <LI>${item} </LI>
                  %endfor
               </UL></LI>
               <LI>Learning
               <UL>
                 %for item in learning:
                        <LI>${item} </LI>
                 %endfor
               </UL></LI>
               <LI>Next Steps
               <UL>
                 %for step in next_steps:
                        <LI>${step} </LI>
                 %endfor
               </UL></LI>
            </UL>
            </td>
            <td>
            %for member, photo in photos.items():
                <span class="image-container">
                <IMG SRC=${photo} ALT="Photo" />
                </span>
            %endfor
            </td>
            </tr>
        % endfor
    </table>