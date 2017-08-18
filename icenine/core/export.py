# -*- coding: utf-8 -*-
import os
import csv
from icenine.core import CONFIG, DEFAULT_DB_LOC, log
from icenine.core.metadata import AccountMeta


class ExportCSV(object):
    """ Export things to a CSV file """

    def __init__(self, filename):

        # Create directories if they don't exist
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename), mode=0o750, exist_ok=True)

        self.filename = filename

    def exportAliases(self):
        """ Export Aliases to a CSV file """

        log.debug("Creating alias CSV")

        # Get aliases from DB
        with AccountMeta() as meta:

            aliases = meta.getAliases()

        log.debug("Saving alias CSV")

        # Open file for writing
        with open(self.filename, "w") as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)

            for alias in aliases:

                writer.writerow(alias)

        log.debug("Alias CSV saved!")

    def importAliases(self):
        """ Import aliases from a CSV """

        log.debug("Opening alias CSV for import")

        # Open CSV
        with open(self.filename, "r") as csvfile:
            reader = csv.reader(csvfile)

            # Open DB
            with AccountMeta() as meta:

                for row in reader:

                    # Add the row to the DB
                    meta.addAlias(row[1], row[0])