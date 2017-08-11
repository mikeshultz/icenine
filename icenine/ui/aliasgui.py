# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'icenine/ui/aliaswindow.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/assets/images/icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(1, 1, 1, 1)
        self.gridLayout.setObjectName("gridLayout")
        self.aliasTable = QtWidgets.QTableWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.aliasTable.sizePolicy().hasHeightForWidth())
        self.aliasTable.setSizePolicy(sizePolicy)
        self.aliasTable.setMinimumSize(QtCore.QSize(400, 200))
        self.aliasTable.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.aliasTable.setShowGrid(True)
        self.aliasTable.setGridStyle(QtCore.Qt.SolidLine)
        self.aliasTable.setRowCount(40)
        self.aliasTable.setColumnCount(2)
        self.aliasTable.setObjectName("aliasTable")
        self.aliasTable.horizontalHeader().setCascadingSectionResizes(False)
        self.aliasTable.horizontalHeader().setSortIndicatorShown(True)
        self.aliasTable.horizontalHeader().setStretchLastSection(True)
        self.aliasTable.verticalHeader().setVisible(False)
        self.aliasTable.verticalHeader().setCascadingSectionResizes(False)
        self.gridLayout.addWidget(self.aliasTable, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuContacts = QtWidgets.QMenu(self.menubar)
        self.menuContacts.setObjectName("menuContacts")
        MainWindow.setMenuBar(self.menubar)
        self.actionAdd_Contact = QtWidgets.QAction(MainWindow)
        self.actionAdd_Contact.setObjectName("actionAdd_Contact")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionRemove_Alias = QtWidgets.QAction(MainWindow)
        self.actionRemove_Alias.setObjectName("actionRemove_Alias")
        self.menuContacts.addAction(self.actionAdd_Contact)
        self.menuContacts.addAction(self.actionRemove_Alias)
        self.menuContacts.addSeparator()
        self.menuContacts.addAction(self.actionClose)
        self.menubar.addAction(self.menuContacts.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Aliases"))
        self.menuContacts.setTitle(_translate("MainWindow", "Contacts"))
        self.actionAdd_Contact.setText(_translate("MainWindow", "Add Alias"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionRemove_Alias.setText(_translate("MainWindow", "Remove Alias"))

from icenine.ui import assets_rc
