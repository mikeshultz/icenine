import os
import sys
import logging
import configparser

VERSION = "0.1.0a2"

CONFIG = configparser.ConfigParser()
if sys.platform == 'win32':
    confPath = '~/AppData/icenine/icenine.ini'
else:
    confPath = '~/.config/icenine/icenine.ini'
CONFIG.read(os.path.expanduser(confPath))

DEFAULT_DB_LOC = "~/.config/icenine/meta.db"
WORDLIST = CONFIG.get('default', 'wordlist', fallback=os.path.join(os.path.dirname(__file__), "../contrib/words.txt"))

LOG_LEVEL_TRANSLATE = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}

log = logging.getLogger("icenine")

# Set loglevel
if os.environ.get('BUILDENV'):
    log.setLevel(LOG_LEVEL_TRANSLATE[CONFIG.get('default', 'loglevel', fallback='debug')])
else:
    log.setLevel(LOG_LEVEL_TRANSLATE[CONFIG.get('default', 'loglevel', fallback='info')])

# Set log format
standardFormat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Try and set logfile location if available, otherwise stdout
try:
    out = logging.FileHandler(CONFIG.get('default', 'logfile'))
    print("Logging to file")
except: 
    out = logging.StreamHandler(sys.stdout)
    print("Logging to stdout")

# Set format    
out.setFormatter(standardFormat)
log.addHandler(out)