import base64
import json
import logging
import requests

logger = logging.getLogger('pyconsul')

class ConsulClient:
    ' Encapsulates the use of the Consul txn API for key-value uploads '

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
        ' Converts a record to a key-value API object '
        kv_root = ""
        if self.mount_point:
            kv_root = self.mount_point

        key = "{}/{}".format(kv_root, record.key)

        if key.startswith('/'):
            key = key[1:]

        value = "{}".format(base64.b64encode(record.contents.encode("utf-8")).decode("utf-8"))
        kv = {
            "KV": {
                "Verb": "set",
                "Key": key,
                "Value": value
            }
        }

        return kv

    def add_records(self, records):
        ' Adds the given records to Consul using the txn API '
        kvs = []
        for record in records:
            kvs.append(self.to_kv(record))

        if self.dryrun:
            logger.info("DRY RUN - payload is \n%s with headers \n%s",
                    json.dumps(kvs, indent=2), self.headers)

            if not self.verify:
                logger.info("DRY RUN - SSL Validation disabled.")
        else:
            logger.info("Mirroring %s keys to %s", len(kvs), self.url)

            response = requests.request('PUT', self.url,
                    data=json.dumps(kvs), headers=self.headers, verify=self.verify)

            if response.status_code == 200:
                logger.debug(f"Request upload succeeded {response.content}")

            else:
                status = response.status_code
                logger.error("Request upload failed. HTTP response code %s", status)
                logger.error("Response body: %s", response.content)
                logger.error("Headers: %s", response.headers)

                raise RuntimeError(f"Consul PUT request failed with status code {status}")
