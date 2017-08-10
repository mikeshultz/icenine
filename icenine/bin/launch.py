# -*- coding: utf-8 -*-
import os
import sys
from enum import Enum
from eth_utils.address import is_hex_address
from eth_utils.hexidecimal import is_hex
from eth_utils.types import is_integer
from icenine.core import log
from icenine.core.accounts import KEYSTORE_SYSTEM, PasswordException, Accounts, KeyStoreFile
from icenine.core.utils import extract_address
from icenine.contrib.transactions import Transaction

from PyQt5 import QtGui
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import (
        QMainWindow, 
        QDialog, 
        QApplication, 
        QMessageBox, 
        QFileDialog, 
        QListWidget,
        QAction
    )
from icenine.ui import gui, passwordgui#, AccountsModel

class AlertLevel(Enum):
    INFO = QMessageBox.Information
    WARNING = QMessageBox.Warning
    ERROR = QMessageBox.Critical

class PasswordPrompt(QDialog, passwordgui.Ui_passwordDialog):
    def __init__(self, parent=None):
        super(PasswordPrompt, self).__init__(parent)
        self.setupUi(self)

class IceNine(QMainWindow, gui.Ui_Icenine):
    def __init__(self, parent=None):
        super(IceNine, self).__init__(parent)
        self.setupUi(self)

        self.tx = {}

        self.accounts = []
        self.accountsModel = None
        self.populateAccounts()

        self.setupEvents()

    def setupEvents(self):
        """ Bind things to the menu """

        # Menu Bar Menu
        self.actionOpen_Keystore_File.triggered.connect(self.openKeyStore)
        self.actionBackup.triggered.connect(self.backup)
        self.actionSave_All_Accounts.triggered.connect(self.saveAll)
        self.actionAdd_Contact.triggered.connect(self.addContact)
        self.actionView_Contacts.triggered.connect(self.showContacts)
        self.actionImport_Contacts.triggered.connect(self.importContacts)
        self.actionExport_Contacts.triggered.connect(self.exportContacts)
        self.actionAbout_Icenine.triggered.connect(self.about)

        # Main Button
        #self.createTransactionButton.triggered.connect(self.createTransaction)
        #createTxAction = QAction(self)
        #createTxAction.triggered.connect(self.createTransaction)
        self.createTransactionButton.clicked.connect(self.createTransaction)

    def triggerAccount(self, item):
        """ A new account was selected """

        # Get the address of the selected account
        selected = self.accounts.accounts[item.indexes()[0].row()].address
        print(selected)
        # Pull the address out of the item string
        addr = extract_address(selected)

        log.debug("Account %s selected" % addr)
        
        # Set the From account in the form
        self.fromAccount.setText(addr)

    def populateAccounts(self):
        """ Fill out the accounts ListView """

        try:

            self.accounts = Accounts()
            self.accounts.load_accounts()

            # Assemble the model
            self.accountsModel = QStandardItemModel(self)
            for acct in self.accounts.accounts:
                self.accountsModel.appendRow(QStandardItem(acct.address))

            # Create the list widget
            self.accountListView.setModel(self.accountsModel)

            # setup selection handler
            self.accountListView.selectionModel().selectionChanged.connect(self.triggerAccount)

        except FileNotFoundError as e:
            self.alert("Warning", str(e), alert_type=AlertLevel.WARNING)

    def refreshAccounts(self):
        """ Refresh the accounts ListView 

            Notes
            -----
            - This will currently not detect new files
        """

        if self.accounts:
            self.accountsModel.clear()
            for acct in self.accounts.accounts:
                self.accountsModel.appendRow(QStandardItem(acct.address))

    def alert(self, title, message, additional=None, detail=None, alert_type=AlertLevel.INFO):
        """ Display an alert to the user """

        msg = QMessageBox(self)
        msg.setIcon(alert_type.value)
        msg.setText(message)
        if additional:
            msg.setInformativeText(message)
        msg.setWindowTitle(title)
        if detail:
            msg.setDetailedText(detail)
        msg.setStandardButtons(QMessageBox.Ok)

        return msg.exec()

    def openKeyStore(self):
        """ Display the file dialog to open a keystore """

        log.debug("showing openKeyStore dialog")

        # Prompt for keystore file
        fname = QFileDialog.getOpenFileName(self, 'Open keystore file or directory', str(KEYSTORE_SYSTEM))

        if fname[0]:

            log.info("Opening keystore %s" % fname[0])

            # Open the key store file
            ksf = KeyStoreFile(fname[0])

            # Add the new account
            self.accounts.accounts.append(ksf)

            # Refresh the list
            self.refreshAccounts()

    def promptPassword(self, account_address):
        """ Get a password from a user for an account """
        
        prompt = PasswordPrompt(self)
        prompt.passwordAccountLabel.setText(QCoreApplication.translate("passwordDialog", account_address))
        return prompt.exec()

    def backup(self):
        pass

    def saveAll(self):
        """ Save all open accounts """
        if len(self.accounts) > 0:
            for ksf in self.accounts:
                try:
                    ksf.save()
                except PasswordException as e:
                    retPass = self.promptPassword(ksf.address)
                    if retPass:
                        ksf.save(retPass)
                    else:
                        log.warning("Account %s was not saved! Password not provided" % ksf.address)

    def addContact(self):
        pass
    def showContacts(self):
        pass
    def importContacts(self):
        pass
    def exportContacts(self):
        pass
    def about(self):
        pass

    def isFormValid(self):
        """ validate the transaction form """

        # Create the tx object
        self._coherceForm()
        
        try:
            assert(is_hex_address(self.tx['fromAccount']))
        except AssertionError:
            log.warning("Invalid from account address")
            self.fromAccount.selectAll()
            self.fromAccount.setFocus()
            return False

        try:
            assert(is_hex_address(self.tx['to']))
        except AssertionError:
            log.warning("Invalid to account address")
            self.to.selectAll()
            self.to.setFocus()
            return False

        try:
            assert(is_integer(self.tx['nonce']))
            assert(self.tx['nonce'] >= 0)
        except AssertionError:
            log.warning("Invalid nonce")
            self.nonce.selectAll()
            self.nonce.setFocus()
            return False

        try:
            assert(is_integer(self.tx['gasPrice']))
            assert(self.tx['gasPrice'] >= 0)
        except AssertionError:
            log.warning("Invalid gas price")
            self.gasPrice.selectAll()
            self.gasPrice.setFocus()
            return False

        try:
            assert(is_integer(self.tx['amount']))
            assert(self.tx['amount'] >= 0)
        except AssertionError:
            log.warning("Invalid amount")
            self.amount.selectAll()
            self.amount.setFocus()
            return False

        if self.tx['data']:
            try:
                assert(is_hex(self.tx['data']))
            except AssertionError:
                log.warning("Invalid data")
                self.data.selectAll()
                self.data.setFocus()
                return False

        return True

    def _coherceForm(self):
        """ Coherce the form values into the right type and format """

        try:
            self.tx['fromAccount'] = self.fromAccount.text()
        except (ValueError, KeyError): self.tx['fromAccount'] = None

        try:
            self.tx['nonce'] = int(self.nonce.text())
        except (ValueError, KeyError): self.tx['nonce'] = None

        try:
            self.tx['gasPrice'] = int(self.gasPrice.text())
        except (ValueError, KeyError): self.tx['gasPrice'] = None

        try:
            self.tx['gasLimit'] = int(self.gasLimit.text())
        except (ValueError, KeyError): self.tx['gasLimit'] = None

        try:
            self.tx['amount'] = int(self.amount.text())
        except (ValueError, KeyError): self.tx['amount'] = None

        try:
            self.tx['data'] = self.data.toPlainText()
        except (ValueError, KeyError): self.tx['data'] = None

        try:
            self.tx['to'] = self.to.text()
        except (ValueError, KeyError): self.tx['to'] = None

    def createTransaction(self):
        """ Create a transaction with the entered data """
        print("fuck")
        log.debug("createTransaction")

        # Go through validation first
        if self.isFormValid():
            # Assemble transaction
            tx = Transaction(self.tx['nonce'], self.tx['gasPrice'], self.tx['gasLimit'], self.tx['to'], self.tx['amount'], self.tx['data'])
            print(tx.to_dict())


def main():
    log.info("Launching Icenine")
    app = QApplication(sys.argv)
    ice9 = IceNine()
    ice9.show()
    app.exec_()

if __name__ == '__main__':
    main()