#!/usr/bin/python

class calenderCreator:
    """ Generates the latex format for 3 a month calender
        Parameters:
            month       = [name, number of days]
            startingDay = day of the week at the start of month 0
                          where monday is 0
    """
    def __init__(self, startingDay, month0, month1, month2):
        self.months  = [ month0, month1, month2 ]

        # Constants
        self.topMargin      = '14mm'
        self.bottomMargin   = '6mm'
        self.sideMargin     = '4mm'
        self.entryWidth     = '52mm'
        maxHeightOfRows     = 116.0
        self.calenderColour = '160, 220, 255'

        # Finds the starting day of each month
        startingDays = []
        startingDays.append( ( startingDay                     )%7 )
        startingDays.append( ( startingDay + self.months[0][1] )%7 )
        startingDays.append( ( startingDay + self.months[0][1] \
                                           + self.months[1][1] )%7 )

        # Finds the smallest starting day
        self.startingDay = startingDays[0]
        for idx in range(1, 3):
            if startingDays[idx] < self.startingDay:
                self.startingDay = startingDays[idx]

        # Uses this to find the relative starting day
        relativeStartingDays = []
        for idx in range(0, 3):
            relativeStartingDays.append( startingDays[idx] \
                                        -self.startingDay  )

        # Adds the relative starting day to the month information
        for idx in range(0, 3):
            self.months[idx].append(relativeStartingDays[idx])


        # Finds the number of rows required
        self.numberOfRows = 0
        for idx in range(0, 3):
            combinedLength = self.months[idx][1] + self.months[idx][2]
            if self.numberOfRows < combinedLength:
                self.numberOfRows = combinedLength


        # Computes the max row hight that will fit on the A4 page
        self.entryHeight = str( round(maxHeightOfRows/self.numberOfRows, 5) )+'mm'


        # Variable to hold the row dates
        self.rows = [None]*3

        # Fills the rows and pads the beginning
        for idx in range(0, 3):
            self.rows[idx] = [0] * self.months[idx][2]             \
                           + list( range(1, self.months[idx][1]+1) )

        # Pads the end
        for i in range(0, 3):
            while len(self.rows[i]) < self.numberOfRows:
                self.rows[i].append(0)

        # Generates the header and footer
        self.headerSetup()
        self.footerSetup()

    def headerSetup(self):
        """ Generates the header
        """
        self.header = \
        [ '\\documentclass[a4paper]{article}',
          '\\usepackage[top='+self.topMargin+', '
                       'bottom='+self.bottomMargin+', '
                       'left='+self.sideMargin+', '
                       'right='+self.sideMargin+']{geometry}'
          '\\usepackage{color, colortbl}',
          '\\pagestyle{empty}',
          '',
          '',
          '\\definecolor{calenderColour}{RGB}{'+self.calenderColour+'}',
          '',
          '\\newcommand{\\entrywidth}{'+self.entryWidth+'}',
          '\\newcommand{\\entryheight}{'+self.entryHeight+'}',
          '',
          '\\begin{document}',
          '\\sffamily ',
          '\\begin{center}',
          '',
          '\\begin{tabular}{|c|p{\\entrywidth}'
                           '|c|p{\\entrywidth}'
                           '|c|p{\\entrywidth}|}',
          '\\hline',
          '\\multicolumn{2}{|c|}{'+self.months[0][0]+'}',
          '&',
          '\\multicolumn{2}{ c|}{'+self.months[1][0]+'}',
          '&',
          '\\multicolumn{2}{ c|}{'+self.months[2][0]+'}',
          '\\\\',
          '\\hline' ]

    def footerSetup(self):
        """ Generates the footer
        """
        self.footer = \
        [ '\\end{tabular}',
          '',
          '\\end{center}',
          '\\end{document}' ]

    def entryRow(self, a, b, c, colour):
        """ Generates a row
        """
        if colour:
            colourLine = '\\rowcolor{calenderColour}'
            if (a and b and c):
                colourLine = '\\rowcolor{calenderColour}'
                line  = str(a) \
                      + ' && ' \
                      + str(b) \
                      + ' && ' \
                      + str(c) \
                      + ' & \\tabularnewline[\entryheight]'
                row = [colourLine, line]
            elif (a and b):
                row  = [ '\\cellcolor{calenderColour}'+str(a)+'&',
                         '\\cellcolor{calenderColour}          &',
                         '\\cellcolor{calenderColour}'+str(b)+'&',
                         '\\cellcolor{calenderColour}          &',
                         '\\multicolumn{2}{ c|}{}'               ,
                         '\\tabularnewline[\entryheight]'         ]
            elif (a and c):
                row  = [ '\\cellcolor{calenderColour}'+str(a)+'&',
                         '\\cellcolor{calenderColour}          &',
                         '\\multicolumn{2}{ c|}{}              &',
                         '\\cellcolor{calenderColour}'+str(c)+'&',
                         '\\cellcolor{calenderColour}'           ,
                         '\\tabularnewline[\entryheight]'         ]
            elif (b and c):
                row  = [ '\\multicolumn{2}{|c|}{}              &',
                         '\\cellcolor{calenderColour}'+str(b)+'&',
                         '\\cellcolor{calenderColour}          &',
                         '\\cellcolor{calenderColour}'+str(c)+'&',
                         '\\cellcolor{calenderColour}'           ,
                         '\\tabularnewline[\entryheight]'         ]
            elif (a):
                row  = [ '\\cellcolor{calenderColour}'+str(a)+'&',
                         '\\cellcolor{calenderColour}          &',
                         '\\multicolumn{2}{ c|}{}              &',
                         '\\multicolumn{2}{ c|}{}'               ,
                         '\\tabularnewline[\entryheight]'         ]
            elif (b):
                row  = [ '\\multicolumn{2}{|c|}{}              &',
                         '\\cellcolor{calenderColour}'+str(b)+'&',
                         '\\cellcolor{calenderColour}          &',
                         '\\multicolumn{2}{ c|}{}'               ,
                         '\\tabularnewline[\entryheight]'         ]
            elif (c):
                row  = [ '\\multicolumn{2}{|c|}{}              &',
                         '\\multicolumn{2}{ c|}{}              &',
                         '\\cellcolor{calenderColour}'+str(c)+'&',
                         '\\cellcolor{calenderColour}'           ,
                         '\\tabularnewline[\entryheight]'         ]
        else:
            if (a and b and c):
                line  = str(a) \
                      + ' && ' \
                      + str(b) \
                      + ' && ' \
                      + str(c) \
                      + ' & \\tabularnewline[\entryheight]'
            elif (a and b):
                line  = str(a)                    \
                      + ' && '                    \
                      + str(b)                    \
                      + ' && '                    \
                      + '\\multicolumn{2}{ c|}{}' \
                      + ' \\tabularnewline[\entryheight]'
            elif (a and c):
                line  = str(a)                    \
                      + ' && '                    \
                      + '\\multicolumn{2}{ c|}{}' \
                      + ' & '                     \
                      + str(c)                    \
                      + ' & \\tabularnewline[\entryheight]'
            elif (b and c):
                line  = '\\multicolumn{2}{|c|}{}' \
                      + ' & '                     \
                      + str(b)                    \
                      + ' && '                    \
                      + str(c)                    \
                      + ' & \\tabularnewline[\entryheight]'
            elif (a):
                line  = str(a)                    \
                      + ' && '                    \
                      + '\\multicolumn{2}{ c|}{}' \
                      + ' & '                     \
                      + '\\multicolumn{2}{ c|}{}' \
                      + ' \\tabularnewline[\entryheight]'
            elif (b):
                line  = '\\multicolumn{2}{|c|}{}' \
                      + ' & '                     \
                      + str(b)                    \
                      + ' && '                    \
                      + '\\multicolumn{2}{ c|}{}' \
                      + ' \\tabularnewline[\entryheight]'
            elif (c):
                line  = '\\multicolumn{2}{|c|}{}' \
                      + ' & '                     \
                      + '\\multicolumn{2}{ c|}{}' \
                      + ' & '                     \
                      + str(c)                    \
                      + ' & \\tabularnewline[\entryheight]'
            row = [line]
        return row

    def entrySeperator(self, a, b, c, d, e, f):
        """ Generates the line seperating row abc from def
        """
        a = a or d
        b = b or e
        c = c or f
        if (a and b and c):
            line = '\\hline'
        elif (a and b):
            line = '\\cline{1-4}'
        elif (a and c):
            line = '\\cline{1-2}' \
                 + '\\cline{5-6}'
        elif (b and c):
            line = '\\cline{3-6}'
        elif (a):
            line = '\\cline{1-2}'
        elif (b):
            line = '\\cline{3-4}'
        elif (c):
            line = '\\cline{5-6}'
        return [line]

    def generateOutput(self):
        """ Generates the complete latex formatting
        """
        # Day of the week for row 0
        dayOfTheWeek = self.startingDay

        # Adds the header
        self.output  = self.header

        # Adds rows
        for row in range(0, self.numberOfRows):
            # True if weekend
            colour = 4 < dayOfTheWeek

            # Adds row
            self.output = self.output \
                        + self.entryRow( self.rows[0][row],
                                         self.rows[1][row],
                                         self.rows[2][row],
                                         colour            )
            # Adds row sperator
            if self.numberOfRows > row +1:
                self.output = self.output \
                            + self.entrySeperator( self.rows[0][row   ],
                                                   self.rows[1][row   ],
                                                   self.rows[2][row   ],
                                                   self.rows[0][row +1],
                                                   self.rows[1][row +1],
                                                   self.rows[2][row +1] )
            else:
                self.output = self.output \
                            + ['\\hline']

            # Increments day of the week
            dayOfTheWeek = (dayOfTheWeek +1)%7

        # Adds the footer
        self.output = self.output \
                    + self.footer

    def outputToFile(self, fileName):
        """ Outputs the formatting to a latex file
        """
        self.generateOutput()
        with open(fileName, 'w') as outputFile:
            for line in self.output:
                outputFile.write(line+'\n')


if __name__ == '__main__':
    cal = calenderCreator(1, ['October', 31], ['November', 30], ['December', 31])
    cal.generateOutput()
    cal.outputToFile('2019-Oct_Nov_Dec.tex')
