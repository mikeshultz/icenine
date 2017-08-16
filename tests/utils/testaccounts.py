from icenine.core.utils import privtoaddr, sha3, to_string, new_keypair

def test_accounts(amt):
    """ Generate some test accounts """
    accounts = []
    keys = []
    for account_number in range(amt):
        keys.append(new_keypair()[0])
        
        accounts.append(privtoaddr(keys[-1]))
        
    return (keys, accounts)

class Account(object):
    def __init__(self, address, privkey):
        self.address = address
        self.privkey = privkey

class TestAccounts(object):
    def __init__(self):

        # Generate some addresses
        keys,addresses = test_accounts(4)

        self.mary = Account(to_string(addresses[0]), keys[0])
        self.jack = Account(to_string(addresses[1]), keys[1])
        self.sue = Account(to_string(addresses[2]), keys[2])
        self.bob = Account(to_string(addresses[3]), keys[3])

# Test accounts
accounts = TestAccounts()

# Test transactions
transactions = [
    {
        "tx": "0xd9a789ce849599b7b1a589763b5e8e18533cb503b7696aa7e746f4316a0d0257",
        "nonce": 265,
        "gasprice": 31000000000,
        "startgas": 90000,
        "to": "0x17edb913daf7584d221f4c3bdf6d42ff8b66cbb3",
        "value": 719670908886784300,
        "data": "0xba5ab9d6",
        "from_address": "0xab536e0fd327049586b79d87506f262a7e9d6c6b"
    },
    {
        "tx": "0xe7d2e325b5cf33eb27316f20aaf8928dc221bca4c08cc6c13dcae672af02f0ee",
        "nonce": 11002,
        "gasprice": 31000000000,
        "startgas": 3005694,
        "to": "0x3d04303126cd6e75324825455685b028401e0ec2",
        "value": 0,
        "data": "0xe733ca974e69646100000000000000000000000000000000000000000000000000000000",
        "from_address": "0x4a7551828712f62ac7afae08091b0fb20f659ad6"
    },
    {
        "tx": "0x499383d163aee943962c5e218f43bdfa809967c125cac46d98e449d9e3f8730e",
        "nonce": 42971,
        "gasprice": 31000000000,
        "startgas": 21001,
        "to": "0x98563de0c697d9b02deaa221f91daac242112e9f",
        "value": 1000000000000000000,
        "data": None,
        "from_address": "0x81b7e08f65bdf5648606c89998a9cc8164397647"
    }
]

TEST_PASSWORD=b"mypassword"