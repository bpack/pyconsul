import base64
import json
import logging
import requests

logger = logging.getLogger('pyconsul')

class ConsulClient:

    def __init__(self, config):
        self.dryrun = config.dryrun

        self.mount_point = config.mount_point
        if self.mount_point and self.mount_point.strip().endswith('/'):
            self.mount_point = self.mount_point.strip()[:-1]

        self.url = "{}/v1/txn".format(config.url)

        self.verify = not config.skip_ssl

        self.headers = {
            'Content-Type': "application/json",
            'X-Consul-Token': config.token,
            'User-Agent': "github.com/bpack/pyconsul",
            'Accept': "*/*",
            'Cache-Control': "no-cache"
        }

    def to_kv(self, record):
        kv_root = ""
        if self.mount_point:
            kv_root = self.mount_point

        key = "{}/{}".format(kv_root, record.key)

        if key.startswith('/'):
            key = key[1:]

        kv = {
            "KV": {
                "Verb": "set",
                "Key": key,
                "Value": "{}".format(base64.b64encode(record.contents.encode("utf-8")).decode("utf-8"))
            }
        }

        return kv

    def add_records(self, records):
        kvs = []
        for record in records:
            kvs.append(self.to_kv(record))

        if self.dryrun:
            logger.info("DRY RUN - payload is \n{} with headers \n{}".format(json.dumps(kvs, indent=2), self.headers))
            if not self.verify:
                logger.info("DRY RUN - SSL Validation disabled.")
        else:
            logger.info("Mirroring {} keys to {}".format(len(kvs), self.url))

            response = requests.request('PUT', self.url, data=json.dumps(kvs), headers=self.headers, verify=self.verify)

            if response.status_code == 200:
                logger.debug(f"Request upload succeeded {response.content}")

            else:
                logger.error(f"Request upload failed. HTTP response code {response.status_code}")
                logger.error(f"Response body: {response.content}")
                logger.error(f"Headers: {response.headers}")

                raise RuntimeError(f"Consul PUT request failed with status code {response.status_code}")

