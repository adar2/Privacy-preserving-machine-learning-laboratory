# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/UiFiles/UploadDataDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

from Client.Infrastructure.GuiUtils import set_style


class Ui_UploadDataDialog(object):
    def setupUi(self, UploadDataDialog):
        UploadDataDialog.setObjectName("UploadDataDialog")
        UploadDataDialog.setWindowModality(QtCore.Qt.WindowModal)
        UploadDataDialog.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(UploadDataDialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.layoutWidget = QtWidgets.QWidget(UploadDataDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 10, 352, 223))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.guid_label = QtWidgets.QLabel(self.layoutWidget)
        self.guid_label.setObjectName("guid_label")
        self.gridLayout.addWidget(self.guid_label, 0, 0, 1, 1)
        self.guid_textbox = QtWidgets.QTextEdit(self.layoutWidget)
        self.guid_textbox.setObjectName("guid_textbox")
        self.gridLayout.addWidget(self.guid_textbox, 0, 1, 1, 1)
        self.data_label = QtWidgets.QLabel(self.layoutWidget)
        self.data_label.setObjectName("data_label")
        self.gridLayout.addWidget(self.data_label, 1, 0, 1, 1)
        self.browse_button = QtWidgets.QPushButton(self.layoutWidget)
        self.browse_button.setObjectName("browse_button")
        self.gridLayout.addWidget(self.browse_button, 1, 1, 1, 1)
        self.guid_label.raise_()
        self.data_label.raise_()
        self.browse_button.raise_()
        self.guid_textbox.raise_()
        set_style(self)
        self.retranslateUi(UploadDataDialog)
        self.buttonBox.accepted.connect(UploadDataDialog.accept)
        self.buttonBox.rejected.connect(UploadDataDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(UploadDataDialog)

    def retranslateUi(self, UploadDataDialog):
        _translate = QtCore.QCoreApplication.translate
        UploadDataDialog.setWindowTitle(_translate("UploadDataDialog", "Upload Data"))
        self.guid_label.setText(_translate("UploadDataDialog", "Experiment Guid: "))
        self.data_label.setText(_translate("UploadDataDialog", "Data:"))
        self.browse_button.setText(_translate("UploadDataDialog", "Browse..."))
