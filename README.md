# icenine
[![Build Status](https://travis-ci.org/mikeshultz/icenine.svg?branch=master)](https://travis-ci.org/mikeshultz/icenine) [![Coverage Status](https://coveralls.io/repos/github/mikeshultz/icenine/badge.svg?branch=master)](https://coveralls.io/github/mikeshultz/icenine?branch=master)

Ethereum cold storage wallet written in Python.

### Features

- Simple interface
- Creates raw transactions that can be sent from any insecure node or service
- Stores transactions for later reference
- Keeps track of current nonce and remembers last gas price and limit
- Can create accounts as needed from a random seed or seed words
- Can import seed words used for other wallets(NEEDS TESTING!)
- Can import standard keystore files from other wallets like go-ethereum(geth)
- Has address alias support so you can give accounts regular words for names
- Can run on any operating system with at least Python 3.4

**NOTE: This software is currently ALPHA at BEST!  Use at your own risk and 
ALWAYS back up your key files!**

## Installation

Icenine **requires** Python >= 3.5.  If you system does not have it, you will
need to [install it manually](https://www.python.org/downloads/).

### Using PyPi

**Not yet implemented**

    pip install icenine

### From Git

    git clone https://github.com/mikeshultz/icenine.git && cd icenine
    python setup.py install

## Running

    icenine

## See Also

- [API Usage](docs/api.md)
- [Configuration](docs/config.md)
- [Development Notes](docs/development.md)
- [Import/Export Aliases](docs/aliases.md)
- [Key File Management](docs/keys.md)