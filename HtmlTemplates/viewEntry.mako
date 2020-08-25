<%def name="title()">FTC16072 Entries - ${pageTitle}</%def>
<%def name="head()">
<script src="https://d3js.org/d3.v5.min.js"></script>
<script src="https://unpkg.com/@hpcc-js/wasm@0.3.11/dist/index.min.js"></script>
<script src="https://unpkg.com/d3-graphviz@3.0.5/build/d3-graphviz.js"></script>
</%def>
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
                        why = []
                        learned = []
                        nextSteps = []
                        notes = []
                        photos = []
                        diagrams = []
                        for entry in entries:
                            if entries.index(entry) == len(entries) - 1:
                                comma = " "
                            else:
                                comma = " "
                            teamMembers.append(entry.memberName + comma)
                            if entry.accomplished:
                                accomplished.append(entry.memberName + ": " + entry.accomplished + comma)
                            why.append(entry.why)
                            if entry.learned:
                                learned.append(entry.memberName + ": " + entry.learned + comma)
                            if entry.nextSteps:
                                nextSteps.append(entry.memberName + ": " + entry.nextSteps + comma)
                            if entry.photoLink:
                                if destination == 'Screen':
                                   photos.append(f"<A HREF='/gotoSmugmug?imgkey={entry.imgKey}'><IMG SRC='{entry.photoLink}' ALT='Photo' /></A>") 
                                else:
                                   photos.append(f"<IMG SRC='{entry.photoLink}' ALT='Photo'/>")
                            if entry.notes:
                                notes.append(entry.memberName + ": " + entry.notes)
                            if entry.diagramDot:
                                diagrams.append(entry.diagramDot)
                    %>
            <td><UL>
               <LI>Accomplished
               <UL>
                    %for item in accomplished:
                        <LI>${item} <UL>
                            <%
                                whytext = why[accomplished.index(item)]
                            %>
                            %if whytext:
                                <li>Why: ${whytext}</li>
                            %endif
                        </UL></LI>
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
               %if notes:
                <li> Notes: <ul>
                    %for note in notes:
                        <li>${note} </li>
                    %endfor
                <ul></li>
               %endif
               %if diagrams:
                <li> Diagrams: <br/>
                  %
                    diagramIndex = diagramIndex + 1
                  %
                  %for diagram in diagrams:
                    <div class="diagram" id="diagram-${diagramIndex}-${loop.index}"></div>
                    <script type="text/javascript">
                        d3.select("#diagram-${loop.index}").graphviz().renderDot('${"".join(diagram.split())|n}');
                    </script>
                  %endfor
                </li>
               %endif
            </UL>
            </td>
            <td>
            %for photo in photos:
                <span class="image-container">
                ${photo | n}
                </span>
            %endfor
            </td>
            </tr>
        % endfor
    </table>