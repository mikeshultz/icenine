# -*- coding: utf-8 -*-
import re
import datetime
import bitcoin
from uuid import UUID, uuid4
from secp256k1 import PrivateKey, PublicKey
from eth_utils import to_normalized_address
from Crypto.Hash import keccak
from icenine.core import WORDLIST
from icenine.core.seedwords import SeedWords

sha3_256 = lambda x: keccak.new(digest_bits=256, data=x).digest()

UUID_REGEX = r'^[A-Fa-f0-9]{8}\-[A-Fa-f0-9]{4}\-[A-Fa-f0-9]{4}\-[A-Fa-f0-9]{4}\-[A-Fa-f0-9]{12}$'
ADDRESS_REGEX = r'(0x[A-Fa-f0-9]{40})'

def sha3(seed):
    return sha3_256(to_string(seed))

def generate_uuid():
    """ Convert private key to a UUID """
    return uuid4()

def is_uuid(val):
    """ Check if string is a UUID """
    if val and type(val) == UUID:
        return True
    if not val or type(val) not in (str, bytes):
        return False
    if re.match(UUID_REGEX, val.strip()):
        return True
    else:
        return False

def is_number(val):
    """ Check if a value is a number """
    if not val:
        return False
    if type(val) in (int, float):
        return True
    if re.match(r'^[0-9]+\.?[0-9]*$', val):
        return True
    return False

def to_string(value):
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return bytes(value, 'utf-8')
    if isinstance(value, int):
        return bytes(str(value), 'utf-8')

def new_keypair():
    """ Create a new Ethereum-compatible keypair """
    pk = PrivateKey()
    return (pk.private_key, pk.pubkey.serialize())

def new_keypair_from_words(seedphrase=None):
    """ Create a new Ethereum-compatible keypair from a seedphrase

        Notes
        -----
        Hashing algorithm is based off of parity seedphrase account generation
    """

    # Get a seedphrase if one is not provided
    if not seedphrase:
        sw = SeedWords(WORDLIST)
        seedphrase = sw.random_seed_words()

    # Get first hash of it
    h = sha3(' '.join(seedphrase))
    
    # Hash the hash about this many times
    for i in range(16384):
        h = sha3(h)
    
    # And a little bit more hashing
    while h[0] != 0:
        h = sha3(h)

    pk = PrivateKey(h)

    return (seedphrase, pk.private_key, pk.pubkey.serialize())

def extract_address(val):
    """ Pull an address out of a string """

    match = re.search(ADDRESS_REGEX, val)

    if match:
        return match.group(1)
    return None

def unix_time(micro=False):
    """ Get the current unix timestamp 

        Parameters
        ----------
        micro - boolean
            If micro is set, microseconds will be included
    """
    stamp = datetime.datetime.utcnow().timestamp()
    if micro:
        return stamp
    else:
        return int(stamp)

def privtoaddr(k):
    """ Turn a private key into an ethereum address """
    pk = PrivateKey(k)
    return to_normalized_address(sha3(pk.pubkey.serialize(compressed=False)[1:])[12:])