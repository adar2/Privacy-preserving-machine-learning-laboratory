# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/UiFiles/ResultsViewDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ResultsViewDialog(object):
    def setupUi(self, ResultsViewDialog):
        ResultsViewDialog.setObjectName("ResultsViewDialog")
        ResultsViewDialog.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(ResultsViewDialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.guid_textbox = QtWidgets.QTextEdit(ResultsViewDialog)
        self.guid_textbox.setGeometry(QtCore.QRect(200, 60, 104, 64))
        self.guid_textbox.setObjectName("guid_textbox")
        self.label = QtWidgets.QLabel(ResultsViewDialog)
        self.label.setGeometry(QtCore.QRect(50, 80, 111, 21))
        self.label.setObjectName("label")
        self.check_results_button = QtWidgets.QPushButton(ResultsViewDialog)
        self.check_results_button.setGeometry(QtCore.QRect(130, 150, 141, 23))
        self.check_results_button.setObjectName("check_results_button")

        self.retranslateUi(ResultsViewDialog)
        self.buttonBox.accepted.connect(ResultsViewDialog.accept)
        self.buttonBox.rejected.connect(ResultsViewDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ResultsViewDialog)

    def retranslateUi(self, ResultsViewDialog):
        _translate = QtCore.QCoreApplication.translate
        ResultsViewDialog.setWindowTitle(_translate("ResultsViewDialog", "Results View"))
        self.label.setText(_translate("ResultsViewDialog", "Experiment GUID"))
        self.check_results_button.setText(_translate("ResultsViewDialog", "Check Results"))
