# -*- coding: utf-8 -*-
from eth_utils.hexidecimal import encode_hex
from icenine.core import log, VERSION
from icenine.core.accounts import KeyStoreFile
from icenine.core.utils import to_string, privtoaddr, new_keypair, new_keypair_from_words
from PyQt5.QtWidgets import QDialog
from icenine.ui import AlertLevel, PasswordPromptResult, passwordgui, aboutgui, transactiongui, newaccountgui
from icenine.ui.app import AlertLevel


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
        self.versionNumber.setText("Version %s" % VERSION)

class TransactionDialog(QDialog, transactiongui.Ui_transactionDialog):
    def __init__(self, rawtx, parent=None):
        super(TransactionDialog, self).__init__(parent)
        self.setupUi(self)
        self.rawTransaction.setText(rawtx)

RANDOM_TAB = 0
SEED_TAB = 1

class NewAccountDialog(QDialog, newaccountgui.Ui_newAccountDialog):
    def __init__(self, parent=None):
        super(NewAccountDialog, self).__init__(parent)
        self.setupUi(self)

        # Setup button events
        self.generateRandomButton.clicked.connect(self.generateRandomAccount)
        self.generateWordsButton.clicked.connect(self.generateWordsAccount)
        self.loadWordsButton.clicked.connect(self.loadFromWords)
        self.buttonBox.accepted.connect(self.save)
        self.buttonBox.rejected.connect(self.cancel)

        self.currentRandomKeyPair = None
        self.currentWordsKeyPair = None

    def generateRandomAccount(self):
        """ Generate a random account """

        log.info("UI: Generating new random private key")

        # 10%
        self.accountGenerationProgress.setValue(10)

        # Generate a new keypair
        privkey, pubkey = new_keypair()

        # 60%
        self.accountGenerationProgress.setValue(60)

        # Set for future reference
        self.currentRandomKeyPair = (privkey, pubkey)

        # 75%
        self.accountGenerationProgress.setValue(75)

        # Populate UI
        self.privateKeyRandom.setText(encode_hex(privkey))
        self.addressRandom.setText(privtoaddr(privkey))

        # 100%
        self.accountGenerationProgress.setValue(100)

    def generateWordsAccount(self):
        """ Generate an account with seed words """

        log.info("UI: Generating new random private key")

        # 10%
        self.accountGenerationProgress.setValue(10)

        # Generate a new keypair
        seedphrase, privkey, pubkey = new_keypair_from_words()

        log.debug("New phrase: %s - New key - %s" % (' '.join(seedphrase), pubkey))

        # 60%
        self.accountGenerationProgress.setValue(60)

        # Set for future reference
        self.currentWordsKeyPair = (privkey, pubkey)

        # 75%
        self.accountGenerationProgress.setValue(75)

        # Populate UI
        self.seedWords.setText(' '.join(seedphrase))
        self.privateKeySeed.setText(encode_hex(privkey))
        self.addressSeed.setText(privtoaddr(privkey))

        # 100%
        self.accountGenerationProgress.setValue(100)

    def loadFromWords(self):
        """ Load/create an account from words provided by user """

        log.info("UI: Generating account from seed words")

        # 10%
        self.accountGenerationProgress.setValue(10)

        seedphrase = self.seedWords.toPlainText()

        if len(seedphrase) < 48:
            parent.alert("Low entropy!", "Provided seed phrase has a low amount of entropy and is insecure.  Consider using more words.", alert_type=AlertLevel.WARNING)

        # Generate keys from the phrase
        digestedseed, privkey, pubkey = new_keypair_from_words(seedphrase)

        log.debug("New phrase: %s - New key - %s" % (' '.join(seedphrase), pubkey))

        # If this isn't the same, something went seriously wrong in processing
        assert digestedseed == seedphrase

        # 60%
        self.accountGenerationProgress.setValue(60)

        # Set for future reference
        self.currentWordsKeyPair = (privkey, pubkey)

        # 75%
        self.accountGenerationProgress.setValue(75)

        # Populate UI
        self.privateKeySeed.setText(encode_hex(privkey))
        self.addressSeed.setText(privtoaddr(privkey))

        # 100%
        self.accountGenerationProgress.setValue(100)



    def save(self):
        """ Save the generated keypair """

        if self.createAccountTabs.currentIndex() == RANDOM_TAB:

            log.debug("UI: Saving randomly generated account...")

            assert self.currentRandomKeyPair is not None

            # Prompt for password
            # TODO: Create a confirm prompt
            res,passwd = PasswordPrompt.getPassword(self.addressRandom.text(), self)

            # Create the KSF
            ksf = KeyStoreFile(load=False)
            ksf.save(passwd, self.currentRandomKeyPair[0])

            log.info("UI: Saved new account!")

        elif self.createAccountTabs.currentIndex() == SEED_TAB:

            log.debug("UI: Saving seed generated account...")

            assert self.currentWordsKeyPair is not None

            # Prompt for password
            # TODO: Create a confirm prompt
            res,passwd = PasswordPrompt.getPassword(self.addressSeed.text(), self)

            # Create the KSF
            ksf = KeyStoreFile(load=False)
            ksf.save(passwd, self.currentWordsKeyPair[0])

            log.info("UI: Saved new account!")

        else:
            raise NotImplementedError("Unknown account creation tab.  I don't know what's going on.'")

    def cancel(self):
        """ No new accounts today, kids """

        # Reset internal tracking
        self.currentRandomKeyPair = None
        self.currentWordsKeyPair = None

        # Reset fields
        self.privateKeyRandom.setText("")
        self.addressRandom.setText("")