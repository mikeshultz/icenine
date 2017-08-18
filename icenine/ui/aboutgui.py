# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'icenine/ui/aboutmodal.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_aboutDialog(object):
    def setupUi(self, aboutDialog):
        aboutDialog.setObjectName("aboutDialog")
        aboutDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        aboutDialog.resize(370, 358)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/assets/images/icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        aboutDialog.setWindowIcon(icon)
        aboutDialog.setModal(True)
        self.label = QtWidgets.QLabel(aboutDialog)
        self.label.setGeometry(QtCore.QRect(80, 20, 221, 221))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/assets/images/icon.svg"))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(aboutDialog)
        self.label_2.setGeometry(QtCore.QRect(10, 250, 351, 61))
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setScaledContents(False)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.versionNumber = QtWidgets.QLabel(aboutDialog)
        self.versionNumber.setGeometry(QtCore.QRect(10, 300, 351, 20))
        self.versionNumber.setAlignment(QtCore.Qt.AlignCenter)
        self.versionNumber.setObjectName("versionNumber")
        self.label_4 = QtWidgets.QLabel(aboutDialog)
        self.label_4.setGeometry(QtCore.QRect(10, 320, 351, 20))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setOpenExternalLinks(True)
        self.label_4.setObjectName("label_4")

        self.retranslateUi(aboutDialog)
        QtCore.QMetaObject.connectSlotsByName(aboutDialog)

    def retranslateUi(self, aboutDialog):
        _translate = QtCore.QCoreApplication.translate
        aboutDialog.setWindowTitle(_translate("aboutDialog", "About IceNine"))
        self.label_2.setText(_translate("aboutDialog", "IceNine"))
        self.versionNumber.setText(_translate("aboutDialog", "Version X.X.X"))
        self.label_4.setText(_translate("aboutDialog", "<html><head/><body><p><a href=\"https://github.com/mikeshultz/icenine\"><span style=\" text-decoration: underline; color:#0000ff;\">https://github.com/mikeshultz/icenine</span></a></p></body></html>"))

from icenine.ui import assets_rc
