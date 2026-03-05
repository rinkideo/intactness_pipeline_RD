"""Set up basic running parameters

Note: See configparser https://docs.python.org/3/library/configparser.html
"""

import logging
from configparser import ConfigParser, ExtendedInterpolation

# pylint: disable=C0103
# Invalid constant name
logger = logging.getLogger('pipe')


def configs(filename):
    """Parse configurations
    """
    logger.info('Checking parameters')

    cfg = ConfigParser(interpolation=ExtendedInterpolation())
    cfg.read(filename)

    if cfg['Main']['email'] == '':
        print('Please specify your email address')
        exit(1)

    return cfg
