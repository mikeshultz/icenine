# -*- coding: utf-8 -*-
import os
import sys
import rlp
from web3 import Web3
from eth_utils.address import is_hex_address
from eth_utils.hexidecimal import is_hex, encode_hex
from eth_utils.types import is_integer
from icenine.core import log
from icenine.core.accounts import (
        KEYSTORE_SYSTEM, 
        PasswordException, 
        Accounts, 
        KeyStoreFile
    )
from icenine.core.utils import extract_address, is_number
from icenine.core.metadata import AccountMeta
from icenine.core.export import ExportCSV
from icenine.contrib.transactions import Transaction

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (
        QMainWindow, 
        QApplication, 
        QMessageBox,
        QFileDialog, 
        QAction
    )
from icenine.ui import gui, AlertLevel, PasswordPromptResult
from icenine.ui.components.dialogs import (
        PasswordPrompt, 
        AboutModal, 
        TransactionDialog,
        NewAccountDialog,
        RANDOM_TAB,
        SEED_TAB
    )
from icenine.ui.windows.alias import AliasWindow
from icenine.ui.windows.transactions import TransactionWindow


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
        self.actionNew_Account.triggered.connect(self.newAccount)
        self.actionImportFromSeed.triggered.connect(self.importFromSeed)
        self.actionSave_All_Accounts.triggered.connect(self.saveAll)
        self.actionView_Aliases.triggered.connect(self.showAliases)
        self.actionImport_Aliases.triggered.connect(self.importAliases)
        self.actionExport_Aliases.triggered.connect(self.exportAliases)
        self.actionAbout_Icenine.triggered.connect(self.about)
        self.actionView_Transactions.triggered.connect(self.showTransactions)

        # Main Button
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
            # Clear UI
            self.accountsModel.clear()

            # Reload from disk
            self.accounts.load_accounts()

            # Iterate loaded accounts
            for acct in self.accounts.accounts:
                # Add it to the list
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

    def showAliases(self):
        """ Open the window to display all aliases """
        window = AliasWindow(self)
        return window.show()

    def importAliases(self):
        """ Import Alias CSV to DB """

        log.debug("showing importAliases dialog")

        # Prompt for keystore file
        fname = QFileDialog.getOpenFileName(self, 'Import CSV from...', os.path.expanduser('~'))

        if fname[0]:

            log.info("Opening alias CSV %s" % fname[0])

            try:
                xport = ExportCSV(fname[0])
                xport.importAliases()
                log.info("Imported aliases!")
            except Exception as e:
                self.alert('Unknown error!', str(e), alert_type=AlertLevel.ERROR)
            finally:
                self.showAliases()

    def exportAliases(self):
        """ Export Alias DB to CSV """

        log.debug("showing exportAliases dialog")

        # Prompt for keystore file
        fname = QFileDialog.getSaveFileName(self, 'Export CSV to...', os.path.expanduser('~'))

        if fname[0]:

            log.info("Saving alias CSV %s" % fname[0])

            try:
                xport = ExportCSV(fname[0])
                xport.exportAliases()
            except Exception as e:
                self.alert('Unknown error!', str(e), alert_type=AlertLevel.ERROR)

    def showTransactions(self):
        """ Open the window to display all aliases """
        window = TransactionWindow(self)
        return window.show()

    def newAccount(self, window=RANDOM_TAB):
        """ Open the new account window """

        newAccountWindow = NewAccountDialog()
        newAccountWindow.createAccountTabs.setTabEnabled(window, True)
        newAccountWindow.exec()

        # Load the new guy
        self.refreshAccounts()

    def importFromSeed(self):
        """ OPen the new account window on the seed tab """
        self.newAccount(window=SEED_TAB)

    def about(self):
        """ Show the About modal """
        modal = AboutModal(self)
        return modal.exec()

    def isFormValid(self):
        """ validate the transaction form """

        # Create the tx object
        self._coherceForm()
        
        try:
            assert is_hex_address(self.tx['fromAccount'])
        except AssertionError:
            log.warning("Invalid from account address")
            self.fromAccount.selectAll()
            self.fromAccount.setFocus()
            return False

        try:
            assert is_hex_address(self.tx['to'])
        except AssertionError:
            log.warning("Invalid to account address")
            self.to.selectAll()
            self.to.setFocus()
            return False

        try:
            assert is_integer(self.tx['nonce'])
            assert self.tx['nonce'] >= 0
        except AssertionError:
            log.warning("Invalid nonce")
            self.nonce.selectAll()
            self.nonce.setFocus()
            return False

        try:
            assert is_integer(self.tx['gasPrice'])
            assert self.tx['gasPrice'] >= 0
        except AssertionError:
            log.warning("Invalid gas price")
            self.gasPrice.selectAll()
            self.gasPrice.setFocus()
            return False

        try:
            log.debug("Checking if %s is a number" % self.tx['amount'])
            assert is_number(self.tx['amount'])
            assert self.tx['amount'] >= 0
        except AssertionError:
            log.warning("Invalid amount")
            self.amount.selectAll()
            self.amount.setFocus()
            return False

        if self.tx['data']:
            try:
                #assert(self.tx['data'] == "0x0" or is_hex(self.tx['data']))
                assert is_hex(self.tx['data'])
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
            self.tx['amount'] = float(self.amount.text())
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