#built in functions
import datetime
import os
#pip installed libraries
from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, Plot, Figure, Matrix, Alignat, LongTable, Center
from pylatex.table import LongTabularx, Tabularx, MultiColumn, ColumnType
#my code
from entries import Entry

bigColumn = ColumnType("b", "X", "X")
smallColumn = ColumnType("s", "X", ">{\hsize=.5\hsize}X")

class LaTeX(): 
    def __init__(self):
        geometry_options = {"tmargin": "1cm", "lmargin": "10cm"}
        self.doc = Document(page_numbers=True, geometry_options=geometry_options)

    def getMonthName(self, monthNumber):
        return datetime.date(2020, int(monthNumber), 1).strftime('%B')

    def entriesLaTeXFromTasksDict(self, taskDict, date):
        monthName = self.getMonthName(date[5:-3])
        wholedate = monthName + " " + date[-2:]
        with self.doc.create(Section(wholedate)):
            with self.doc.create(Center()):
                with self.doc.create(LongTable('|c|c|c|',)) as data_table:
                    data_table.add_hline()
                    data_table.add_row(["Task","Details","Pictures"])
                    data_table.add_hline()
                    data_table.end_table_header()
                    data_table.add_hline()
                    data_table.add_row((MultiColumn(3, align='|c|',
                                        data='Continued on Next Page'),))
                    data_table.add_hline()
                    data_table.end_table_footer()
                    data_table.add_hline()
                    data_table.add_row((MultiColumn(3, align='|c|',
                                        data='Not Continued on Next Page'),))
                    data_table.add_hline()
                    data_table.end_table_last_footer()
                    data_table.add_row("test", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur eros nunc, consequat sit amet nisl quis, finibus faucibus augue. Maecenas gravida blandit dolor a gravida. Donec mauris libero, viverra eu consequat sit amet, feugiat non nunc. Donec blandit dignissim pulvinar. Morbi faucibus quam eros, vitae mollis ligula porta at. Fusce sed aliquet tortor. Mauris tincidunt urna dui, at ultrices leo tristique ac. Suspendisse iaculis pharetra magna, sit amet rhoncus neque fermentum non. Quisque vitae hendrerit mauris. Interdum et malesuada fames ac ante ipsum primis in faucibus. Integer at arcu in lectus eleifend pretium. Nam blandit arcu eu sem lacinia condimentum.\
                    Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Sed ullamcorper eros metus, vitae placerat lacus bibendum in. Fusce faucibus neque id suscipit iaculis. Ut et augue tempus, mattis eros quis, tincidunt ligula. Suspendisse gravida varius lectus, id viverra ex maximus eu. Pellentesque id commodo nunc, at commodo ex. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras faucibus hendrerit leo quis tincidunt. Phasellus et placerat ex. Sed nec dictum leo. Integer et tortor non felis venenatis tempor. \
                    Morbi id dui sit amet quam viverra tincidunt dignissim eu augue. Integer ut maximus velit. Nunc pellentesque facilisis aliquam. Ut feugiat lorem tortor. Nam lobortis pellentesque lobortis. Morbi volutpat molestie nibh et rutrum. In porta in lectus in dignissim. Sed in mollis massa, quis aliquet odio. Nulla eu justo nec turpis ultricies efficitur. Sed pharetra sem consectetur mi ultrices, in pretium leo suscipit. Donec quis tortor semper, tempus urna a, iaculis diam. \
                    Sed dictum cursus pulvinar. Aliquam finibus turpis ut dui convallis, eu fermentum tortor euismod. Donec lobortis sem at vulputate venenatis. Sed gravida et lacus sit amet gravida. Nam nec lorem posuere, semper diam at, gravida neque. Curabitur iaculis nisi ut dolor fermentum, vel ornare risus suscipit. Proin pulvinar hendrerit elit, a lobortis est pharetra sit amet. Pellentesque arcu orci, porttitor vitae velit in, interdum elementum ex. Nulla pellentesque sodales imperdiet. In vulputate neque eu nunc rhoncus mattis.\
                    Vestibulum vehicula nisi urna, et volutpat magna placerat eget. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin arcu mi, sagittis sit amet ex sit amet, tincidunt molestie lorem. Vestibulum consequat risus sit amet purus fermentum scelerisque. Praesent diam risus, hendrerit in ultricies in, tincidunt sagittis urna. Vivamus cursus augue at diam condimentum, ut rhoncus lacus facilisis. Aliquam at erat eu magna sollicitudin vestibulum.", "")


        """ monthName = self.getMonthName(date[5:-3])
        wholedate = monthName + " " + date[-2:]
        latexString = self.slash + "subsubsection {date} \n".format(date="{"+wholedate+"}")
        latexString += self.slash + "begin{tabular}{|c|c|c|} \n"
        latexString += self.slash + "hline Task & Details & Photos \\tabularnewline \n"
        #result = "\n".join(listStrings);

        for task, entries in taskDict.items():
            latexString += task + " & \\begin{itemize}\n"
            for entry in entries:
                whytext = "\\begin{itemize} \\item Why: " + entry.why + " \\end{itemize}" if entry.why else ""
                accomplishedString = "\\item Accomplished \n \\begin{itemize} \n  \\item " + entry.memberName + ": " + entry.accomplished + "\n" + whytext + "\\end{itemize}"
                learnedString = "\\item Learned:"




            latexString += "& \\tabularnewline \\hline \n"

        print(latexString) """




        



if __name__ == "__main__":
    latex = LaTeX()
    testDict = {
        "task1":[Entry("2019-12-07", "task1", "Philip", "Blah", "why", "Learned", "nextSteps", "photoLink", "imgKey")],
        "task2":[Entry("2019-12-07", "task2", "Andrew", "Accomplished", "", "Learned", "nextSteps", "photoLink", "imgKey")]
    }
    latex.entriesLaTeXFromTasksDict(testDict, "2019-12-07")
    latex.doc.generate_pdf('full', clean_tex=False)
    print("nothing else for me to do")
