import sys
from os.path import expanduser
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon


# Taken from pythonspot.com
class FileDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "File Dialog"
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getExistingDirectory(
            self, "Open a Folder", expanduser("~"), QFileDialog.ShowDirsOnly
        )
        if fileName:
            return fileName
