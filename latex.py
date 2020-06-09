import datetime
from entries import Entry


class LaTeX():
    def getMonthName(self, monthNumber):
        return datetime.date(2020, int(monthNumber), 1).strftime('%B')

    def entriesLaTeXFromTasksDict(self, taskDict, date):
        monthName = self.getMonthName(date[5:-3])
        wholedate = monthName + " " + date[-2:]
        latexString = "\\subsubsection {date} \n".format(date="{"+wholedate+"}")
        latexString += "\\begin{tabular}{|c|c|c|} \n"
        latexString += "\\hline Task &  Details & Photos \\tabularnewline \n"
        #result = "\n".join(listStrings);

        for task, entries in taskDict.items():
            latexString += task + " & \\begin{itemize}\n"
            for entry in entries:
                whytext = "\\begin{itemize} \\item Why: " + entry.why + " \\end{itemize}" if entry.why else ""
                accomplishedString = "\\item Accomplished \n \\begin{itemize} \n  \\item " + entry.memberName + ": " + entry.accomplished + "\n" + whytext + "\\end{itemize}"
                learnedString = "\\item Learned:"




            latexString += "& \\tabularnewline \\hline \n"

        print(latexString)


        



if __name__ == "__main__":
    latex = LaTeX()
    testDict = {
        "task1":[Entry("2019-12-07", "task1", "Philip", "Blah", "why", "Learned", "nextSteps", "photoLink", "imgKey")],
        "task2":[Entry("2019-12-07", "task2", "Andrew", "Accomplished", "", "Learned", "nextSteps", "photoLink", "imgKey")]
    }
    latex.entriesLaTeXFromTasksDict(testDict, "2019-12-07")
    print("nothing else for me to do")