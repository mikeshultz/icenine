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

TEST_PASSWORD=b"mypassword"