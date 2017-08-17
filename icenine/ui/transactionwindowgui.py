# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'icenine/ui/transactionwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TransactionsWindow(object):
    def setupUi(self, TransactionsWindow):
        TransactionsWindow.setObjectName("TransactionsWindow")
        TransactionsWindow.resize(859, 635)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/assets/images/icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        TransactionsWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(TransactionsWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMaximumSize(QtCore.QSize(60, 16777215))
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.accountComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.accountComboBox.setObjectName("accountComboBox")
        self.gridLayout.addWidget(self.accountComboBox, 0, 1, 1, 1)
        self.transactionTable = QtWidgets.QTableWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.transactionTable.sizePolicy().hasHeightForWidth())
        self.transactionTable.setSizePolicy(sizePolicy)
        self.transactionTable.setRowCount(2)
        self.transactionTable.setColumnCount(9)
        self.transactionTable.setObjectName("transactionTable")
        self.gridLayout.addWidget(self.transactionTable, 1, 0, 1, 2)
        TransactionsWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(TransactionsWindow)
        QtCore.QMetaObject.connectSlotsByName(TransactionsWindow)

    def retranslateUi(self, TransactionsWindow):
        _translate = QtCore.QCoreApplication.translate
        TransactionsWindow.setWindowTitle(_translate("TransactionsWindow", "Transactions"))
        self.label.setText(_translate("TransactionsWindow", "Account:"))

from icenine.ui import assets_rc
