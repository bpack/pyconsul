import argparse
import logging
import os
import sys
from .config import PyconsulConfig
from .processor import PyconsulProcessor

def parse_args(argv):
    parser = argparse.ArgumentParser()
 
    parser.add_argument('-d', '--dryrun', action='store_true',
            help='Logs the operations that would be performed instead of executing.')
    parser.add_argument('-m', '--mountpoint',
            help='Defines a top level path in Consul where keys will be written.')
    parser.add_argument('-p', '--paths', default='.', 
            help='The paths on the file system to copy to Consul.')
    parser.add_argument('-s', '--no-ssl-verify', action='store_true',
            help='Skips SSL verification of the Consul URL. Not recommended.')
    parser.add_argument('-t', '--token', default=os.environ.get('CONSUL_TOKEN'),
            help='The authentication token to use with Consul.')
    parser.add_argument('-u', '--url', default=os.environ.get('CONSUL_URL'),
            help='The base Consul URL to use.')
    parser.add_argument('-v', '--verbose', action='count', default=0,
            help='Controls output logging detail. -v for info, -vv for debug.')

    args = parser.parse_args(argv[1:])
    setup_logger(args.verbose)

    config = PyconsulConfig()
    config.dryrun = args.dryrun
    config.mount_point = args.mountpoint
    config.paths = args.paths
    config.skip_ssl = args.no_ssl_verify
    config.token = args.token
    config.url = args.url
    config.verbosity = args.verbose

    logger = logging.getLogger('pyconsul')
    log_config(config, logger)

    return config


def setup_logger(verbosity):
    log_level = {
        0: logging.WARNING,
        1: logging.INFO,
        2: logging.DEBUG
    }.get(verbosity, logging.DEBUG)

    logger = logging.getLogger('pyconsul')
    logger.setLevel(log_level)

    s = logging.StreamHandler()
    s.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    s.setFormatter(formatter)

    logger.addHandler(s)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    config = parse_args(argv)
    processor = PyconsulProcessor(config)
    processor.mirror()


def log_config(config, logger):
    logger.debug('Logging configured')
    logger.debug(str(config))


if __name__ == '__main__':
    main(sys.argv)

