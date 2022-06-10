import sys
from math import sqrt

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from Client.ASY import run_ASY_protocol
from Client.DataServerClient import DataServerClient
from Client.Infrastructure.GuiUtils import error_popup, info_popup, copy_to_clipboard, DialogWithBrowse
from Client.UI.PyFiles.MainWindow import Ui_MainWindow
from Client.UI.PyFiles.NewExperimentDialog import Ui_NewExperimentDialog
from Client.UI.PyFiles.ResultsViewDialog import Ui_ResultsViewDialog
from Client.UI.PyFiles.SimulationsDialog import Ui_SimulationsDialog
from Client.UI.PyFiles.UploadDataDialog import Ui_UploadDataDialog
from Client.Infrastructure.Common import FAILURE
from LogrankTest import LogrankTest
from Tests.Simulator import ExperimentSimulator


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


class NewExperimentDialog(QDialog, Ui_NewExperimentDialog):
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


class DataUploadDialog(QDialog, Ui_UploadDataDialog, DialogWithBrowse):
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


class SimulationsDialog(QDialog, Ui_SimulationsDialog, DialogWithBrowse):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connect_browse_button(self.browse_button)
        self.browse_button.setEnabled(False)
        self.run_simulations_button.clicked.connect(self.run_simulations)
        self.generate_dataset_checkbox.stateChanged.connect(self.on_generate_checkbox_toggled)
        self.figure = Figure()
        self.left_canvas = FigureCanvas(self.figure)
        self.right_canvas = FigureCanvas(self.figure)
        self.form_layout.addWidget(self.left_canvas)
        self.form_layout.addWidget(self.right_canvas)
        self.simulator = ExperimentSimulator()
        self.simulator.figure_signal.inner.connect(self.draw_figure_by_signal)
        self.simulator.progress_signal.inner.connect(self.update_progress_bar)

    def should_generate_data(self):
        return self.generate_dataset_checkbox.isChecked()

    def on_generate_checkbox_toggled(self, state):
        if state == QtCore.Qt.Checked:
            self.browse_button.setEnabled(False)
        else:
            self.browse_button.setEnabled(True)

    def run_simulations(self):
        num_of_parties = int(self.num_of_parties_textbox.text())
        num_of_runs = int(self.num_of_runs_textbox.text())
        self.simulator.number_of_parties = num_of_parties
        self.simulator.simulations_to_run = num_of_runs
        # use local file
        if self.should_generate_data():
            generated_file_name = self.generate_data_file()
            self.simulator.file_name = generated_file_name
        else:
            self.simulator.file_name = self.file_full_path
        z_fig = LogrankTest.run_logrank_test(self.simulator.file_name)
        self.simulator.start()
        self.draw_figure_on_canvas(z_fig, self.left_canvas)

    def generate_data_file(self):
        from Datasets.DataGenerator import DataGenerator
        generated_file_name = f'GeneratedData.txt'
        generator = DataGenerator()
        generator.generate_data(generated_file_name)
        return generated_file_name

    def draw_figure_on_canvas(self, figure, canvas):
        canvas.figure = figure
        canvas.draw()

    def update_progress_bar(self, percent):
        self.progress_bar.setValue(percent)

    def draw_figure_by_signal(self, object):
        self.right_canvas.figure = object
        self.right_canvas.draw()


class ResultsViewDialog(QDialog, Ui_ResultsViewDialog):
    def __init__(self, data_server_client: DataServerClient, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.check_results_button.clicked.connect(self.on_check_results_click)
        self.data_server_client = data_server_client

    def guid_textbox_is_empty(self):
        return len(self.guid_textbox.toPlainText()) == 0

    def on_check_results_click(self):
        if self.guid_textbox_is_empty():
            error_popup("No Guid Entered", "Guid field can't be empty!")
        guid = self.guid_textbox.toPlainText()
        status, results_json = self.data_server_client.get_results(guid)
        if status is FAILURE:
            error_popup("Connection Error", "Failed connecting to server!")
        name = results_json['name']
        date = results_json['creation_date']
        u = results_json['U']
        d = results_json['D']
        z_star = d / sqrt(u)
        info_popup("Experiment Results", f'Experiment Name: {name}\nCreated on: {date}\n Current Z*: {z_star}')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    app.exec()
