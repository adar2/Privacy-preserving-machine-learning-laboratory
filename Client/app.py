import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QFileDialog
from Client.Infrastructure.GuiUtils import error_popup, info_popup, copy_to_clipboard
from Client.UI.PyFiles.MainWindow import Ui_MainWindow
from Client.UI.PyFiles.UploadDataDialog import Ui_Dialog as UploadDataDialogUI
from Client.UI.PyFiles.NewExperimentDialog import Ui_Dialog as NewExperimentDialogUI
from ASY import run_ASY_protocol
from Client.DataServerClient import DataServerClient
from Client.Infrastructure.Common import FAILURE


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
        response, guid = self.data_server_client.new_experiment(name)
        if not response:
            error_popup("Connection Error", "Failed to connect to server!")
        info_popup("Experiment created", "Experiment successfully created!\n\nThe GUID was copied to your clipboard.",
                   f"Experiment name: {name}\nExperiment GUID: {guid}")
        copy_to_clipboard(guid)


class DataUploadDialog(QDialog, UploadDataDialogUI, DialogWithBrowse):
    def __init__(self, data_server_client: DataServerClient, parent=None):
        super().__init__(parent)
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
            error_popup("Connection Error", "Failed to connect to server!")
        m1, m2 = run_ASY_protocol(self.file_full_path, public_key)
        results_response = self.data_server_client.submit_results(entered_guid, m1, m2)
        if results_response == FAILURE:
            error_popup("Connection Error", "Failed to connect to server!")
        info_popup("Data upload succeeded", f"Data successfully uploaded to experiment: {entered_guid}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    app.exec()
