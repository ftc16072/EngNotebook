<%def name="title()">FTC16072 - ${pageTitle}</%def>
<%def name="head()">
<script src="https://d3js.org/d3.v5.min.js"></script>
<script src="https://unpkg.com/@hpcc-js/wasm@0.3.11/dist/index.min.js"></script>
<script src="https://unpkg.com/d3-graphviz@3.0.5/build/d3-graphviz.js"></script>
</%def>
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
            <th class="notes">Notes and Diagrams</th>
        </tr>
        <%
            diagramIndex = 0
        %>
        % for date, entries in dateDictionary.items():
            <tr>
            % if destination == "Screen":
                       <td class="header"><a href='/viewEntry?dateString=${date}&destination=Screen'>${date}</a></td>
            % else:
                       <td class="header">${date}</td>
            % endif
            <%
                accomplished = []
                photos = []
                notes = []
                diagrams = []
                for entry in entries:
                    if entry.accomplished:
                        accomplished.append(f"{entry.memberName} : {entry.accomplished}")
                    if entry.photoLink:
                        if destination == 'Screen':
                            photos.append(f"<A HREF='/gotoSmugmug?imgkey={entry.imgKey}'><IMG SRC='{entry.photoLink}' ALT='Photo' /></A>") 
                        else:
                            photos.append(f"<IMG SRC='{entry.photoLink}' ALT='Photo'/>") 
                    if entry.notes:
                        notes.append(f"{entry.memberName} : {entry.notes}")
                    if entry.diagramDot:
                        diagrams.append(entry.diagramDot)
            %>
            <td>
               <UL>
                 %for item in accomplished:
                      <LI>${item} </LI>
                  %endfor
               </UL>
            </td>
            <td>
            %for photo in photos:
                <span class="image-container">
                ${photo | n}
                </span>
            %endfor
            </td>
            <td>
            %if notes:
                <UL>
                %for note in notes:
                   <LI>${note}</LI>
                %endfor
                </UL>
            %endif
            %if diagrams:
               <%
                    diagramIndex = diagramIndex + 1
               %>
               %for diagram in diagrams:
               <div class="diagram" id="diagram-${diagramIndex}-${loop.index}"></div>
               <%
                        jsDiagram = diagram.replace('\\', '\\\\').replace("\r", " ").replace("\n", "\\n").replace("'", "\\'").replace('"', '\\"')
               %> 
               <script type="text/javascript">
                    d3.select("#diagram-${diagramIndex}-${loop.index}").graphviz().renderDot("${jsDiagram|n}");
               </script>
               %endfor
            %endif
            </td>
            </tr>
        % endfor
    </table>