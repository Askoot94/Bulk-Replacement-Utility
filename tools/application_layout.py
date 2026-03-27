from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QTextEdit, 
    QHBoxLayout, QVBoxLayout, QPushButton,
    QPlainTextEdit, QFileDialog, QScrollBar,
    QWidget, QGridLayout
)
from PyQt6.QtGui import QFocusEvent
from tkinter import Tk
from .glossary import createGlossary, replaceTerms

# Create one TkEngine for use in all widgets
UniEngine = Tk()
UniEngine.withdraw()

# This is the Qlabel that hold the title text for the application
class title(QLabel):
    def __init__(self):
        super().__init__()

        self.setText("Bulk Term Replacements")
        
        titleFont = self.font()
        titleFont.setUnderline(True)
        titleFont.setPointSize(26)
        self.setFont(titleFont)

        self.setMaximumSize(600, 400)

class glossaryInsert(QPlainTextEdit):
    glossary = []

    def loadFile(self, fileLocation: str):
        try:
            with open(fileLocation, "rt", encoding="UTF-8") as glossaryFile:
                tempStore = glossaryFile.read()
                self.setPlainText(tempStore)
                self.updateGlossary()
                
        except Exception as error:
            print(error, "\nNeed load file warning Dialog")

    def saveFile(self, fileLocation:str):
        try:
            with open(fileLocation, "wt", encoding="UTF-8") as glossaryFile:
                tempStore = self.toPlainText()
                glossaryFile.write(tempStore)
        except Exception as error:
            print(error, "\nNeed save file warning Dialog")


    def focusOutEvent(self, e: QFocusEvent | None) -> None:
        self.updateGlossary()
        return super().focusOutEvent(e)

    def updateGlossary(self):
        plainText = self.toPlainText()

        # Need to implment faster iteration that checks if term already exists in list before adding.
        self.glossary.clear()
        self.glossary = createGlossary(plainText)

    def __init__(self):
        super().__init__()

        self.setBaseSize(360, 400)
        self.setMaximumHeight(800)
        
        formatting = self.font()
        formatting.setPointSize(12)
        self.setFont(formatting)
        
        self.setPlaceholderText("Insert glossary replacement terms here.\n" 
        "Format: {Find}={Replace} i.e Hello=World")

        self.addScrollBarWidget(QScrollBar(), Qt.AlignmentFlag(0x0002))

# This is the TextEdit box that will receive the pre-replaced text
class inputText(QTextEdit):
    def __init__(self):
        super().__init__()

        self.setPlaceholderText("Enter Text to perform replacement...")
        
        formatting = self.font()
        formatting.setPointSize(12)
        self.setFont(formatting)
        
        self.setBaseSize(960, 900)
        self.setMaximumHeight(1000)
    
class outputText(QTextEdit):
    def updateText(self, str):
        self.setText(str)

    def __init__(self):
        super().__init__()

        self.setReadOnly(True)
        self.addScrollBarWidget(QScrollBar(), Qt.AlignmentFlag(0x0002))

        formatting = self.font()
        formatting.setPointSize(18)
        self.setFont(formatting)

        self.setMinimumHeight(200)
        self.setMinimumWidth(400)
        
        self.setPlaceholderText("Replaced Text will appear here...")

class UserInputtingLayer(QGridLayout):
    replacementBegin = pyqtSignal((str, ))

    @pyqtSlot()
    def startReplacement(self):
        document = self.textBox.toPlainText()
        self.replacementBegin.emit(document)

    @pyqtSlot()
    def grabFile(self):
        # Set Options for openfile
        result = self.fileLocation.getOpenFileName(filter="*.txt *.rtf", options=QFileDialog.Option.ReadOnly)
        
        # result is a tuple with [0] = the file location Dir and [1] = filters
        # with file start loading the glossary terms
        self.glossaryWidget.loadFile(result[0])

    @pyqtSlot()
    def saveFile(self):
        # Set Options for openfile
        result = self.fileLocation.getSaveFileName(filter="*.txt *.rtf")
    
        # with file start saving the glossary terms
        self.glossaryWidget.saveFile(result[0])

    @pyqtSlot()
    def loadClipboard(self):
        UniEngine.update()
        clipboardText = UniEngine.clipboard_get()
        self.textBox.setText(clipboardText)

    def __init__(self):
        # Consists of Plain Text and Glossary Replacements
        super().__init__()

        # Create required widgets
        self.glossaryWidget = glossaryInsert()
        self.fileLocation = QFileDialog()
        self.textBox = inputText()

        fileGrab = QPushButton()
        fileGrab.setText("Load File")
        fileGrab.released.connect(lambda: self.grabFile())

        fileSave = QPushButton()
        fileSave.setText("Save File")
        fileSave.released.connect(lambda: self.saveFile())
        
        clipboardPaste = QPushButton()
        clipboardPaste.setText("Paste from Clipboard")
        clipboardPaste.released.connect(lambda: self.loadClipboard())

        self.submit = QPushButton()
        self.submit.setText("Start Replacement")
        self.submit.clicked.connect(lambda: self.startReplacement())

        # group Glossary buttons
        glossButtonsLayout = QHBoxLayout()
        glossButtonsLayout.setSpacing(6)
        glossButtonsLayout.addWidget(fileGrab)
        glossButtonsLayout.addWidget(fileSave)
        glossButtonsLayout.setContentsMargins(0,0,0,0)
        fileButtonsWidget = QWidget()
        fileButtonsWidget.setLayout(glossButtonsLayout)

        # group Input buttons
        inputButtonsLayout = QHBoxLayout()
        inputButtonsLayout.setSpacing(6)
        inputButtonsLayout.addWidget(clipboardPaste)
        inputButtonsLayout.addWidget(self.submit)
        inputButtonsLayout.setContentsMargins(0,0,0,0)
        inputButtonsWidget = QWidget()
        inputButtonsWidget.setLayout(inputButtonsLayout)

        # Connect all widgets together in grid
        self.addWidget(self.glossaryWidget, 0,0)
        self.addWidget(fileButtonsWidget, 1,0)
        self.addWidget(self.textBox, 0,1)
        self.addWidget(inputButtonsWidget, 1,1)

class TextLayer(QVBoxLayout):
    @pyqtSlot()
    def copyToClipboard(self):
        UniEngine.clipboard_clear()
        UniEngine.clipboard_append(self.output.toPlainText())
        UniEngine.update()

    def updateOutputText(self, text:str):
        self.output.updateText(text)

    def __init__(self):
        super().__init__()

        inputting = QHBoxLayout()
        importGroup = QWidget()
        importGroup.setLayout(inputting)

        self.addWidget(importGroup)

        self.output = outputText()
        self.addWidget(self.output)

        self.copy = QPushButton()
        self.copy.setText("Copy to Clipboard")
        self.copy.clicked.connect(self.copyToClipboard)
        self.addWidget(self.copy)

class FinalLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()

        capTitle = title()
        capTitle.setAlignment(Qt.AlignmentFlag(0x0021))

        # Combine Top Layer with Text Layer
        top = QWidget()
        text = QWidget()

        self.layText = TextLayer()
        self.layInp = UserInputtingLayer()
        
        top.setLayout(self.layInp)
        text.setLayout(self.layText)
        self.setContentsMargins(5,10,5,10)
        self.layInp.replacementBegin.connect(self.replacement)
        
        self.addWidget(capTitle)
        self.addWidget(top)
        self.addWidget(text)

    @pyqtSlot((str))
    def replacement(self, document:str):
        # Using Created Glossary and Given Plaintext perform call replacement and update Output Text
        # grab Glossary
        terms = self.layInp.glossaryWidget.glossary
        
        try:
            self.layText.updateOutputText(replaceTerms(document, terms))
        except Exception as e:
            print(e)
            self.layText.updateOutputText("An Error has occured.") 

class MainApplication(QMainWindow):
    def __init__(self):
        super().__init__()

        parentWidget = QWidget()
        parentWidget.setLayout(FinalLayout())

        self.setWindowTitle("Bulk Term Replacments")
        self.setCentralWidget(parentWidget)