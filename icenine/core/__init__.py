import os
import logging as log
import configparser

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.expanduser('~/.config/icenine/icenine.ini'))


bcKwargs = {
    "level": log.DEBUG
}

# Try and set logfile location if available
try:
    bcKwargs["filename"] = CONFIG.get('default', 'logfile')
except: pass

log.basicConfig(**bcKwargs)