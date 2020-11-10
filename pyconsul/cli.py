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
@click.option('-v', '--verbose', count=True)
def mirror(verbose):
    setup_logger(verbose)
    logger = logging.getLogger('pyconsul')
    logger.debug('Logging configured')

if __name__ == '__main__':
    mirror()
