# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'icenine/ui/transactiondialog.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_transactionDialog(object):
    def setupUi(self, transactionDialog):
        transactionDialog.setObjectName("transactionDialog")
        transactionDialog.resize(635, 324)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/assets/images/icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        transactionDialog.setWindowIcon(icon)
        self.buttonBox = QtWidgets.QDialogButtonBox(transactionDialog)
        self.buttonBox.setGeometry(QtCore.QRect(290, 290, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.groupBox = QtWidgets.QGroupBox(transactionDialog)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 631, 251))
        self.groupBox.setObjectName("groupBox")
        self.rawTransaction = QtWidgets.QTextBrowser(self.groupBox)
        self.rawTransaction.setGeometry(QtCore.QRect(10, 30, 611, 211))
        self.rawTransaction.setObjectName("rawTransaction")
        self.label = QtWidgets.QLabel(transactionDialog)
        self.label.setGeometry(QtCore.QRect(10, 260, 611, 41))
        self.label.setWordWrap(True)
        self.label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label.setObjectName("label")

        self.retranslateUi(transactionDialog)
        self.buttonBox.accepted.connect(transactionDialog.accept)
        self.buttonBox.rejected.connect(transactionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(transactionDialog)

    def retranslateUi(self, transactionDialog):
        _translate = QtCore.QCoreApplication.translate
        transactionDialog.setWindowTitle(_translate("transactionDialog", "Signed Raw Transaction"))
        self.groupBox.setTitle(_translate("transactionDialog", "Raw Transaction"))
        self.label.setText(_translate("transactionDialog", "You can now safely take this raw transaction and enter it in any publicly available service or personal node you like. "))

from icenine.ui import assets_rc
