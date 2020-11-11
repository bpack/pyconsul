import logging
import click

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


@click.command()
@click.option('-d', '--directory', multiple=True,
    default=['.'],
    help='''
        Directories to be mirrored to consul.
    ''')
@click.option('-v', '--verbose', count=True)
def main(directory, verbose):
    setup_logger(verbose)
    logger = logging.getLogger('pyconsul')
    config = {
        "paths": directory,
        "verbosity": verbose
    }
    log_config(config, logger)


def log_config(config, logger):
    logger.debug('Logging configured')
    for k, v in config.items():
        logger.debug(f"{k} = {v}")


if __name__ == '__main__':
    main()
