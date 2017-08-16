import sys
import os
import pytest
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from utils.testaccounts import accounts, transactions
from icenine.core.metadata import AccountMeta

TEST_DB_LOC=":memory:"


class TestAccountMeta(object):
    """ Tests for AccountMeta
    """

    def test_create_db(self):
        """ Create a new database """

        with AccountMeta(db_location=TEST_DB_LOC) as meta:

            # Query for the alias table
            res = meta.curse.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='alias';")

            # Make sure we found it
            assert res.fetchone()[0] == 'alias'

            # Query for the trans table
            res = meta.curse.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='trans';")

            # Make sure we found it
            assert res.fetchone()[0] == 'trans'

    def test_create_alias(self):
        """ Create an alias """

        with AccountMeta(db_location=TEST_DB_LOC) as meta:

            # Add an alias for Mary
            meta.addAlias(accounts.mary.address, "Mary")

            # Get it from the DB
            res = meta.getAlias(accounts.mary.address)

            # Make sure we got a result
            assert res is not None

            # Get the full set from the DB and look for Mary
            res = meta.getAliases()

            assert res is not None
            assert res[0][1] == accounts.mary.address

    def test_update_alias(self):
        """ Make sure aliases can be updated """

        with AccountMeta(db_location=TEST_DB_LOC) as meta:

            # Add an alias for Mary
            meta.addAlias(accounts.mary.address, "Mary")

            # Check it
            res = meta.getAlias(accounts.mary.address)
            assert res == "Mary"

            # Change it
            meta.updateAliasAddress("Mary", accounts.bob.address)

            # Check it
            res = meta.getAlias(accounts.bob.address)
            assert res == "Mary"

            # Change it
            meta.updateAliasAlias(accounts.bob.address, "Bob")

            # Check it
            res = meta.getAlias(accounts.bob.address)
            assert res == "Bob"

    def test_transactions(self):
        """ Make sure transaction methods work as expected """

        with AccountMeta(db_location=TEST_DB_LOC) as meta:

            # Add a transaction
            meta.addTransaction(transactions[0]['tx'], transactions[0]['nonce'], 
                transactions[0]['gasprice'], transactions[0]['startgas'], 
                transactions[0]['to'], transactions[0]['value'], 
                transactions[0]['data'], transactions[0]['from_address'])

            # Get it back
            trans = meta.getTransaction(transactions[0]['tx'])

            # Verify it stored and fetched accurately
            assert trans[0] == transactions[0]['tx']
            assert trans[1] == transactions[0]['nonce']
            assert trans[2] == transactions[0]['gasprice']
            assert trans[3] == transactions[0]['startgas']
            assert trans[4] == transactions[0]['to']
            assert trans[5] == transactions[0]['value']
            assert trans[6] == transactions[0]['data']
            assert trans[8] == transactions[0]['from_address']

            # Add another transaction
            meta.addTransaction(transactions[1]['tx'], transactions[1]['nonce'], 
                transactions[1]['gasprice'], transactions[1]['startgas'], 
                transactions[1]['to'], transactions[1]['value'], 
                transactions[1]['data'], transactions[1]['from_address'])

            # Get all transactions
            trans = meta.getTransactions()

            # Make sure we got 2
            assert len(trans) == 2

            for t in trans:
                print(t[7])

            # Get the last transaction
            trans = meta.getLastTransaction()

            # Make sure it's the last one we added
            assert trans[0] == transactions[1]['tx']

            # Make sure nonce is being calculated correctly, too
            nonce = meta.getNonce(transactions[1]['from_address'])

            assert nonce == transactions[1]['nonce'] + 1



