# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import os
import sys
import rlp
from web3 import Web3
from enum import Enum
from eth_utils.address import is_hex_address
from eth_utils.hexidecimal import is_hex, encode_hex
from eth_utils.types import is_integer
from icenine.core import log
from icenine.core.accounts import KEYSTORE_SYSTEM, PasswordException, Accounts, KeyStoreFile
from icenine.core.utils import extract_address
from icenine.core.metadata import AccountMeta
from icenine.contrib.transactions import Transaction

from PyQt5 import QtGui
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import (
        QMainWindow, 
        QDialog, 
        QApplication, 
        QMessageBox, 
        QFileDialog, 
        QListWidget,
        QAction,
        QTableWidgetItem,
        QHeaderView
    )
from icenine.ui import gui, passwordgui, aboutgui, transactiongui, aliasgui#, AccountsModel

class AlertLevel(Enum):
    INFO = QMessageBox.Information
    WARNING = QMessageBox.Warning
    ERROR = QMessageBox.Critical

class PasswordPromptResult(Enum):
    SUCCESS = 1
    CANCELED = 2
    FAILED = 3

class TableWidgetItem(QTableWidgetItem):
    """ Same as QTableWidgetItem but with some extra data """
    def __init__(self, *args, **kwargs):
        QTableWidgetItem.__init__(self, *args, **kwargs)
        if len(args) > 0 and type(args[0]) == type(""):
            self.originalValue = args[0]
        else:
            self.originalValue = ""

    def setText(self, text):
        # Not sure if we should do this one, does it use it internally?
        self.originalValue = text
        QTableWidgetItem.setText(self, text)

    def revert(self):
        """ Revert back to original value """
        self.setText(self.originalValue)

class PasswordPrompt(QDialog, passwordgui.Ui_passwordDialog):
    def __init__(self, parent=None):
        super(PasswordPrompt, self).__init__(parent)
        self.setupUi(self)

    def getPassword(account, parent=None):
        """ Prompt for a password """
        dialog = PasswordPrompt()
        dialog.passwordAccountLabel.setText(str(account))
        result = dialog.exec()
        password = dialog.password.text()
        return (result, password)

class AboutModal(QDialog, aboutgui.Ui_aboutDialog):
    def __init__(self, parent=None):
        super(AboutModal, self).__init__(parent)
        self.setupUi(self)

class TransactionDialog(QDialog, transactiongui.Ui_transactionDialog):
    def __init__(self, rawtx, parent=None):
        super(TransactionDialog, self).__init__(parent)
        self.setupUi(self)
        self.rawTransaction.setText(rawtx)

class AliasWindow(QMainWindow, aliasgui.Ui_MainWindow):
    """ The alias table window 

        Notes
        -----
        Column 0 - Alias
        Column 1 - Address
    """
    def __init__(self, parent=None):
        super(AliasWindow, self).__init__(parent)

        # Create elements
        self.setupUi(self)

        self.aliases = []
        self.blankRow = 0

        # Set table headers
        self.aliasTable.setHorizontalHeaderLabels(['Alias', 'Address'])

        # Set column resizing
        self.aliasTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.aliasTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

        with AccountMeta() as meta:
            
            self.aliases = meta.getAliases()
            i = 0
            lastRow = i

            if self.aliases:
                # Set total rows
                self.aliasTable.setRowCount(len(self.aliases) + 1)

                # Populate the table
                for alias in self.aliases:
                    aliasItem = TableWidgetItem(alias[0])
                    aliasItem.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled )

                    addressItem = TableWidgetItem(alias[1])
                    addressItem.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled )

                    self.aliasTable.setItem(i, 0, aliasItem)
                    self.aliasTable.setItem(i, 1, addressItem)

                    lastRow = i + 1
                    i += 1

            else:
                self.aliasTable.setRowCount(1)

            # Create blank cell items for a blank row at the end
            aliasBlankItem = TableWidgetItem()
            aliasBlankItem.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled )
            addressBlankItem = TableWidgetItem()
            addressBlankItem.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled )

            # An extra row for adding new aliases
            self.aliasTable.setItem(lastRow, 0, aliasBlankItem)
            self.aliasTable.setItem(lastRow, 1, addressBlankItem)

            self.blankRow = lastRow

            # handle changes
            self.aliasTable.itemChanged.connect(self.edited)

    def edited(self, item):
        """ Part of the table has been changed, figure out what it was and 
            handle it.
        """

        # If nothing was really changed, fuggetaboutit
        if hasattr(item, "originalValue"):
            if item.text() == item.originalValue:
                return

        # Get the row and column we're working with
        row = item.row()
        column = item.column()
        print("%s - %s" % (row, self.blankRow))
        # Is it the blank row that has been changed?
        if row == self.blankRow:

            addNew = False

            # Is it the alias column?
            if column == 0:

                # Has the address been filled in?
                if self.aliasTable.item(row, 1).text():
                    # Then we want to add a new alias to the DB
                    addNew = True

            elif column == 1:

                # Check if the value is valid
                if not is_hex_address(self.aliasTable.item(row, 1).text()):
                    log.debug("Invalid address, reverting change!")
                    # Revert if not
                    self.aliasTable.item(row, 1).revert()

                else:
                    # Has the alias been filled in?
                    if self.aliasTable.item(row, 0).text():
                        # Then we want to add a new alias to the DB
                        addNew = True

            if addNew:

                with AccountMeta() as meta:
                    log.debug("Adding alias %s for %s" % (self.aliasTable.item(row, 0).text(), self.aliasTable.item(row, 1).text()))
                    # Add the new alias to the DB
                    meta.addAlias(self.aliasTable.item(row, 1).text(), self.aliasTable.item(row, 0).text())

                log.debug("Adding new blank row")

                # Since we just took our last row with a new alias, add another
                aliasBlankItem = TableWidgetItem()
                aliasBlankItem.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled )
                addressBlankItem = TableWidgetItem()
                addressBlankItem.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled )

                self.aliasTable.setItem(row+1, 0, aliasBlankItem)
                self.aliasTable.setItem(row+1, 1, addressBlankItem)

                self.aliasTable.setRowCount(row+2)

        # If it's not a blank row, we're updating one
        else:

            with AccountMeta() as meta:

                # We're updating the alias
                if column == 0:
                    print(self.aliasTable.item(row, 1).text())
                    try:
                        meta.updateAliasAddress(self.aliasTable.item(row, 0).text(), self.aliasTable.item(row, 1).text())
                    except Exception as e:
                        log.error("Error while updating alias: %s" % str(e))
                        self.aliasTable.item(row, 0).revert()

                # Updating the address
                elif column == 1:

                    revert = False

                    try:
                        meta.updateAliasAlias(self.aliasTable.item(row, 1).text(), self.aliasTable.item(row, 0).text())

                    except ValueError as e:
                        revert = True
                        
                        # This is an unexpected exception, throw it
                        if "Invalid address" not in str(e):
                            raise e

                    finally:

                        if revert:
                            self.aliasTable.item(row, 1).revert()



class IceNine(QMainWindow, gui.Ui_Icenine):
    def __init__(self, parent=None):
        super(IceNine, self).__init__(parent)
        self.setupUi(self)

        self.tx = {}

        self.accounts = []
        self.accountsModel = None
        self.selectedAccount = None

        self.populateAccounts()
        self.populateForm()
        self.setupEvents()

    def setupEvents(self):
        """ Bind things to the menu """

        # Menu Bar Menu
        self.actionOpen_Keystore_File.triggered.connect(self.openKeyStore)
        self.actionBackup.triggered.connect(self.backup)
        self.actionSave_All_Accounts.triggered.connect(self.saveAll)
        self.actionAdd_Alias.triggered.connect(self.addAlias)
        self.actionView_Aliases.triggered.connect(self.showAliases)
        self.actionImport_Aliases.triggered.connect(self.importAliases)
        self.actionExport_Aliases.triggered.connect(self.exportAliases)
        self.actionAbout_Icenine.triggered.connect(self.about)

        # Main Button
        #self.createTransactionButton.triggered.connect(self.createTransaction)
        #createTxAction = QAction(self)
        #createTxAction.triggered.connect(self.createTransaction)
        self.createTransactionButton.clicked.connect(self.createTransaction)

    def resetForm(self):
        """ Clear and reset fields of the transaction form """

        self.to.setText("")
        self.amount.setText("")
        self.data.setText("")

        # Repopulate form
        self.populateForm()

    def populateForm(self):
        """ Fill in form data that we can """

        if not self.selectedAccount:
            return

        with AccountMeta() as meta:
            # Use the last used gas price and gas limit
            last_tx = meta.getLastTransaction(self.selectedAccount)
            if last_tx:
                self.gasPrice.setValue(Web3.fromWei(last_tx[2], "gwei"))
                self.gasLimit.setText(str(last_tx[3]))

            # Use the next nonce we have for the selected account
            nonce = meta.getNonce(self.selectedAccount)
            if nonce:
                self.nonce.setText(str(nonce))
            else:
                self.nonce.setText("0")

    def triggerAccount(self, item):
        """ A new account was selected """

        # Get the address of the selected account
        selected = self.accounts.accounts[item.indexes()[0].row()].address
        
        # Pull the address out of the item string
        addr = extract_address(selected)

        # Set selected
        self.selectedAccount = addr

        log.debug("Account %s selected" % addr)
        
        # Set the From account in the form
        self.fromAccount.setText(addr)

        # Populate transaction form with last known values
        self.populateForm()

    def populateAccounts(self):
        """ Fill out the accounts ListView """

        try:

            self.accounts = Accounts()
            self.accounts.load_accounts()

            # Assemble the model
            self.accountsModel = QStandardItemModel(self)
            for acct in self.accounts.accounts:
                
                account_string = acct.address
                
                # Add the alias if we have it
                if acct.alias:
                    account_string = "(%s) - %s" % (acct.alias, acct.address)
                self.accountsModel.appendRow(QStandardItem(account_string))

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
        
        return PasswordPrompt.getPassword(account_address)

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

    def addAlias(self):
        pass

    def showAliases(self):
        """ Open the window to display all aliases """
        window = AliasWindow(self)
        return window.show()

    def importAliases(self):
        pass
    def exportAliases(self):
        pass

    def about(self):
        """ Show the About modal """
        modal = AboutModal(self)
        return modal.exec()

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
                #assert(self.tx['data'] == "0x0" or is_hex(self.tx['data']))
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
            dat = self.data.toPlainText()
            # Empty should be hex zero
            #if not dat:
            #    dat = "0x0"
            self.tx['data'] = dat
        except (ValueError, KeyError): self.tx['data'] = None

        try:
            self.tx['to'] = self.to.text()
        except (ValueError, KeyError): self.tx['to'] = None

    def unlockAccount(self, account):
        """ Unlock an account """

        result, password = self.promptPassword(self.selectedAccount)
        if result:
            try:
                account.unlock(password)
            except PasswordException as e:
                log.debug(str(e))
                return PasswordPromptResult.FAILED
            return PasswordPromptResult.SUCCESS
        else:
            return PasswordPromptResult.CANCELED

    def createTransaction(self):
        """ Create a transaction with the entered data """
        
        log.debug("createTransaction")

        # Go through validation first
        if self.isFormValid():
            # Make sure we have an account for signing
            if not self.selectedAccount:
                self.alert("You must select an account before creating a transaction")

            # Get the current account
            signing_account = self.accounts.get(self.selectedAccount)

            # Unlock the account if necessary
            while not signing_account.privkey:
                try:
                    # Try to unlock an account, but if the user cancels, quit
                    if self.unlockAccount(signing_account) == PasswordPromptResult.CANCELED:
                        break
                except Exception as e:
                    self.alert("Unknown error!", str(e), alert_type=AlertLevel.ERROR)

            # If we have the private key, we can put the transaction together
            if signing_account.privkey:
                
                # Assemble transaction
                tx = Transaction(self.tx['nonce'], 
                    Web3.toWei(self.tx['gasPrice'], 'gwei'), 
                    self.tx['gasLimit'], self.tx['to'], 
                    Web3.toWei(self.tx['amount'], "ether"), 
                    self.tx['data']).sign(signing_account.privkey)
                rawtx = encode_hex(rlp.encode(tx))
                
                log.debug(tx.to_dict())

                dialog = TransactionDialog(rawtx, self)
                okay = dialog.exec()

                if okay:
                    with AccountMeta() as meta:
                        # Add the tx to the DB
                        meta.addTransaction(encode_hex(tx.hash), self.tx['nonce'], 
                            Web3.toWei(self.tx['gasPrice'], 'gwei'), 
                            self.tx['gasLimit'], self.tx['to'], 
                            Web3.toWei(self.tx['amount'], "ether"), 
                            self.tx['data'], self.selectedAccount)

                    # Reset the form if the transaction was accepted
                    self.resetForm()

                else:
                    log.warning("User canceled transaction.  Transaction details and nonce will not be stored!")

            else:
                log.debug("User canceled account unlock")


def launch():
    log.info("Launching Icenine")
    app = QApplication(sys.argv)
    ice9 = IceNine()
    ice9.show()
    app.exec_()