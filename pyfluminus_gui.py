import os
from pyfluminus.authorization import vafs_jwt
from pyfluminus import api
from pyfluminus.structs import File, Module
from pyfluminus.gui_file_dialog import FileDialog
from typing import Dict, List

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox

Form, Window = uic.loadUiType("pyfluminus.ui")


app = QApplication([])
window = Window()

FILE_DOWNLOAD_DIR = None
AUTH = None


def download_files(file: File, auth: Dict, download_path: str, verbose=False):

    if not file.directory:
        full_file_path = os.path.join(download_path, file.name)
        if os.path.exists(full_file_path):
            return
        print("- {}".format(full_file_path))
        file.download(auth, download_path, verbose)
        return
    print(
        "This is the dl path {} and this is the file name: {}".format(
            download_path, file.name
        )
    )
    download_path = os.path.join(download_path, file.name)
    if file.children is None:
        file.load_children(auth)
        if file.children is None:
            print("Error loading children for file: {}".format(file.name))
            return
    for child in file.children:
        download_files(child, auth, download_path, verbose)


def download():
    modules_res = api.modules(auth)
    modules = modules_res.data
    print("\n\nDownloading Files to {}".format(FILE_DOWNLOAD_DIR))
    actually_ignored_modules = []
    for module in modules:
        if module is None:
            continue
        print("{} {}".format(module.code, module.name))
        module_file = File.from_module(auth, module)
        # TODO set verbose=True for now
        download_files(module_file, auth, FILE_DOWNLOAD_DIR, True)
    print("\nDONE")
    display_download_complete()


def display_incorrect_login_message():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Error: ")
    msg.setInformativeText("You have entered an incorrect Username or Password")
    msg.setWindowTitle("Incorrect Username/Password")
    msg.exec_()


def display_download_complete():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Download Complete!")
    msg.exec_()
    exit()


def display_file_browser():
    dialog = FileDialog()
    global FILE_DOWNLOAD_DIR
    # TODO: Find a way to get rid of this global
    FILE_DOWNLOAD_DIR = dialog.openFileNameDialog()
    form.DownloadLocation.setText("Download Location:" + FILE_DOWNLOAD_DIR)


def login():
    global auth
    username = form.Username.text()
    password = form.Password.text()
    auth = vafs_jwt("nusstu\\" + username, password)
    if "jwt" not in auth:
        print("Failed to authenticate:", auth["error"])
        display_incorrect_login_message()
        return
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
form.Browse.clicked.connect(display_file_browser)
form.DownloadButton.clicked.connect(download)

window.show()
app.exec_()
