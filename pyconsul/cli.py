import argparse
import logging
import os
from .config import PyconsulConfig

def parse_args():
    parser = argparse.ArgumentParser()
 
    parser.add_argument('-d', '--dryrun', action='store_true')
    parser.add_argument('-m', '--mountpoint')
    parser.add_argument('-p', '--paths', default='.')
    parser.add_argument('-t', '--token', default=os.environ.get('CONSUL_TOKEN'))
    parser.add_argument('-u', '--url', default=os.environ.get('CONSUL_URL'))
    parser.add_argument('-v', '--verbose', action='count', default=0)

    args = parser.parse_args()
    setup_logger(args.verbose)

    config = PyconsulConfig()
    config.dryrun = args.dryrun
    config.mount_point = args.mountpoint
    config.paths = args.paths
    config.token = args.token
    config.url = args.url
    config.verbosity = args.verbose

    logger = logging.getLogger('pyconsul')
    log_config(config, logger)



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


def main():
    parse_args()

def log_config(config, logger):
    logger.debug('Logging configured')
    for k, v in config._config.items():
        logger.debug(f"{k} = {v}")


if __name__ == '__main__':
    main()
