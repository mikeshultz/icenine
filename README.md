# icenine
Ethereum cold storage wallet

## API Usage

    from icenine.core.keys import Accounts
    accts = Accounts('.')
    accts.load_accounts()

## Notes

- HD wallet is not suitable, jaxx is dropping it as well.
- pyethereum is a full node implementation
- pyetherapp is just a CLI util to interact with a node
- web3.py may have helpful utils that can be used, but mostly it interacts with RPC/IPC nodes
- ethereum-utils should be considered
- secp256k1-py is our main library  https://github.com/ludbb/secp256k1-py

