"""
Services logic.
"""
import txtorcon

import apaf
from apaf.config import config


def start_services(torconfig):
    """
    For each service active in the configuration xand avaible in the
    `services/` directory, launch it.

    :param torconfig: an instance of txtorcon.TorConfig representing the
                      configuration file.
    """

