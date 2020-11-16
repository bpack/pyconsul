import logging
import os
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
            records.append(self._process_path(path))

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

                logger.debug(f"Adding key = {key}, f = {filepath}")
                records.append(PyconsulRecord(key, filepath))

        return records

    def _add_value(self, record):
        with open(record.path, 'r') as f:
            record.contents = f.read()

    def mirror(self):
        all_records = self._build_list()

        for block in divide_list(all_records, 64):
            for records in block:
                for record in records:
                    self._add_value(record)

                self.client.add_records(records)

