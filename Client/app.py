import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QFileDialog
from MainWindow import Ui_MainWindow
from UploadDataDialog import Ui_Dialog as UploadDataDialogUI
from NewExperimentDialog import Ui_Dialog as NewExperimentDialogUI
from ASY import run_ASY_protocol
from Client.DataServerClient import DataServerClient
from Client.Common import FAILURE

def error_popup(title, text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(text)
    msg.setWindowTitle(title)
    msg.exec_()

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.UploadDataButton.clicked.connect(self.upload_data_click)
        self.CreateExperimentButton.clicked.connect(self.on_create_experiment_click)
        self.data_server_client = DataServerClient()

    def upload_data_click(self):
        dialog = DataUploadDialog(self.data_server_client)
        dialog.exec()

    def on_create_experiment_click(self):
        dialog = NewExperimentDialog(self.data_server_client)
        dialog.exec()


class NewExperimentDialog(QDialog, NewExperimentDialogUI):
    def __init__(self, data_server_client: DataServerClient, parent=None):
        super().__init__(parent)
        self.data_server_client = data_server_client
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.create_new_experiment_request)

    def create_new_experiment_request(self):
        name = self.experiment_name_textbox.toPlainText()
        if len(name) == 0:
            error_popup("Name Error", "No Name Entered!")
        else:
            self.data_server_client.new_experiment(name)




class DataUploadDialog(QDialog, UploadDataDialogUI):
    def __init__(self, data_server_client: DataServerClient, parent=None):
        super().__init__(parent)
        self.file_full_path = None
        self.setupUi(self)
        self.data_server_client = data_server_client
        self.browse_button.clicked.connect(self.browse_file)
        self.buttonBox.accepted.connect(self.run_protocol)

    def run_protocol(self):
        entered_guid = self.guid_textbox.toPlainText()
        if len(entered_guid) == 0:
            error_popup("GUID Error", "No GUID Entered!")
        public_key_response, public_key = self.data_server_client.get_public_key_from_uid(entered_guid)
        if public_key_response == FAILURE:
            error_popup("Connection Error","Failed to connect to server!")
        m1, m2 = run_ASY_protocol(self.file_full_path, public_key_response)
        results_response = self.data_server_client.submit_results(entered_guid, m1, m2)
        if results_response == FAILURE:
            error_popup("Connection Error","Failed to connect to server!")

    def browse_file(self):
        filedialog = QFileDialog()
        filedialog.setFileMode(QFileDialog.AnyFile)
        #filedialog.setFilter("Text files (*.txt)")
        filedialog.setWindowTitle('Select Dataset')
        if filedialog.exec_() == QDialog.Accepted:
            self.file_full_path = str(filedialog.selectedFiles()[0])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    app.exec()
