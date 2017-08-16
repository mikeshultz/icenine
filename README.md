# icenine
[![Build Status](https://travis-ci.org/mikeshultz/icenine.svg?branch=master)](https://travis-ci.org/mikeshultz/icenine) [![Coverage Status](https://coveralls.io/repos/github/mikeshultz/icenine/badge.svg?branch=master)](https://coveralls.io/github/mikeshultz/icenine?branch=master)

Ethereum cold storage wallet

## Installation

Icenine **requires** Python >= 3.5.  If you system does not have it, you will
need to [install it manually](https://www.python.org/downloads/).

### Using PyPi

    pip install icenine

### From Git

    git clone https://github.com/mikeshultz/icenine.git && cd icenine
    python setup.py install

## Running

    icenine

## API Usage

*To be documented*

    from icenine.core.keys import Accounts
    accts = Accounts('.')
    accts.load_accounts()

## Testing

Dev dependencies should be installed first.

    pip install -r requirements.dev.txt

And a simple `pytest` command will run them all.

    pytest

## UI Development

### Generate GUI

    pyuic5 icenine/ui/mainwindow.ui -o icenine/ui/gui.py --import-from=icenine.ui
    pyuic5 icenine/ui/passwordmodal.ui -o icenine/ui/passwordgui.py --import-from=icenine.ui
    pyuic5 icenine/ui/transactiondialog.ui -o icenine/ui/transactiongui.py --import-from=icenine.ui
    pyuic5 icenine/ui/aboutmodal.ui -o icenine/ui/aboutgui.py --import-from=icenine.ui
    pyuic5 icenine/ui/aliaswindow.ui -o icenine/ui/aliasgui.py --import-from=icenine.ui

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