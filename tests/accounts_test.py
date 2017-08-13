import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from eth_utils.address import to_normalized_address
from icenine.core.utils import is_uuid
from icenine.core.accounts import KEYSTORE_SYSTEM, KeyStoreFile, Accounts
from testaccounts import TEST_PASSWORD, accounts

#TMP_DIR = "/tmp/i9test/"

class TestKeyStoreFile(object):
    """ Tests for KeyStoreFile
    """

    def setup_class(self):
        """ Create some storage we'll need for multiple tests """

        self.firstKsf = None
        self.secondKsf = None
        self.thirdKsf = None

    def test_create(self):
        """ Create a keystore file """
        print("Jack: %s" % accounts.jack.privkey)
        print("Jack: %s" % accounts.jack.address)
        # Init the KSF
        self.firstKsf = KeyStoreFile(load=False)

        # Try and create it
        self.firstKsf.save(TEST_PASSWORD, accounts.jack.privkey)

        # See if it has all the right values
        assert self.firstKsf.password == TEST_PASSWORD
        assert self.firstKsf.privkey == accounts.jack.privkey
        assert to_normalized_address(self.firstKsf.address) == to_normalized_address(accounts.jack.address)
        assert str(KEYSTORE_SYSTEM) in str(self.firstKsf.path)
        assert is_uuid(self.firstKsf.uuid)

    def test_create_with_path(self):
        """ Create a keystore file """

        # The keystore file we're going to create
        newFilePath = KEYSTORE_SYSTEM.joinpath("keystore-%s" % accounts.mary.address)

        # Init the KSF object
        self.secondKsf = KeyStoreFile(file_path=newFilePath, load=False)

        # Try and create it with our test password
        self.secondKsf.save(TEST_PASSWORD, accounts.mary.privkey)

        # Double check values
        assert self.secondKsf.password == TEST_PASSWORD
        assert self.secondKsf.privkey == accounts.mary.privkey
        assert to_normalized_address(self.secondKsf.address) == to_normalized_address(accounts.mary.address)

        # Load the file again for comparison after FS load
        reloadedKsf = KeyStoreFile(file_path=newFilePath, load=True)

        # Unlock it
        reloadedKsf.unlock(TEST_PASSWORD)

        # Check against originals
        assert reloadedKsf.privkey == accounts.mary.privkey
        assert to_normalized_address(reloadedKsf.address) == to_normalized_address(accounts.mary.address)