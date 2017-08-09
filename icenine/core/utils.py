import re
from uuid import uuid4
from secp256k1 import PrivateKey, PublicKey

UUID_REGEX = r'^[A-Fa-f0-9]{8}\-[A-Fa-f0-9]{4}\-[A-Fa-f0-9]{4}\-[A-Fa-f0-9]{4}\-[A-Fa-f0-9]{12}$'


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