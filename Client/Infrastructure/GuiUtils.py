from PyQt5.QtWidgets import QMessageBox, QApplication


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