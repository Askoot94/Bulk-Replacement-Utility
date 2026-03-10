# If commandline arguments needed use: import sys and pass sys.argv to QApplication

from PyQt6.QtWidgets import QApplication
from tools.application_layout import MainApplication


if __name__ == "__main__":    
    app = QApplication([])

    mainDisplay = MainApplication()
    mainDisplay.show()       # Since mainWindow is parent it's hidden by default

    app.exec()