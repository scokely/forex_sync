""" Custom exception to handle database queries without configuration. """

from forex_sync.core import DbClient
from .config_error import ConfigError


def get_config():
    """ Queries DbClient for existing configuations.

    The function initializes DbClient to connect to the exchange_rate database
    and identifies existing configurations using the 'config' collection.

    Within DbClient context, calling the find_one() method without arguments
    returns the first item in the collection. Here, if the exchange_rate
    database does not have an existing base currency configuration,
    ConfigError() is raised.

    Setting the base currency with option '--setbasecurrency' updates the
    exchange_rate database config collection.
    """

    config = None

    with DbClient('exchange_rates', 'config') as db:
        config = db.find_one()

    if config is None:
        error_message = (
            """ It was not possible to retrieve your base currency.'\n'
                If you haven't already, use option '--setbasecurrency''\n'
                and try again.""")
        raise ConfigError(error_message)

    return config
