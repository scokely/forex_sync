# work in progress. have only implemented basic API functionality so far.

"""This module extracts forex data from the fixer.io API, and returns
exhange rates for 170 currencies. By default, fixer.io sets the base
(reference) currency to EUR. Changing the base currency requires a $10/month
subsrciption.

Create an account with fixer.io to create a free account and download a
private API_KEY.

"""


import requests
from http import HTTPStatus
import json

API_KEY = 'your_api_key_goes_here'


def fetch_forex_for(currency):
    """future docstring"""

    #if you have the free version of fixer.io, comment out '&base={currency}
    base_currency = requests.get(f'http://data.fixer.io/api/latest?access_key={API_KEY}&base={currency}')

    if base_currency.status_code == HTTPStatus.OK:
        conversion_table = json.loads(base_currency.text)
        return conversion_table
    elif base_currency.status_code == HTTPStatus.NOT_FOUND:
        raise ValueError(f'Could not find forex rates for {currency}.')
    elif base_currency.status_code == HTTPStatus.BAD_REQUEST:
        raise ValueError(f'Invalid input: {currency}.')
    else:
        raise Exception('Uh oh! Something went wrong. Unable to get rates.')
