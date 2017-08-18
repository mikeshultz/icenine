# Icenine Configuration

Configuration file is located in `%APPDATA%/icenine/icenine.ini` on Windows and 
`~/.config/icenine/icenine.ini` on everything else.

## INI Options

### Example File

The following are all of the options for the config.  All are optional. 

    [default]
    logfile = /var/log/icenine.log
    loglevel = warning
    dbfile = ~/.config/icenine/meta.db
    wordlist = /path/to/wordlist.txt

### Option Breakdown

`logfile`: Where Icenine should log to.  Normally, all logging is sent to 
stdout.

`loglevel`: The level of logging that should be done.  Options are `debug`, 
`info`, `warning`, `error`, and `critical`.

`dbfile`: Where the database should be saved.  While nothing is inherently 
valuable is stored in here, the security paranoid could set this to a location 
in `/tmp` if they're using `tmpfs`.  That way, the DB is destroyed on reboot.

`wordlist`: A list of words to use as random seed words for account generation.
The default word list comes with 40,089 english nouns from a scrabble dictionary.
While this should be reasonably secure, the security minded may want to use 
their own word list.  File should be formatted with one word per line.