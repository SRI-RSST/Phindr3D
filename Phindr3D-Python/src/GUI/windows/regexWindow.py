# Copyright (C) 2022 Sunnybrook Research Institute
# This file is part of Phindr3D <https://github.com/DWALab/Phindr3D>.
#
# Phindr3D is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Phindr3D is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Phindr3D.  If not, see <http://www.gnu.org/licenses/>.

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from array import *
import os

class regexWindow(QDialog):
    def __init__(self):
        super(regexWindow, self).__init__()
        largetext = QFont("Arial", 12, 1)
        self.setWindowTitle("Create Regular Expression")
        self.samplefile = ""
        self.regex = r""
        # Use the Python array datatype to track map from filename to regex
        # (type signed int)
        self.fileToRegexPos = array('i')
        # There are column headers (groups) that are reserved or generated by
        # the metadata file writer. The list is below. Add the 'append' value to fix
        self.reservedKeys = ["ImageID"]
        self.appendToFix = "UserDefined"
        layout = QGridLayout()

        samplelabel = QLabel()
        samplelabel.setText('Sample File Name:   ')
        samplelabel.setFixedHeight(30)

        self.samplefilebox = QTextEdit()
        self.samplefilebox.setReadOnly(True)
        self.samplefilebox.setPlaceholderText(self.samplefile)
        self.samplefilebox.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.samplefilebox.setFont(largetext)
        self.samplefilebox.setFixedSize(450, 30)

        instructionlabel = QLabel()
        instructionlabel.setWordWrap(True)
        instText = "To extract metadata info from the Sample File Name, highlight the metadata value in the Sample File Name. " \
                   "Then enter the metadata name in the Group Name textbox and click the Add Group button. " \
                   "The change should be reflected in regular expression textbox. " \
                   "Repeat until all metadata info is accounted for in the regular expression." \
                   "\nNote: Don't highlight the metadata prefix or filename separators." \
                   "\nRe-selecting a previous value will produce errors. Click the Reset button to start over." \
                   "\nDo not use the following reserved group names: " + ", ".join(self.reservedKeys)
        instructionlabel.setText(instText)
        instructionlabel.setFixedSize(450, 175)

        example_btn=QPushButton("Show Example")
        example_btn.setFixedSize(example_btn.minimumSizeHint())
        example_btn.setFixedHeight(30)

        addGroup = QPushButton("Add Group")
        addGroup.setFixedSize(addGroup.minimumSizeHint())
        addGroup.setFixedHeight(30)

        groupbox = QLineEdit()
        groupbox.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        groupbox.setFont(largetext)
        groupbox.setFixedSize(200, 30)
        groupbox.setPlaceholderText("Group Name")

        viewlabel = QLabel()
        viewlabel.setText('Regular Expression:   ')
        viewlabel.setFixedHeight(30)

        self.regexview = QTextEdit()
        self.regexview.setPlaceholderText(self.samplefile)
        self.regexview.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.regexview.setFont(largetext)
        self.regexview.setFixedSize(450, 60)

        finish = QPushButton("Finish")
        finish.setFixedSize(finish.minimumSizeHint())
        finish.setFixedHeight(30)

        reset = QPushButton("Reset")
        reset.setFixedSize(reset.minimumSizeHint())
        reset.setFixedHeight(30)

        cancel = QPushButton("Cancel")
        cancel.setFixedSize(cancel.minimumSizeHint())
        cancel.setFixedHeight(30)

        def addRegexGroup():
            # The array fileToRegexPos tracks where characters in
            # the original sample file are in the regular expression
            # as group labels are added to the regex
            # Use 9999 as the previous use value for safety. The type of fileToRegexPos
            # is set to 'i' (signed int), but if it is set to 'I' (unsigned int),
            # using -1 as the previousUseVal crashes the program (full crash, not Python error).
            previousUseVal = 9999
            try:
                filename = self.samplefilebox.toPlainText()
                cursor = self.samplefilebox.textCursor()
                selstart = cursor.selectionStart()
                # cursor.selectionEnd returns the next index AFTER the selection
                selend = cursor.selectionEnd()
                sellength = len(cursor.selectedText())
                groupName = groupbox.text()
            except AttributeError:
                return
            # If the user did not select any text with the cursor,
            # show a message and return from this function
            if sellength == 0:
                errWin = self.buildErrorWindow("Use the cursor to select a value in the file name to associate with the Group Name.",
                    QMessageBox.Critical, "Select Value")
                errWin.exec()
                return

            # Test all values in the selection. If any are -1,
            # part of this text was included in a previous selection.
            # Show error window and return from this function
            testVal = any(ele == previousUseVal for ele in self.fileToRegexPos[selstart:selend])
            if testVal:
                errWin = self.buildErrorWindow("You have already defined a group that includes part or all "
                    + "of your current selection. To redefine parts of the file name, click Reset to start over.",
                    QMessageBox.Critical, "Previously Selected Characters")
                errWin.exec()
                return

            groupValue = filename[selstart:selend]

            # If no group name has been entered, do nothing
            # Otherwise, check if it is in the reserved keys list and fix it
            if groupName == "" or groupName is None:
                return
            else:
                # Check whether a reserved group name has been entered
                if groupName in self.reservedKeys:
                    groupName = groupName+self.appendToFix
                if groupValue.isnumeric():
                    grouplabel = f'(?P<{groupName}>\\d+)'
                else:
                    grouplabel = f'(?P<{groupName}>.+)'

            # Translate from the selection to the regex
            try:
                restart = self.fileToRegexPos[selstart]
                reend = self.fileToRegexPos[selend]
            except IndexError:
                return

            # Insert the grouplabel into the regex
            self.regex = self.regex[:restart] + grouplabel + self.regex[reend:]

            # Set the selected characters to previousUseVal
            for ix in range(selstart, selend):
                self.fileToRegexPos[ix] = int(previousUseVal)

            # Get the length of grouplabel, and move the indices in fileToRegex
            lenGroupLabel = len(grouplabel)
            # Number of elements in the array after the new insertion
            elAfterLabel = len(self.fileToRegexPos[selend:])
            for cx in range(elAfterLabel):
                addVal = 0 if self.fileToRegexPos[selend+cx] == previousUseVal else (lenGroupLabel - sellength)
                self.fileToRegexPos[selend+cx] += addVal

            self.regexview.setText(self.regex)
            groupbox.clear()
            groupbox.setPlaceholderText("Next Group Name")
        # end addRegexGroup

        def resetRegex():
            self.samplefilebox.setText(self.samplefile)
            self.regex = self.samplefile
            self.regexview.setText(self.regex)
            groupbox.clear()
            groupbox.setPlaceholderText("Group Name")
            # Reset the array (type signed int)
            self.fileToRegexPos = array('i')
            # Fill the index values in the array
            # (back to first positions)
            for ix in range(len(self.samplefile)):
                self.fileToRegexPos.append(ix)

        def finishRegex():
            self.regex = self.regexview.toPlainText()
            QDialog.accept(self)

        cancel.clicked.connect(self.close)
        reset.clicked.connect(resetRegex)
        finish.clicked.connect(finishRegex)
        addGroup.clicked.connect(addRegexGroup)
        example_btn.clicked.connect(lambda: example_regex())

        layout.addWidget(samplelabel, 0, 0, 1, 1)
        layout.addWidget(self.samplefilebox, 0, 1, 1, 3)
        layout.addWidget(instructionlabel, 1, 1, 1, 3)
        layout.addWidget(example_btn, 2, 3, 1, 1)
        layout.addWidget(groupbox, 2, 1, 1, 2)
        layout.addWidget(addGroup, 2, 0, 1, 1)
        layout.addWidget(viewlabel, 3, 0, 1, 1)
        layout.addWidget(self.regexview, 3, 1, 1, 3)
        layout.addWidget(finish, 4, 0, 1, 1)
        layout.addWidget(reset, 4, 1, 1, 1)
        layout.addWidget(cancel, 4, 2, 1, 1)
        self.setLayout(layout)
        self.setFixedSize(self.minimumSizeHint())

    def inputSampleFile(self):
        self.samplefilebox.setText(self.samplefile)
        self.regex = self.samplefile
        self.regexview.setText(self.regex)
        # Reset the array (type signed int)
        self.fileToRegexPos = array('i')
        # Fill the index values in the array
        for ix in range(len(self.samplefile)):
            self.fileToRegexPos.append(ix)

    def buildErrorWindow(self, errormessage, icon, errortitle="ErrorDialog"):
        alert = QMessageBox()
        alert.setWindowTitle(errortitle)
        alert.setText(errormessage)
        alert.setIcon(icon)
        return alert

import sys
class example_regex(QDialog):
    def __init__(self):
        super(example_regex, self).__init__()
        layout = QGridLayout()
        self.setWindowTitle("Example Regex")

        examplelabel = QLabel("Ex) If trying to extract ch3 which represents Channel 3, highlight 3 and put Channel in the Group Name textbox then click Add Group")
        examplelabel.setWordWrap(True)
        #example image
        img = QLabel()
        try:
            # _MEIPASS is a temporary directory that only exists
            # while running a compiled executable
            path = sys._MEIPASS #run Phindr.exe (pyinstaller temp folder)
        except:
            path = os.path.dirname(os.path.abspath(__file__)) #run Phindr.py script
        img.setPixmap(QPixmap(os.path.join(path, 'regex_example.png')))
        #add Widgets/layout
        layout.addWidget(examplelabel, 0, 0)
        layout.addWidget(img, 1, 0)
        self.setLayout(layout)
        self.show()
        self.exec()


import sys
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = regexWindow()

    # Set test file
    window.samplefile = "r03c19f01p09-ch1sk1fk1fl1.tiff"
    # window.samplefile = "image1__T111__z2__ch3__dla.tiff"
    # window.samplefile = "Wr02c02__F1__Z2__CH2__ID1__OB2.tiff"
    # window.samplefile = "P1__Wr02c02__F1__CH1__TEV__Z50__ID1__OB1.tiff"

    window.inputSampleFile()
    window.show()
    result = window.exec()
    print("Result from the regex window is " + "True" if result else "False")
    if result:
        window.close()

# end main