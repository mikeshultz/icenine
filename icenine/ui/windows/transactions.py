# -*- coding: utf-8 -*-
from datetime import datetime
from web3 import Web3
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QHeaderView
from icenine.core import log
from icenine.core.accounts import Accounts
from icenine.core.metadata import AccountMeta
from icenine.ui import transactionwindowgui
from icenine.ui.components.widgets import TableWidgetItem


class TransactionWindow(QMainWindow, transactionwindowgui.Ui_TransactionsWindow):
    """ The alias table window 

        Notes
        -----
        Column 0 - tx
        Column 1 - nonce
        Column 1 - gasprice
        Column 1 - startgas
        Column 1 - to_address
        Column 1 - value
        Column 1 - data
        Column 1 - stamp
        Column 1 - from_address
    """
    def __init__(self, parent=None):
        super(TransactionWindow, self).__init__(parent)

        # Create elements
        self.setupUi(self)

        columns = 9

        # Set header resizing
        for i in range(columns):
            self.transactionTable.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)

        # Get accounts
        # TODO: Should probably share the same instance with the main window
        self.accounts = Accounts()
        self.accounts.load_accounts()

        with AccountMeta() as meta:

            # Populate account dropdown
            self.accountComboBox.addItem('All Accounts')

            # Add the accounts to the trop down
            for account in self.accounts.accounts:
                self.accountComboBox.addItem(account.address)

            self.accountComboBox.currentTextChanged.connect(self.change_account)

        self.load_transactions()

    def change_account(self):
        """ Switch to an account that was selected in the dropdown """

        log.debug("Switching to account %s" % self.accountComboBox.currentText())

        self.load_transactions(self.accountComboBox.currentText())

    def load_transactions(self, account=None):
        """ Load transactions and put them in the table """

        log.info("Loading transactions for %s" % account)

        # No account for "All Accounts"
        if account == "All Accounts":
            account = None

        self.transactions = []

        with AccountMeta() as meta:

            # Get data
            self.transactions = meta.getTransactions(account)

            if self.transactions:

                # Set table headers
                self.transactionTable.setHorizontalHeaderLabels(['txhash', 'Stamp', 'Nonce', 'Gas Price', 'Gas Limit', 'To', 'Value', 'Data', 'From'])

                # Set row count
                self.transactionTable.setRowCount(len(self.transactions))

                # Populate table
                i = 0
                for trans in self.transactions:
                    # TX
                    transactionItem = TableWidgetItem(trans[0])
                    transactionItem.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
                    self.transactionTable.setItem(i, 0, transactionItem)

                    # stamp
                    if trans[7]:
                        stmp = datetime.fromtimestamp(trans[7]).strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        stmp = ""
                    stampItem = TableWidgetItem(stmp)
                    stampItem.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
                    self.transactionTable.setItem(i, 1, stampItem)

                    # Nonce
                    nonceItem = TableWidgetItem(str(trans[1]))
                    nonceItem.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
                    self.transactionTable.setItem(i, 2, nonceItem)

                    # gasprice
                    gaspriceItem = TableWidgetItem(str(trans[2]))
                    gaspriceItem.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
                    self.transactionTable.setItem(i, 3, gaspriceItem)

                    # startgas
                    startgasItem = TableWidgetItem(str(trans[3]))
                    startgasItem.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
                    self.transactionTable.setItem(i, 4, startgasItem)

                    # to_address
                    toItem = TableWidgetItem(trans[4])
                    toItem.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
                    self.transactionTable.setItem(i, 5, toItem)

                    # value
                    if trans[5]:
                        val = Web3.fromWei(trans[5], "ether")
                    else:
                        val = 0
                    valueItem = TableWidgetItem(str(val) + "Ξ")
                    valueItem.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
                    self.transactionTable.setItem(i, 6, valueItem)

                    # data
                    dataItem = TableWidgetItem(trans[6])
                    dataItem.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
                    self.transactionTable.setItem(i, 7, dataItem)

                    # from_address
                    fromItem = TableWidgetItem(trans[8])
                    fromItem.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
                    self.transactionTable.setItem(i, 8, fromItem)

                    # Increment row count
                    i += 1

            # Has no transactions
            else:
                self.transactionTable.setRowCount(0)