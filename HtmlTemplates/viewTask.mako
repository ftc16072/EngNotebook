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
                    <td class="header"><a href='/viewEntry?dateString=${date}&destination=Screen'>${date}</a></td>
                    <%
                        teamMembers = []
                        accomplished = []
                        photos = {}
                        for entry in entries:
                            if entries.index(entry) == len(entries) - 1:
                                comma = " "
                            else:
                                comma = " "
                            teamMembers.append(entry.memberName + comma)
                            if entry.accomplished:
                                accomplished.append(entry.memberName + ": " + entry.accomplished + comma)
                            if entry.photoLink:
                                photos[entry.memberName] = entry.photoLink

                            print(photos)
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
                <IMG SRC=${photo} ALT="Photo" />
                </span>
            %endfor
            </td>
            </tr>
        % endfor
    </table>