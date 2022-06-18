import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from Client.DataServerClient import DataServerClient
from Client.FunctionalDialogs import NewExperimentDialog, DataUploadDialog, SimulationsDialog, ResultsViewDialog
from Client.UI.PyFiles.MainWindow import Ui_MainWindow


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.upload_data_button.clicked.connect(self.on_upload_data_click)
        self.create_experiment_button.clicked.connect(self.on_create_experiment_click)
        self.simulations_button.clicked.connect(self.on_simulations_click)
        self.view_results_button.clicked.connect(self.on_view_results_click)
        self.data_server_client = DataServerClient()

    def on_upload_data_click(self):
        dialog = DataUploadDialog(self.data_server_client)
        dialog.exec()

    def on_simulations_click(self):
        dialog = SimulationsDialog()
        dialog.exec()

    def on_view_results_click(self):
        dialog = ResultsViewDialog(self.data_server_client)
        dialog.exec()

    def on_create_experiment_click(self):
        dialog = NewExperimentDialog(self.data_server_client)
        dialog.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    app.exec()
