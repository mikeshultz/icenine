# Development

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
    pyuic5 icenine/ui/newaccountdialog.ui -o icenine/ui/newaccountgui.py --import-from=icenine.ui
    pyuic5 icenine/ui/transactionwindow.ui -o icenine/ui/transactionwindowgui.py --import-from=icenine.ui

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

## Creating a Release

1) Recreate or `rebase` the `release` branch.
2) Update `VERSION` in `icenine/core/__init__.py`
3) Update `version` and `download_url` in `setup.py`
4) Commit
5) Tag release with PEP440 version number prefixed with 'v'
6) Push to `origin`
7) `python setup.py sdist upload -r [repos]`
8) Merge release changes back into `master`