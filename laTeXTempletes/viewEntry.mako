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
                elif not entry.photoLink: #Because we can only upload one image at a time, we submit mostly blank entries with only a picture... this is to keep that from showing the name of the person multiple times
                    accomplished.append(entry.memberName)
                    why.append("")
                if entry.learned:
                    learned.append(entry.memberName + ": " + entry.learned)
                if entry.nextSteps:
                    nextSteps.append(entry.memberName + ": " + entry.nextSteps)
                if entry.photoLink:
                    photos.append(f"{entry.photoLink}")
        %>
        \begin{itemize} 
            %if accomplished:
                \item Accomplished \begin{itemize}
                                    %for item in accomplished:
                                    \item ${item }
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
            %endif
            %if learned:
             \item Learned \begin{itemize}
                                    %for item in learned:
                                        \item ${item}
                                    %endfor
                                \end{itemize}
            %endif
            %if nextSteps:
                 \item Next Steps \begin{itemize}
                                    %for item in nextSteps:
                                        \item ${item}
                                    %endfor
                                \end{itemize}
            %endif
       \end{itemize} & 
            %for link in photos:
                \smugmugphoto{${link}}{${link.rsplit('/', 1)[-1]}}
            %endfor
        \\\
%endfor

\end{longtable}%
