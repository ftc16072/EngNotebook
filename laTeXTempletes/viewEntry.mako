##<%inherit file = "base.mako"/>

##\begin{document}

<%!
    from latex import tex_escape
%>

\begin{center}
\subsection{${date}}
\end{center}

\begin{longtable}{|p{4 cm}|p{7 cm}|p{5 cm}|}%
\hline%
Task&Details&Pictures\\%
\hline%
\endhead%
\hline%
\multicolumn{3}{|c|}{Continued on Next Page}\\%
\hline%
\endfoot%
\hline%
\multicolumn{3}{|c|}{Not Continued on Next Page}\\%
\hline%
\endlastfoot%
<% print(taskDict) %>
% for task, entries in taskDict.items():
    \hline
    ${task} & 
        <%
            teamMembers = []
            accomplished = []
            why = []
            learned = []
            nextSteps = []
            photos = []
            for entry in entries:
                teamMembers.append(entry.memberName)
                if entry.accomplished:
                    accomplished.append(entry.memberName + ": " + entry.accomplished)
                    why.append(entry.why)
                else:
                    accomplished.append(entry.memberName)
                    why.append("")
                if entry.learned:
                    learned.append(entry.memberName + ": " + entry.learned)
                if entry.nextSteps:
                    nextSteps.append(entry.memberName + ": " + entry.nextSteps)
                if entry.photoLink:
                    photos.append(f"{entry.photoId}")
        %>
        \begin{itemize} 
            %if accomplished:
                \item Accomplished \begin{itemize}
                                    %for item in accomplished:
                                    \item ${item |n, tex_escape}
                                    <%
                                    whytext = why[accomplished.index(item)]
                                    %>
                                        %if whytext:
                                            \begin{itemize}
                                                \item ${whytext |n, tex_escape}
                                            \end{itemize}
                                        %endif

                                    %endfor
                                \end{itemize}
            %endif
            %if learned:
             \item Learned \begin{itemize}
                                    %for item in learned:
                                        \item ${item |n, tex_escape}
                                    %endfor
                                \end{itemize}
            %endif
            %if nextSteps:
                 \item Next Steps \begin{itemize}
                                    %for item in nextSteps:
                                        \item ${item |n, tex_escape}
                                    %endfor
                                \end{itemize}
            %endif
       \end{itemize} & \\\
%endfor

\end{longtable}%
