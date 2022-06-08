from PyQt5.QtWidgets import QMessageBox, QApplication, QFileDialog, QDialog


def error_popup(title, text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(text)
    msg.setWindowTitle(title)
    msg.exec_()


def info_popup(title, text, informative_text=""):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(text)
    msg.setWindowTitle(title)
    msg.setInformativeText(informative_text)
    msg.exec_()


def copy_to_clipboard(text):
    QApplication.clipboard().setText(str(text))


class DialogWithBrowse():

    def __init__(self) -> None:
        self.file_full_path = None

    def browse_file(self):
        filedialog = QFileDialog()
        filedialog.setFileMode(QFileDialog.AnyFile)
        filedialog.setNameFilter("Text files (*.txt)")
        filedialog.setWindowTitle('Select Dataset')
        if filedialog.exec_() == QDialog.Accepted:
            self.file_full_path = str(filedialog.selectedFiles()[0])

    def connect_browse_button(self, browse_button):
        browse_button.clicked.connect(self.browse_file)