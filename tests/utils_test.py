import sys
import os
import uuid
import pytest
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

#from testaccounts import TEST_PASSWORD, accounts
from icenine.core.utils import (
        generate_uuid, 
        is_uuid, 
        to_string, 
        new_keypair, 
        new_keypair_from_words,
        extract_address, 
        unix_time, 
        privtoaddr
    )

class TestUtils(object):
    """ Tests for utils
    """

    def test_uuid(self):
        """ Create a new UUID """

        u = generate_uuid()
        try:
            assert is_uuid(u)
        except ValueError:
            assert False

    def test_to_string(self):
        """ Test the to_string function """

        b = b'asdf'
        s = 'asdf'
        i = 10

        assert to_string(b) == b
        assert to_string(s) == b
        assert to_string(i) == b'10'

    def test_extract_address(self):
        """ Test the extract_address function """

        addr = "0x977e2f875bd8b049419deadbeef491b11b639839"
        s = 'my address is %s' % addr

        assert addr == extract_address(s)

    def test_unix_time(self):
        """ Test function unix_time """

        a = unix_time()
        b = unix_time(True)

        assert b > a

    def test_new_keypair_from_words(self):
        """ Test keypair generation from seed words """

        # Get first new pk with randomly chosen words
        key_a = new_keypair_from_words()

        # Create second keypair from the words from the original seedphrase
        key_b = new_keypair_from_words(key_a[0])

        # Make sure the PK is the same
        assert key_a[1] == key_b[1]