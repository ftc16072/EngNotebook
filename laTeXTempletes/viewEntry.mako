##<%inherit file = "base.mako"/>

##\begin{document}


\begin{center}
\subsection{${date}}

\begin{longtable}{|c{}|c{}|c{}|}%
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
<% print("**************************") %>
<% print(taskDict) %>
% for task, entries in taskDict.items():
    #
    % for entry in entries:
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
                if entry.learned:
                    learned.append(entry.memberName + ": " + entry.learned)
                if entry.nextSteps:
                    nextSteps.append(entry.memberName + ": " + entry.nextSteps)
                if entry.photoLink:
                    photos.append(f"{entry.photoId}")
        %>
        task & 
        \begin{itemize} 
            \item Accomplished \begin{itemize}
                                    %for item in accomplished:
                                    \item ${item}
                                    <%
                                    whytext = why[accomplished.index(item)]
                                    %>
                                        %if whytext:
                                            \begin{itemize}
                                                \item ${whytext}
                                            \end{itemize}
                                        %endif

                                    %endfor
                                \end{itemize}
            \item learned \begin{itemize}
                                    %for item in learned:
                                        \item ${item}
                                    %endfor
                                \end{itemize}
            \item nextSteps \begin{itemize}
                                    %for item in nextSteps:
                                        \item ${item}
                                    %endfor
                                \end{itemize}
        \end{itemize}
        & photos \\
    % endfor
%endfor
\end{longtable}%
\end{center}
\end{document}