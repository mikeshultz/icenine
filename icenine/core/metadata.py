# -*- coding: utf-8 -*-
import os
import sqlite3
import datetime
from eth_utils.address import is_hex_address
from icenine.core import CONFIG, DEFAULT_DB_LOC, log
from icenine.core.utils import unix_time

IntegrityError = sqlite3.IntegrityError

class AccountMeta(object):
    """ DB operations class for meta data 

        Usage
        -----
        with AccountMeta() as meta:
            nonce = meta.getNonce()
    """

    def __init__(self, db_location=None):
        if db_location:
            dbf = os.path.expanduser(db_location)
        else:
            dbf = os.path.expanduser(CONFIG.get('default', 'dbfile', fallback=DEFAULT_DB_LOC))

        self.db_file = dbf
        self.create_database = False

        # If the db doesn't exist yet, we will need to recreate it
        if not os.path.exists(self.db_file):
            self.create_database = True

    def __enter__(self):

        # Make sure the directories exist, too
        if self.create_database:
            if self.db_file != ':memory:':
                d = os.path.dirname(self.db_file)
                log.debug("Creating DB directory %s" % d)
                os.makedirs(d, mode=0o750, exist_ok=True)

        
        log.debug("Opening database %s" % self.db_file)

        # Connect
        self.db = sqlite3.connect(self.db_file)

        # Get cursor
        self.curse = self.db.cursor()

        # Create tables if necessary
        if self.create_database:
            self.curse.execute("CREATE TABLE alias (address text UNIQUE, alias text);")
            self.curse.execute("CREATE TABLE trans (tx text PRIMARY KEY, nonce integer, gasprice integer, startgas integer, to_address text, from_address text, value integer, data text, stamp integer);")
            self.create_database = False

        # Give back ourselves
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.commit()
        self.db.close()

    def getAlias(self, address):
        """ Get an alias for an address """

        if not is_hex_address(address):
            raise ValueError("Invalid address")

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

        if not is_hex_address(address):
            raise ValueError("Invalid address")

        self.curse.execute("INSERT INTO alias (address,alias) VALUES (?,?)", 
            (address, alias))

    def updateAliasAddress(self, alias, address):
        """ Update the address for an alias """

        if not is_hex_address(address):
            raise ValueError("Invalid address")

        self.curse.execute("UPDATE alias SET address = ? WHERE alias = ?", [address, alias])

    def updateAliasAlias(self, address, alias):
        """ Update the alias for an address """

        if not is_hex_address(address):
            raise ValueError("Invalid address")

        self.curse.execute("UPDATE alias SET alias = ? WHERE address = ?", [alias, address])

    def getTransactions(self, address=None):
        """ Get all transactions """

        if address:
            self.curse.execute("SELECT tx, nonce, gasprice, startgas, to_address, value, data, stamp, from_address FROM trans WHERE from_address = ? ORDER BY stamp", [address])
        else:    
            self.curse.execute("SELECT tx, nonce, gasprice, startgas, to_address, value, data, stamp, from_address FROM trans ORDER BY stamp")

        return self.curse.fetchall()

    def getTransaction(self, txhash):
        """ Get a transaction """

        self.curse.execute("SELECT tx, nonce, gasprice, startgas, to_address, value, data, stamp, from_address FROM trans WHERE tx = ?", [txhash])

        return self.curse.fetchone()

    def getLastTransaction(self, address=None):
        """ Return the latest transaction """

        if address and not is_hex_address(address):
            raise ValueError("Invalid address")

        if address:
            self.curse.execute("SELECT tx, nonce, gasprice, startgas, to_address, value, data, stamp FROM trans WHERE from_address = ? ORDER BY stamp DESC LIMIT 1", [address])
        else:
            self.curse.execute("SELECT tx, nonce, gasprice, startgas, to_address, value, data, stamp, from_address FROM trans ORDER BY stamp DESC LIMIT 1")

        return self.curse.fetchone()

    def addTransaction(self, tx, nonce, gasprice, startgas, to, value, data, from_address=None):
        """ Add a transaction """

        self.curse.execute("INSERT INTO trans (tx, nonce, gasprice, startgas, to_address, value, data, stamp, from_address) VALUES (?,?,?,?,?,?,?,?,?)", 
            (tx, nonce, gasprice, startgas, to, value, data, unix_time(True), from_address))

    def getNonce(self, address=None):
        """ Get the current nonce """
        tx = self.getLastTransaction(address)
        if tx and len(tx) > 0:
            return tx[1] + 1
        return 0