<%def name="title()">FTC16072 Entries - ${pageTitle}</%def>
<%def name="head()"></%def>
<%inherit file = "base.mako"/>
    % if destination == "Screen":
        % if previousEntry:
            <a href="/viewEntry?dateString=${previousEntry}&destination=${destination}"><button>${previousEntry}</button></a>
        % endif
        <a href="/"><button>Home</button></a>
        % if nextEntry:
            <a href="/viewEntry?dateString=${nextEntry}&destination=${destination}"><button>${nextEntry}</button></a>
        % endif
    % endif
    <h1>${pageTitle}</h1>
    <table class="Minutes">
        <tr>
            <th class="task">Task</th>
            <th class="details">Details</th>
            <th class="picture">Picture(s)</th>
        </tr>
        
        % for item, entries in tasksDictionary.items():
            <tr>
                    % if destination == "Screen":
                        <td class="header"><a href='/viewTaskByName?taskName=${item}'>${item}</a></td>
                    % else:
                        <td class="header">${item}</td>
                    % endif
                    
                    <%
                        teamMembers = []
                        accomplished = []
                        learned = []
                        nextSteps = []
                        photos = []
                        for entry in entries:
                            if entries.index(entry) == len(entries) - 1:
                                comma = " "
                            else:
                                comma = " "
                            teamMembers.append(entry.memberName + comma)
                            if entry.accomplished:
                                accomplished.append(entry.memberName + ": " + entry.accomplished + comma)
                            if entry.learned:
                                learned.append(entry.memberName + ": " + entry.learned + comma)
                            if entry.nextSteps:
                                nextSteps.append(entry.memberName + ": " + entry.nextSteps + comma)
                            if entry.photoLink:
                                % if destination == 'Screen':
                                   photos.append(f"<A HREF='/gotoSmugmug?{entry.imgKey}'><IMG SRC={entry.photoLink} ALT='Photo' /></A>") 
                                % else:
                                   photos.append(f"<IMG SRC={entry.photoLink} ALT='Photo'/>")
                                % endif     
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
                 %for item in learned:
                        <LI>${item} </LI>
                 %endfor
               </UL></LI>
               <LI>Next Steps
               <UL>
                 %for step in nextSteps:
                        <LI>${step} </LI>
                 %endfor
               </UL></LI>
            </UL>
            </td>
            <td>
            %for photo in photos:
                <span class="image-container">
                ${photo}
                </span>
            %endfor
            </td>
            </tr>
        % endfor
    </table>