from pyfluminus.authorization import vafs_jwt
from pyfluminus import api
from pyfluminus.structs import File, Module

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox

Form, Window = uic.loadUiType("pyfluminus.ui")


app = QApplication([])
window = Window()


def login():
    username = form.Username.text()
    password = form.Password.text()
    print("Usename is {} and password is {}".format(username, password))
    auth = vafs_jwt("nusstu\\" + username, password)

    if "jwt" not in auth:
        print("Failed to authenticate:", auth["error"])
        exit()

    name_res = api.name(auth)
    if not name_res.ok:
        print("Error getting name: ", name_res.error_msg)
    print("Hello {}".format(name_res.data))

    modules_res = api.modules(auth)
    if not modules_res.ok:
        print("Error: ", modules_res.error_msg)
    print("Your are taking the following mods")
    modules = modules_res.data
    for module in modules:
        if module is None:
            print("Error parsing module data")
            continue
        print("- {} {}".format(module.code, module.name))
    form.stackedWidget.setCurrentIndex(1)


form = Form()
form.setupUi(window)
# Configure messages
form.Login.clicked.connect(login)

window.show()
app.exec_()
