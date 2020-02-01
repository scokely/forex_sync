""" Command line tools to set base currency and update FOREX rates. """

import sys
from argparse import Action
from datetime import datetime


# local modules
from .db import DbClient
from .request import fetch_forex_for
from forex_sync.config import get_config


class SetBaseCurrency(Action):
    """docs"""

    def __init__(self, option_strings, dest, args=None, **kwargs):
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, value, option_string=None):

        self.dest = value

        try:  # recall: DbClient.update(filter, document, upsert=True)
            with DbClient('exchange_rates', 'config') as db:
                db.update(
                        {'base_currency': {'$ne': None}},
                        {'base_currency': value})
                print(f'Success. Base currency set to {value}')

        except Exception as e:
            print(e)

        finally:
            sys.exit(0)


class UpdateForexRates(Action):
    """ docs  """

    def __init__(self, option_strings, dest, args=None, **kwargs):
        super().__init(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, value, option_string=None):

        setattr(namespace, self.dest, True)

        try:
            config = get_config()
            base_currency = config['base_currency']
            print(('Retrieving Forex rates . . . '
                   f' [base currency: {base_currency}]'))
            response = fetch_forex_for(base_currency)
            response['date'] = datetime.utcnow()

            with DbClient('exchange_rates', 'rates') as db:
                db.update(
                        {'base': base_currency},
                        response)

        except Exception as e:
            print(e)

        finally:
            sys.exit(0)
