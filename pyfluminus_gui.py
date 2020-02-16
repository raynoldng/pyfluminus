from pyfluminus.authorization import vafs_jwt
from pyfluminus import api
from pyfluminus.structs import File, Module

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

Form, Window = uic.loadUiType("pyfluminus.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()
app.exec_()
