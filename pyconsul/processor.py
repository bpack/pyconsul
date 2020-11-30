import logging
import os
import sys
from .consul_client import ConsulClient
from .record import PyconsulRecord

def divide_list(full_list, n):
    ' Yield successive blocks of a list into n-sized pieces '
    for i in range(0, len(full_list), n):
        yield full_list[i:i + n]

logger = logging.getLogger('pyconsul')

class PyconsulProcessor:
    ' Encapsulates the processing of paths to Consul key-values '

    def __init__(self, config):
        self.config = config

        self._setup_client(config)

    def _setup_client(self, config):
        ' Creates the Consul Client given the system config '
        self.client = ConsulClient(config)

    def _build_list(self):
        ' Builds the list of key-value pairs for the provided paths'
        records = []
        for path in self.config.paths:
            records.extend(self._process_path(path))

        return records

    def _process_path(self, path):
        ' Inspects an individual path for all files to use as key-value pairs '
        records = []
        if path.strip().endswith('/'):
            path = path.strip()[:-1]

        for root, _, files in os.walk(path):

            for name in files:
                filepath = os.path.join(root, name)
                key = filepath.replace(path, '')

                if key.startswith('/'):
                    key = key[1:]

                logger.debug("Adding key = %s, path = %s", key, filepath)
                records.append(PyconsulRecord(key, filepath))

        return records

    def _add_value(self, record):
        ' Enriches a record with the file contents '
        with open(record.path, 'r') as f:
            record.contents = f.read()

    def mirror(self):
        ' Mirrors all the paths on the file system using the consul client '
        all_records = self._build_list()

        blocks = divide_list(all_records, 64)

        if len(all_records) > 64:
            logger.info("Key set of %s records will be processed in 64 key blocks.",
                    len(all_records))

        for block in blocks:
            logger.debug("Processing block with size: %s", str(len(block)))
            for record in block:
                self._add_value(record)

            try:
                self.client.add_records(block)
            except:
                logger.error("Error uploading keys. Exiting ...")
                sys.exit(1)
