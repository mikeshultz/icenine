# -*- coding: utf-8 -*-
import os
import csv
from icenine.core import CONFIG, DEFAULT_DB_LOC, log
from icenine.core.utils import to_normalized_address
from icenine.core.metadata import AccountMeta, IntegrityError


class ExportCSV(object):
    """ Export things to a CSV file """

    def __init__(self, filename, db_file=None):

        # Create directories if they don't exist
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename), mode=0o750, exist_ok=True)

        self.filename = filename
        self.db_file = db_file

        self.warnings = []

    def exportAliases(self):
        """ Export Aliases to a CSV file """

        log.debug("Creating alias CSV %s" % self.filename)

        # Get aliases from DB
        with AccountMeta(self.db_file) as meta:

            aliases = meta.getAliases()

        log.debug("Saving alias CSV %s" % self.filename)

        # Open file for writing
        with open(self.filename, "w") as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)

            for alias in aliases:

                writer.writerow([alias[0], alias[1].decode('utf-8')])

        log.debug("Saved Alias CSV  %s!" % self.filename)

    def importAliases(self):
        """ Import aliases from a CSV """

        log.debug("Opening alias CSV %s" % self.filename)

        self.warnings = []

        # Open CSV
        with open(self.filename, "r") as csvfile:
            reader = csv.reader(csvfile)

            # Open DB
            with AccountMeta(self.db_file) as meta:

                for row in reader:

                    try:
                        # Add the row to the DB
                        log.debug("Attempting to insert alias %s for address %s" % (row[0], row[1]))
                        meta.addAlias(row[1], row[0])
                    except IntegrityError as e:
                        if "UNIQUE" in str(e):
                            self.warnings.append("ExportCSV: Failed importing alias %s!" % row[1])
                            log.warning(warnings[-1])
                        else:
                            raise e

        # TODO: Display any warnings somehow