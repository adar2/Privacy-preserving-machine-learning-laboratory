# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(696, 380)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(80, 40, 631, 81))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.UploadDataButton = QtWidgets.QPushButton(self.centralwidget)
        self.UploadDataButton.setGeometry(QtCore.QRect(60, 180, 131, 81))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.UploadDataButton.setFont(font)
        self.UploadDataButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.UploadDataButton.setObjectName("UploadDataButton")
        self.CreateExperimentButton = QtWidgets.QPushButton(self.centralwidget)
        self.CreateExperimentButton.setGeometry(QtCore.QRect(400, 180, 241, 81))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.CreateExperimentButton.setFont(font)
        self.CreateExperimentButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.CreateExperimentButton.setObjectName("CreateExperimentButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ASY Experiment Tool"))
        self.label.setText(_translate("MainWindow", "ASY protocol experiment tool"))
        self.UploadDataButton.setText(_translate("MainWindow", "Upload data"))
        self.CreateExperimentButton.setText(_translate("MainWindow", "Create new experiment"))