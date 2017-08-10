from PyQt5.QtCore import QAbstractItemModel, QModelIndex
from PyQt5.QtGui import QStandardItem

class AccountsModel(QAbstractItemModel):
    """ Model for an account """

    def __init__(self, parent, data):
       super(AccountsModel, self).__init__(parent)
       self.setData(data)

    def columnCount(self, parent = QModelIndex()):
        return 1

    def rowCount(self, parent = QModelIndex()):
        item = parent.internalPointer()
        return len(self.itemData)

    def setData(self, data, parent=QModelIndex()):
        for acct in data:
            newItem = QStandardItem(str(acct.address))
            self.itemData.append(newItem)
        self.dataChanged()

"""
    def index():
        pass

    def parent(self):
        pass

    def rowCount(self):
        pass

    def columnCount(self):
        return 1

    def data(self):
        pass"""