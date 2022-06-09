# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/UiFiles/SimulationsDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SimulationsDialog(object):
    def setupUi(self, SimulationsDialog):
        SimulationsDialog.setObjectName("SimulationsDialog")
        SimulationsDialog.resize(482, 346)
        self.label_2 = QtWidgets.QLabel(SimulationsDialog)
        self.label_2.setGeometry(QtCore.QRect(90, 40, 131, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(SimulationsDialog)
        self.label_3.setGeometry(QtCore.QRect(90, 100, 131, 21))
        self.label_3.setObjectName("label_3")
        self.run_simulations_button = QtWidgets.QPushButton(SimulationsDialog)
        self.run_simulations_button.setGeometry(QtCore.QRect(160, 250, 121, 31))
        self.run_simulations_button.setObjectName("run_simulations_button")
        self.num_of_parties_textbox = QtWidgets.QPlainTextEdit(SimulationsDialog)
        self.num_of_parties_textbox.setGeometry(QtCore.QRect(230, 40, 104, 31))
        self.num_of_parties_textbox.setObjectName("num_of_parties_textbox")
        self.num_of_runs_textbox = QtWidgets.QPlainTextEdit(SimulationsDialog)
        self.num_of_runs_textbox.setGeometry(QtCore.QRect(230, 100, 104, 31))
        self.num_of_runs_textbox.setObjectName("num_of_runs_textbox")
        self.generate_dataset_checkbox = QtWidgets.QCheckBox(SimulationsDialog)
        self.generate_dataset_checkbox.setGeometry(QtCore.QRect(90, 150, 211, 18))
        self.generate_dataset_checkbox.setChecked(True)
        self.generate_dataset_checkbox.setObjectName("generate_dataset_checkbox")
        self.label = QtWidgets.QLabel(SimulationsDialog)
        self.label.setGeometry(QtCore.QRect(90, 190, 91, 21))
        self.label.setObjectName("label")
        self.browse_button = QtWidgets.QPushButton(SimulationsDialog)
        self.browse_button.setGeometry(QtCore.QRect(220, 190, 161, 41))
        self.browse_button.setObjectName("browse_button")
        self.buttonBox = QtWidgets.QDialogButtonBox(SimulationsDialog)
        self.buttonBox.setGeometry(QtCore.QRect(310, 310, 156, 23))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(SimulationsDialog)
        QtCore.QMetaObject.connectSlotsByName(SimulationsDialog)

    def retranslateUi(self, SimulationsDialog):
        _translate = QtCore.QCoreApplication.translate
        SimulationsDialog.setWindowTitle(_translate("SimulationsDialog", "Simulations"))
        self.label_2.setText(_translate("SimulationsDialog", "Number Of Parties:"))
        self.label_3.setText(_translate("SimulationsDialog", "Number Of Runs:"))
        self.run_simulations_button.setText(_translate("SimulationsDialog", "Run Simulations"))
        self.generate_dataset_checkbox.setText(_translate("SimulationsDialog", "Generate Synthetic Dataset"))
        self.label.setText(_translate("SimulationsDialog", "Dataset:"))
        self.browse_button.setText(_translate("SimulationsDialog", "Browse..."))