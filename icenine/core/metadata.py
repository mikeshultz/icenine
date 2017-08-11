import os
import sqlite3
import datetime
from icenine.core import CONFIG, DEFAULT_DB_LOC
from icenine.core.utils import unix_time

class AccountMeta(object):
    """ DB operations class for meta data 

        Usage
        -----
        with AccountMeta() as meta:
            nonce = meta.getNonce()
    """

    def __init__(self):

        self.db_file = os.path.expanduser(CONFIG.get('default', 'dbfile', fallback=DEFAULT_DB_LOC))
        self.create_tables = False

        # If the db doesn't exist yet, we will need to recreate it
        if not os.path.exists(self.db_file):
            self.create_tables = True

    def __enter__(self):

        # Connect
        self.db = sqlite3.connect(self.db_file)

        # Get cursor
        self.curse = self.db.cursor()

        # Create tables if necessary
        if self.create_tables:
            self.curse.execute("CREATE TABLE alias (address text, alias text);")
            self.curse.execute("CREATE TABLE trans (tx text, nonce integer, gasprice integer, startgas integer, to_address text, from_address text, value integer, data text, stamp integer);")
            self.create_tables = False

        # Give back ourselves
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.commit()
        self.db.close()

    def getAlias(self, address):
        """ Get an alias for an address """

        self.curse.execute("SELECT alias FROM alias WHERE address = ?", [address])

        result = self.curse.fetchone()

        if result and len(result) > 0:
            return result[0]
        return None

    def getAliases(self):
        """ Get all aliases """

        self.curse.execute("SELECT alias, address FROM alias")

        result = self.curse.fetchall()

        if result and len(result) > 0:
            return result
        return None

    def addAlias(self, address, alias):
        """ Add an alias """

        self.curse.execute("INSERT INTO alias (address,alias) VALUES (?,?)", 
            (address, alias))

    def getTransactions(self):
        """ Get all transactions """

        self.curse.execute("SELECT tx, nonce, gasprice, startgas, to_address, value, data, stamp, from_address FROM trans")

        return self.curse.fetchall()

    def getTransaction(self, txhash):
        """ Get a transaction """

        self.curse.execute("SELECT tx, nonce, gasprice, startgas, to_address, value, data, stamp, from_address FROM trans WHERE tx = ?", [txhash])

        return self.curse.fetchone()

    def getLastTransaction(self, address=None):
        """ Return the latest transaction """

        if address:
            self.curse.execute("SELECT tx, nonce, gasprice, startgas, to_address, value, data, stamp FROM trans WHERE from_address = ? ORDER BY stamp DESC LIMIT 1", [address])
        else:
            self.curse.execute("SELECT tx, nonce, gasprice, startgas, to_address, value, data, stamp, from_address FROM trans ORDER BY stamp DESC LIMIT 1")

        return self.curse.fetchone()

    def addTransaction(self, tx, nonce, gasprice, startgas, to, value, data, from_address=None):
        """ Add a transaction """

        self.curse.execute("INSERT INTO trans (tx, nonce, gasprice, startgas, to_address, value, data, stamp, from_address) VALUES (?,?,?,?,?,?,?,?,?)", 
            (tx, nonce, gasprice, startgas, to, value, data, unix_time(), from_address))

    def getNonce(self, address=None):
        """ Get the current nonce """
        tx = self.getLastTransaction(address)
        if tx and len(tx) > 0:
            return tx[1] + 1
        return 0