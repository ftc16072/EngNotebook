<%def name="title()">FTC16072 - ${pageTitle}</%def>
<%def name="head()"></%def>
<%inherit file = "base.mako"/>
% if destination == "Screen":
    <a href="/"><button>Home</button></a>
% endif
    <h1>${pageTitle}</h1>
    <table class="Minutes">
        <tr>
            <th class="date">Date</th>
            <th class="accomplished">Accomplished</th>
            <th class="picture">Picture(s)</th>
        </tr>
        
        % for date, entries in dateDictionary.items():
            <tr>
             % if destination == "Screen":
                       <td class="header"><a href='/viewEntry?dateString=${date}&destination=Screen'>${date}</a></td>
                    % else:
                       <td class="header">${date}</td>
                    % endif
                    <%
                        teamMembers = []
                        accomplished = []
                        photos = []
                        for entry in entries:
                            if entries.index(entry) == len(entries) - 1:
                                comma = " "
                            else:
                                comma = " "
                            teamMembers.append(entry.memberName + comma)
                            if entry.accomplished:
                                accomplished.append(entry.memberName + ": " + entry.accomplished + comma)
                            if entry.photoLink:
                                if destination == 'Screen':
                                   photos.append(f"<A HREF='/gotoSmugmug?imgkey={entry.imgKey}'><IMG SRC='{entry.photoLink}' ALT='Photo' /></A>") 
                                else:
                                   photos.append(f"<IMG SRC='{entry.photoLink}' ALT='Photo'/>") 
                    %>
            <td>
               <UL>
                 %for item in accomplished:
                      <LI>${item} </LI>
                  %endfor
               </UL>
            </td>
            <td>
            %for member, photo in photos.items():
                <span class="image-container">
                ${photo | n}
                </span>
            %endfor
            </td>
            </tr>
        % endfor
    </table>