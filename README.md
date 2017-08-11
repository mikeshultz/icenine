# icenine
Ethereum cold storage wallet

## API Usage

    from icenine.core.keys import Accounts
    accts = Accounts('.')
    accts.load_accounts()

## UI Development

### Generate GUI

    pyuic5 icenine/ui/mainwindow.ui -o icenine/ui/gui.py --import-from=icenine.ui
    pyuic5 icenine/ui/passwordmodal.ui -o icenine/ui/passwordgui.py --import-from=icenine.ui
    pyuic5 icenine/ui/transactiondialog.ui -o icenine/ui/transactiongui.py --import-from=icenine.ui
    pyuic5 icenine/ui/aboutmodal.ui -o icenine/ui/aboutgui.py --import-from=icenine.ui

### Generate Assets

    pyrcc5 icenine/ui/assets/assets.qrc -o icenine/ui/assets_rc.py

## Contrib Libraries

This is awful, but some modules have been brought in from pyethereum so the 
entire node implementation doesn't need to be a dependency.  These should be 
checked for update often.

### [transactions.py](https://github.com/ethereum/pyethereum/blob/develop/ethereum/transactions.py) 
(Last updated: 2017-08-08)

This file was all hacked up.  It should really be reimplemented into a separate 
package.

### [keys.py](https://github.com/ethereum/pyethereum/blob/develop/ethereum/tools/keys.py) 
(Last updated: 2017-08-08)

## Notes

- HD wallet is not suitable, jaxx is dropping it as well.
- pyethereum is a full node implementation
- pyetherapp is just a CLI util to interact with a node
- web3.py may have helpful utils that can be used, but mostly it interacts with RPC/IPC nodes
- ethereum-utils should be considered
- secp256k1-py is our main library  https://github.com/ludbb/secp256k1-py

