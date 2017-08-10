import sqlite3
from icenine.core import CONFIG, DEFAULT_DB_LOC

class DB:
    """ DB operations class to be extended """
    def __enter__(self):
        self.db = sqlite3.connect(CONFIG.get('default', 'dbfile', fallback=DEFAULT_DB_LOC))
        self.curse = self.db.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.commit()
        self.db.close()

    def getAlias(self, address):
        """ Get an alias for an address """

        self.curse.execute("SELECT alias FROM alias WHERE address = ?", address)

        return self.curse.fetchone()

    def addAlias(self, address, alias):
        """ Add an alias """

        self.curse.execute("INSERT INTO alias (address,alias) VALUES (?,?)", 
            (address, alias))

    def getTransactions(self):
        """ Get all transactions """

        self.curse.execute("SELECT tx, nonce, gasprice, startgas, to, value, data, stamp FROM transaction")

        return self.curse.fetchall()

    def getTransaction(self, txhash):
        """ Get a transaction """

        self.curse.execute("SELECT tx, nonce, gasprice, startgas, to, value, data, stamp FROM transaction WHERE tx = ?", txhash)

        return self.curse.fetchone()

    def getLatestTransaction(self):
        """ Return the latest transaction """

        self.curse.execute("SELECT tx, nonce, gasprice, startgas, to, value, data, stamp FROM transaction ORDER BY stamp DESC LIMIT 1")

        return self.curse.fetchone()

    def addTransaction(self, tx, nonce, gasprice, startgas, to, value, data):
        """ Add a transaction """

        self.curse.execute("INSERT INTO transaction (tx, nonce, gasprice, startgas, to, value, data) VALUES (?,?,?,?,?,?,?)", 
            (tx, nonce, gasprice, startgas, to, value, data))



class AccountMeta(DB):
    """ Handle storage of general metadata for accounts and contacts """

    def getNonce(self):
        """ Get the current nonce """
        tx = self.getLatestTransaction()
        if len(tx) > 0:
            return tx[1] + 1
        return 0
