##<%inherit file = "base.mako"/>

##\begin{document}

<%!
    from latex import tex_escape
%>
<%page expression_filter="n, tex_escape"/>

\subsection{${date}}

\begin{longtable}{|m{5 cm}|m{7 cm}|m{7 cm}|}%
\hline%
Task & Details & Photo
\endhead%
\hline%
\endfoot%
\hline%
\endlastfoot

<% print(taskDict) %>
% for task, entries in taskDict.items():
    \hline
    ${task} &
    \hline
        <%
            teamMembers = []
            accomplished = []
            why = []
            learned = []
            nextSteps = []
            notes = []
            photos = []
            for entry in entries:
                teamMembers.append(entry.memberName)
                if entry.accomplished:
                    accomplished.append(entry.memberName + ": " + entry.accomplished)
                    why.append(entry.why)
                elif not entry.photoLink: #Because we can only upload one image at a time, we submit mostly blank entries with only a picture... this is to keep that from showing the name of the person multiple times
                    accomplished.append(entry.memberName)
                    why.append("")
                if entry.learned:
                    learned.append(entry.memberName + ": " + entry.learned)
                if entry.nextSteps:
                    nextSteps.append(entry.memberName + ": " + entry.nextSteps)
                if entry.photoLink:
                    photos.append(f"{entry.imgKey}")
                if entry.notes:
                    notes.append(entry.memberName + ": " + entry.notes)
        %> 
            %if accomplished:
                Accomplished: \begin{itemize}
                                    %for item in accomplished:
                                        \item ${item }
                                    <%
                                    whytext = why[accomplished.index(item)]
                                    %>
                                        %if whytext:
                                            \begin{itemize}
                                                \item ${whytext }
                                            \end{itemize}
                                        %endif

                                    %endfor
                                \end{itemize} \\
                                \hline
            %endif
            %if learned:
             Learned: \begin{itemize}
                                    %for item in learned:
                                        \item ${item}
                                    %endfor
                                \end{itemize} \\
                                \hline
            %endif
            %if nextSteps:
                 Next Steps \begin{itemize}
                                    %for item in nextSteps:
                                        \item ${item}
                                    %endfor        
                                \end{itemize}
                                \hline
            %endif
            %if notes:
                Notes:\begin{itemize}
                    %for note in notes:
                        \item ${note} 
                    %endfor
                \end{itemize}
               %endif
            &
            %if photos:
                    %for key in photos:
                        `${key}`
                    %endfor
            %endif
            \tabularnewline

        
%endfor
\hline


\end{longtable}%
