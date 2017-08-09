import os
import sys
import json
import uuid
import bitcoin
from pathlib import Path
from eth_utils.hexidecimal import encode_hex, add_0x_prefix
from .utils import generate_uuid, is_uuid, new_keypair
from icenine.core import log
from icenine.contrib.keys import decode_keystore_json, privtoaddr

"""
Some helpful documentation:

Web3 Secrete Storage Definition - Defines how the keystore exist on the 
filesystem
https://github.com/ethereum/wiki/wiki/Web3-Secret-Storage-Definition
"""

KEYSTORE_WINDOWS = "~/AppData/Web3/keystore"
KEYSTORE_NIX = "~/.web3/keystore"

class KeyStoreFile:
    """ Model for a keystore file 

        Attributes
        ----------
        privkey
        pubkey
        address
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
        self.address = None
        self.uuid = None
        self.keystoreObject = None

        if load:
            self._load()

    def _load(self):
        """ Load the JSON from the file, but don't decrypt """

        # Make sure it exists
        if not self.path.exists():
            raise FileNotFoundError("%s does not exist" % str(self.path))
        
        # Open it
        with self.path.open() as keystore:
            # Get the JSON object
            self.keystoreObject = json.loads(keystore.read())
            self.address = add_0x_prefix(self.keystoreObject['address'])
            self.uuid = self.keystoreObject['id']

    def unlock(self, password):
        """ Load the keystore json file 
            
            Arguments
            ---------
            password : string
                The password to decrypt the file with
        """
        
        # Decrypt
        self.privkey = json_string = decode_keystore_json(self.keystoreObject, password)
        self.pubkey = bitcoin.privtopub(self.privkey)

    def lock(self):
        """ Get the important bits out of memory """
        self.privkey = None
        self.pubkey = None
        self.password = None

    def save(self, password, privkey=None):
        """ Save keystore file 
            
            Arguments
            ---------
            privkey : string
                The private key to be saved
            password : string
                The password to encrypt the file with
        """

        if not privkey and not self.privkey:
            raise ValueError("Account does not appear to have been properly generated or loaded. Cannot save.")

        if privkey:
            self.privkey = privkey
        self.password = password

        self.keystoreObject = make_keystore_json(self.privkey, self.password)

        if not self.path:
            if sys.platform == 'win32':
                self.loc = Path(os.path.join("~/AppData/Web3/keystore", self.keystoreObject['id']))
            else:
                self.loc = Path(os.path.join("~/.web3/keystore", self.keystoreObject['id']))

        with self.path.open('w') as keystore:
            
            keystore.write(json.dumps(self.keystoreObject))

            log.info("Saved %s" % self.path)

class Accounts:
    """ Handles all available accounts

        Usage
        -----
        # Load all accounts from default location
        accts = Accounts()
        # Load all accounts from file or folder
        kp = KeyPair("/path/to/keystore")

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
            if sys.platform == 'win32':
                self.loc = Path("~/AppData/Web3/keystore")
            else:
                self.loc = Path("~/.web3/keystore")

    def load_accounts(self):
        """ Load all the accounts we can find in location """

        # Reset accounts list
        self.accounts = []

        # Load file(s)
        if self.loc.is_file():
            self.load(self.loc)

        elif self.loc.is_dir():
            for file in self.loc.iterdir():
                print(file)
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

        # Create new keypair
        privkey,pubkey = new_keypair()
    
        # Init the KeyStoreFile
        ksf = KeyStoreFile(load=False)
        ksf.save(password, privkey)
        return True

