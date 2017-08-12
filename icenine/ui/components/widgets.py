# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QTableWidgetItem

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