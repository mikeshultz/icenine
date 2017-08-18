import sys
import os
import pytest
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from testaccounts import accounts, transactions
from icenine.core.utils import to_normalized_address
from icenine.core.metadata import AccountMeta
from icenine.core.export import ExportCSV

TEST_DB_LOC="/tmp/test-%s.db" % datetime.utcnow().timestamp()
TEST_DB_LOC2="/tmp/test2-%s.db" % datetime.utcnow().timestamp()
TEST_CSV_LOC="/tmp/test-%s.csv" % datetime.utcnow().timestamp()


class TestExportCSV(object):
    """ Tests for ExportCSV
    """

    def test_create_db(self):
        """ Create a new database with aliases """

        with AccountMeta(db_location=TEST_DB_LOC) as meta:

            # Add an alias for Mary
            meta.addAlias(accounts.mary.address, "Mary")
            meta.addAlias(accounts.bob.address, "Bob")

            # Make sure it worked
            res = meta.getAlias(accounts.mary.address)

            # Make sure we got a result
            assert res == "Mary"

    def test_export_aliases(self):
        """ Export CSVs to a test CSV """

        # Initialize CSV handler
        xport = ExportCSV(TEST_CSV_LOC, db_file=TEST_DB_LOC)

        # Export them
        xport.exportAliases()

        assert os.path.exists(TEST_CSV_LOC)

    def test_import_aliases(self):
        """ Test importing a CSV """

        # Init
        xport = ExportCSV(TEST_CSV_LOC, db_file=TEST_DB_LOC2)

        # Import
        xport.importAliases()

        # Open original DB
        with AccountMeta(db_location=TEST_DB_LOC) as meta:

            # Get aliases from DB for check
            original_set = meta.getAliases()

        # Open original DB for comparison
        with AccountMeta(db_location=TEST_DB_LOC2) as meta:

            # Check every alias in the original DB
            for alias in original_set:
                
                # And make sure it exists in the new DB
                assert meta.getAlias(to_normalized_address(alias[1])) is not None