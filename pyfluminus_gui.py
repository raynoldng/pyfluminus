from pyfluminus.authorization import vafs_jwt
from pyfluminus import api
from pyfluminus.structs import File, Module
from typing import Dict, List

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox

Form, Window = uic.loadUiType("pyfluminus.ui")


app = QApplication([])
window = Window()


def download_files(file: File, auth: Dict, verbose=False):
    download_path = form.DownloadLocation.text()
    for module in modules:
        if module is None:
            continue
        if module.code in ignored_modules:
            actually_ignored_modules.append(module)
            continue
        print("{} {}".format(module.code, module.name))
        module_file = File.from_module(auth, module)
        # TODO set verbose=True for now
        download_files(module_file, auth, True)
        
    if not file.directory:
        full_file_path = os.path.join(download_path, file.name)
        if os.path.exists(full_file_path):
            return
        print("- {}".format(full_file_path))
        file.download(auth, download_path, verbose)
        return
    download_path = os.path.join(download_path, file.name)
    if file.children is None:
        file.load_children(auth)
        if file.children is None:
            print("Error loading children for file: {}".format(file.name))
            return
    for child in file.children:
        download_files(child, auth, download_path, verbose)
    form.stackedWidget.setCurrentIndex(3)


def login():
    username = form.Username.text()
    password = form.Password.text()
    auth = vafs_jwt("nusstu\\" + username, password)

    if "jwt" not in auth:
        print("Failed to authenticate:", auth["error"])
        exit()
    name_res = api.name(auth)
    if not name_res.ok:
        print("Error getting name: ", name_res.error_msg)
    print("Hello {}".format(name_res.data))
    get_modules_taken(auth)
    form.stackedWidget.setCurrentIndex(1)


def get_modules_taken(auth):
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


form = Form()
form.setupUi(window)
# Configure messages
form.Login.clicked.connect(login)
# form.DownloadButton.clicked.connect(download_files())

window.show()
app.exec_()
