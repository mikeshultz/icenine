import os
import logging as log
import configparser

CONFIG = configparser.ConfigParser()
if sys.platform == 'win32':
    confPath = '~/AppData/icenine/icenine.ini'
else:
    confPath = '~/.config/icenine/icenine.ini'
CONFIG.read(os.path.expanduser(confPath))

LOG_LEVEL_TRANSLATE = {
    'debug': log.DEBUG,
    'info': log.INFO,
    'warning': log.WARNING,
    'error': log.ERROR,
    'critical': log.CRITICAL,
}

bcKwargs = {}

# Set loglevel
bcKwargs['level'] = LOG_LEVEL_TRANSLATE[CONFIG.get('default', 'loglevel', fallback='warning')]

# Try and set logfile location if available
try:
    bcKwargs["filename"] = CONFIG.get('default', 'logfile')
except: pass

log.basicConfig(**bcKwargs)