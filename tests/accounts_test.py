import sys
import os
import pytest
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from eth_utils.address import to_normalized_address, is_address
from icenine.core.utils import is_uuid
from icenine.core.accounts import KEYSTORE_SYSTEM, KeyStoreFile, Accounts
from testaccounts import TEST_PASSWORD, accounts

@pytest.fixture(scope='module')
def shared_keystores(request):
    """ Provide three KSF slots we can use between all tests """
    return {
        "firstKsf": None,
        "secondKsf": None,
        "thirdKsf": None,
    }


@pytest.mark.usefixtures('shared_keystores')
class TestKeyStoreFile(object):
    """ Tests for KeyStoreFile
    """

    def test_create(self, shared_keystores):
        """ Create a keystore file """
        
        # Init the KSF
        shared_keystores['firstKsf'] = KeyStoreFile(load=False)

        # Try and create it
        shared_keystores['firstKsf'].save(TEST_PASSWORD, accounts.jack.privkey)

        # See if it has all the right values
        assert shared_keystores['firstKsf'].password == TEST_PASSWORD
        assert shared_keystores['firstKsf'].privkey == accounts.jack.privkey
        assert to_normalized_address(shared_keystores['firstKsf'].address) == to_normalized_address(accounts.jack.address)
        assert str(KEYSTORE_SYSTEM) in str(shared_keystores['firstKsf'].path)
        assert is_uuid(shared_keystores['firstKsf'].uuid)

    def test_create_with_path(self, shared_keystores):
        """ Create a keystore file and make sure it can be reloaded from disk.
        """
        
        # The keystore file we're going to create
        newFilePath = KEYSTORE_SYSTEM.joinpath("keystore-%s" % accounts.mary.address)

        # Init the KSF object
        shared_keystores['secondKsf'] = KeyStoreFile(file_path=newFilePath, load=False)

        # Try and create it with our test password
        shared_keystores['secondKsf'].save(TEST_PASSWORD, accounts.mary.privkey)

        # Double check values
        assert shared_keystores['secondKsf'].password == TEST_PASSWORD
        assert shared_keystores['secondKsf'].privkey == accounts.mary.privkey
        assert to_normalized_address(shared_keystores['secondKsf'].address) == to_normalized_address(accounts.mary.address)

        # Load the file again for comparison after FS load
        reloadedKsf = KeyStoreFile(file_path=newFilePath, load=True)

        # Unlock it
        reloadedKsf.unlock(TEST_PASSWORD)

        # Check against originals
        assert reloadedKsf.privkey == accounts.mary.privkey
        assert to_normalized_address(reloadedKsf.address) == to_normalized_address(accounts.mary.address)

    def test_lock(self, shared_keystores):
        """ Make sure accounts lock and unlock """
        
        # Make sure it's unlocked
        assert shared_keystores['firstKsf'].privkey is not None

        # Lock it
        shared_keystores['firstKsf'].lock()

        # Make sure it locked
        assert shared_keystores['firstKsf'].privkey is None
        assert shared_keystores['firstKsf'].pubkey is None
        assert shared_keystores['firstKsf'].password is None

        # Unlock it
        shared_keystores['firstKsf'].unlock(TEST_PASSWORD)

        # Make sure we have important bits back
        assert shared_keystores['firstKsf'].privkey is not None
        assert shared_keystores['firstKsf'].pubkey is not None
        assert shared_keystores['firstKsf'].password is not None


@pytest.mark.usefixtures('shared_keystores')
class TestAccounts(object):
    """ Tests for Accounts object
    """

    def test_load(self, shared_keystores):
        """ Load all pre-exising keystores saved to the default location """

        accounts = Accounts()

        # Load the accounts
        accounts.load_accounts()

        # Make sure we loaded some accounts
        assert len(accounts.accounts) > 0

        addresses = [a.address for a in accounts.accounts]

        # Make sure both addresses exist in the two KSFs we created in the 
        # previous test class
        assert to_normalized_address(shared_keystores['firstKsf'].address) in addresses
        assert to_normalized_address(shared_keystores['secondKsf'].address) in addresses

    def test_new_account(self, shared_keystores):
        """ Create a new private key and KSF """

        accounts = Accounts()

        shared_keystores['thirdKsf'] = accounts.new_account(TEST_PASSWORD)

        # Make sure the KSF looks good
        assert shared_keystores['thirdKsf'].password == TEST_PASSWORD
        assert shared_keystores['thirdKsf'].privkey is not None
        assert is_address(shared_keystores['thirdKsf'].address)
        assert str(KEYSTORE_SYSTEM) in str(shared_keystores['thirdKsf'].path)
        assert is_uuid(shared_keystores['thirdKsf'].uuid)

        # Make sure it's in the object, too
        addresses = [a.address for a in accounts.accounts]
        assert shared_keystores['thirdKsf'].address in addresses