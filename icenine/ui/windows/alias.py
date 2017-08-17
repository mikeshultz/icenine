# -*- coding: utf-8 -*-
from eth_utils.address import is_hex_address
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QHeaderView
from icenine.core import log
from icenine.core.metadata import AccountMeta
from icenine.ui import aliasgui
from icenine.ui.components.widgets import TableWidgetItem


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