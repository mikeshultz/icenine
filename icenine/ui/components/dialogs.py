# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog
from icenine.ui import passwordgui, aboutgui, transactiongui


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