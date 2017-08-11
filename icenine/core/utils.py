import re
import datetime
from uuid import uuid4
from secp256k1 import PrivateKey, PublicKey

UUID_REGEX = r'^[A-Fa-f0-9]{8}\-[A-Fa-f0-9]{4}\-[A-Fa-f0-9]{4}\-[A-Fa-f0-9]{4}\-[A-Fa-f0-9]{12}$'
ADDRESS_REGEX = r'(0x[A-Za-z0-9]{40})'

def generate_uuid():
    """ Convert private key to a UUID """
    # TODO: Implement this
    return uuid4()

def is_uuid(val):
    """ Check if string is a UUID """
    if re.match(UUID_REGEX, val.strip()):
        return True
    else:
        return False

def new_keypair():
    """ Create a new Ethereum-compatible keypair """
    pk = PrivateKey()
    return (pk.private_key, pk.pubkey.serialize())

def extract_address(val):
    """ Pull an address out of a string """

    match = re.match(ADDRESS_REGEX, val)

    if match:
        return match.group(1)

def unix_time():
    return int(datetime.datetime.utcnow().timestamp())