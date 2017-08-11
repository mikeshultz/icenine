# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'icenine/ui/aboutmodal.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_aboutDialog(object):
    def setupUi(self, aboutDialog):
        aboutDialog.setObjectName("aboutDialog")
        aboutDialog.resize(400, 358)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/assets/images/icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        aboutDialog.setWindowIcon(icon)
        aboutDialog.setModal(True)
        self.label = QtWidgets.QLabel(aboutDialog)
        self.label.setGeometry(QtCore.QRect(100, 20, 221, 221))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/assets/images/icon.svg"))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(aboutDialog)
        self.label_2.setGeometry(QtCore.QRect(150, 250, 141, 61))
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setScaledContents(False)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(aboutDialog)
        self.label_3.setGeometry(QtCore.QRect(170, 310, 91, 17))
        self.label_3.setObjectName("label_3")

        self.retranslateUi(aboutDialog)
        QtCore.QMetaObject.connectSlotsByName(aboutDialog)

    def retranslateUi(self, aboutDialog):
        _translate = QtCore.QCoreApplication.translate
        aboutDialog.setWindowTitle(_translate("aboutDialog", "About IceNine"))
        self.label_2.setText(_translate("aboutDialog", "IceNine"))
        self.label_3.setText(_translate("aboutDialog", "Version X.X.X"))

from icenine.ui import assets_rc
