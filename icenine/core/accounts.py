# -*- coding: utf-8 -*-
import os
import sys
import json
import uuid
import bitcoin
from pathlib import Path
from eth_utils.hexidecimal import encode_hex, add_0x_prefix
from eth_utils.address import is_hex_address
from .utils import generate_uuid, is_uuid, new_keypair
from icenine.core import log
from icenine.core.utils import to_string
from icenine.core.metadata import AccountMeta
from icenine.contrib.keys import make_keystore_json, decode_keystore_json, privtoaddr

"""
Some helpful documentation:

Web3 Secrete Storage Definition - Defines how the keystore exist on the 
filesystem
https://github.com/ethereum/wiki/wiki/Web3-Secret-Storage-Definition
"""

KEYSTORE_WINDOWS = Path(os.path.expanduser("~/AppData/Web3/keystore"))
KEYSTORE_NIX = Path(os.path.expanduser("~/.web3/keystore"))

# Set one that can be used right away
if sys.platform == 'win32':
    KEYSTORE_SYSTEM = KEYSTORE_WINDOWS
else:
    KEYSTORE_SYSTEM = KEYSTORE_NIX

# Make sure the directory exists
if not KEYSTORE_SYSTEM.exists():
    KEYSTORE_SYSTEM.mkdir(mode=0o750, parents=True)

""" Exceptions """
class PasswordException(Exception): 
    pass


class KeyStoreFile:
    """ Model for a keystore file 

        Usage
        -----

        # Load all accounts from file or folder
        kp = KeyPair("/path/to/keystore")

        Attributes
        ----------
        privkey
        pubkey
        address
        password
        uuid
        path
    """

    def __init__(self, file_path=None, load=True):

        if file_path:
            self.path = Path(file_path)
        else:
            self.path = None
        self.privkey = None
        self.pubkey = None
        self.password = None
        self.address = None
        self.uuid = None
        self.alias = None
        self.keystoreObject = None

        if load:
            self._load()

    def _load(self):
        """ Load the JSON from the file, but don't decrypt """

        # Make sure it exists
        if not self.path.exists():
            raise FileNotFoundError("%s does not exist" % str(self.path))

        log.info("Loading keystore file %s" % self.path)
        
        # Open it
        with self.path.open() as keystore:
            # Get the JSON object
            self.keystoreObject = json.loads(keystore.read())
            
            # Assign some useful info bits
            self.address = add_0x_prefix(self.keystoreObject['address'])
            self.uuid = self.keystoreObject['id']

            # Get the alias if it's available
            with AccountMeta() as meta:
                self.alias = meta.getAlias(self.address)

            log.info("Loaded account %s" % self.address)

    def unlock(self, password):
        """ Load the keystore json file 
            
            Arguments
            ---------
            password : string
                The password to decrypt the file with
        """

        log.info("Unlocking account %s" % self.address)
        log.debug("password used was %s" % password)
        
        # Decrypt
        try:
            self.privkey = json_string = decode_keystore_json(self.keystoreObject, password)
            self.pubkey = bitcoin.privtopub(self.privkey)
            self.password = password
        except ValueError as e:
            if "Password incorrect" in str(e):
                raise PasswordException("Invalid password")
            else:
                raise e

    def lock(self):
        """ Get the important bits out of memory """

        log.info("Locking account %s" % self.address)

        self.privkey = None
        self.pubkey = None
        self.password = None

    def save(self, password=None, privkey=None):
        """ Save keystore file 
            
            Arguments
            ---------
            privkey : string
                The private key to be saved
            password : string
                The password to encrypt the file with
        """

        if not password and not self.password:
            raise PasswordException("Need a password to save the keyfile.")

        if not privkey and not self.privkey:
            raise ValueError("Account does not appear to have been properly generated or loaded. Cannot save.")

        # Set if we got new ones
        if privkey:
            self.privkey = privkey
        if password:
            self.password = password
        
        # Get the JSON object
        self.keystoreObject = make_keystore_json(self.privkey, self.password)

        # Store the address if we don't have it already
        if not self.address:
            self.address = privtoaddr(self.privkey)

        # Store the uuid if we don't have it already
        if not self.uuid:
            self.uuid = self.keystoreObject['id']

        # If we don't have a set path, create one
        if not self.path:
            self.path = KEYSTORE_SYSTEM.joinpath(self.keystoreObject['id'])

        log.info("Saving account %s to %s" % (self.address, self.path))

        # Write the file
        with self.path.open('w') as keystore:
            
            keystore.write(json.dumps(self.keystoreObject))

            log.info("Saved %s" % self.path)

class Accounts:
    """ Handles all available accounts

        Usage
        -----
        # Load all accounts from default location
        accts = Accounts()
        accts.load_accounts()

        Attributes
        ----------
        accounts : list
            List of KeyStoreFile objects
    """

    def __init__(self, location=None):

        self.accounts = []
        
        if location:
            self.loc = Path(location)
        else:
            self.loc = KEYSTORE_SYSTEM

    def __len__(self):
        return len(self.accounts)

    def __iter__(self):
        return iter(self.accounts)

    def get(self, addr):
        """ Get an account by address """
        for a in self.accounts:
            if a.address == addr:
                return a

    def load_accounts(self):
        """ Load all the accounts we can find in location """

        log.info("Loading accounts from %s" % self.loc)

        # Reset accounts list
        self.accounts = []

        # Load file(s)
        if self.loc.is_file():
            ksf = KeyStoreFile(self.loc)
            self.accounts.append(ksf)

        elif self.loc.is_dir():
            for file in self.loc.iterdir():
                if file.is_file():
                    # Load the keystore file JSON but do not decrypt the private
                    # key until later. 
                    try:
                        ksf = KeyStoreFile(file)
                        self.accounts.append(ksf)

                    # Ignore any files that are not JSON
                    except json.JSONDecodeError:
                        pass
        else:
            # TODO Prompt for location
            raise FileNotFoundError("Did not find any accounts!")

    def new_account(self, password):
        """ Create a new account """

        log.info("Creating new Ethereum account")

        # Create new keypair
        privkey,pubkey = new_keypair()
    
        # Init the KeyStoreFile
        ksf = KeyStoreFile(load=False)
        ksf.save(password, privkey)

        # Add the account to memory
        self.accounts.append(ksf)

        # Give it back, too
        return ksf

