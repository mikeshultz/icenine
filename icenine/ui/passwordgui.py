# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'icenine/ui/passwordmodal.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_passwordDialog(object):
    def setupUi(self, passwordDialog):
        passwordDialog.setObjectName("passwordDialog")
        passwordDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        passwordDialog.resize(668, 110)
        self.buttonBox = QtWidgets.QDialogButtonBox(passwordDialog)
        self.buttonBox.setGeometry(QtCore.QRect(320, 70, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(passwordDialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 191, 17))
        self.label.setObjectName("label")
        self.passwordAccountLabel = QtWidgets.QLabel(passwordDialog)
        self.passwordAccountLabel.setGeometry(QtCore.QRect(200, 10, 461, 17))
        self.passwordAccountLabel.setObjectName("passwordAccountLabel")
        self.password = QtWidgets.QLineEdit(passwordDialog)
        self.password.setGeometry(QtCore.QRect(10, 40, 651, 25))
        self.password.setMaxLength(1024)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")

        self.retranslateUi(passwordDialog)
        self.buttonBox.accepted.connect(passwordDialog.accept)
        self.buttonBox.rejected.connect(passwordDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(passwordDialog)

    def retranslateUi(self, passwordDialog):
        _translate = QtCore.QCoreApplication.translate
        passwordDialog.setWindowTitle(_translate("passwordDialog", "Enter account password"))
        self.label.setText(_translate("passwordDialog", "Enter password for account"))
        self.passwordAccountLabel.setText(_translate("passwordDialog", "FILLER"))

