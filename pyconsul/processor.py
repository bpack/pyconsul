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

    def __init__(self, config):
        self.config = config

        self._setup_client(config)

    def _setup_client(self, config):
        self.client = ConsulClient(config)

    def _build_list(self):
        records = []
        for path in self.config.paths:
            records.extend(self._process_path(path))

        return records

    def _process_path(self, path):
        records = []
        if path.strip().endswith('/'):
            path = path.strip()[:-1]

        for root, dirs, files in os.walk(path):

            for name in files:
                filepath = os.path.join(root, name)
                key = filepath.replace(path, '')

                if key.startswith('/'):
                    key = key[1:]

                logger.debug(f"Adding key = {key}, path = {filepath}")
                records.append(PyconsulRecord(key, filepath))

        return records

    def _add_value(self, record):
        with open(record.path, 'r') as f:
            record.contents = f.read()

    def mirror(self):
        all_records = self._build_list()

        blocks = divide_list(all_records, 64)

        if len(all_records) > 64:
            logger.info(f"Key set of {len(all_records)} records will be processed in 64 key blocks.")

        for block in blocks:
            logger.debug(f"Processing block with size: {str(len(block))}")
            for record in block:
                self._add_value(record)

            try:
                self.client.add_records(block)
            except:
                logger.error("Error uploading keys. Exiting ...")
                sys.exit(1)

