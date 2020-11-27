import argparse
import logging
import os
import sys
from .config import PyconsulConfig
from .processor import PyconsulProcessor

def parse_args(argv):
    parser = argparse.ArgumentParser()
 
    parser.add_argument('-d', '--dryrun', action='store_true')
    parser.add_argument('-m', '--mountpoint')
    parser.add_argument('-p', '--paths', default='.')
    parser.add_argument('-s', '--no-ssl-verify', action='store_true')
    parser.add_argument('-t', '--token', default=os.environ.get('CONSUL_TOKEN'))
    parser.add_argument('-u', '--url', default=os.environ.get('CONSUL_URL'))
    parser.add_argument('-v', '--verbose', action='count', default=0)

    print("In parse_args()", argv[1:])
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

