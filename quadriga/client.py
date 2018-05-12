from __future__ import absolute_import, unicode_literals, division

import logging

import requests

from quadriga.exceptions import (
    InvalidCurrencyError,
    InvalidOrderBookError
)
from quadriga.book import OrderBook
from quadriga.rest import RestClient
from quadriga.version import __version__


class QuadrigaClient(object):
    """Python client for QuadrigaCX's `REST API v2`_.

    :param api_key: QuadrigaCX API key.
    :type api_key: str | unicode
    :param api_secret: QuadrigaCX API secret.
    :type api_secret: str | unicode
    :param client_id: QuadrigaCX client ID (number used for user login).
    :type client_id: str | unicode | int
    :param timeout: Number of seconds to wait for QuadrigaCX to respond to an
        API request.
    :type timeout: int | float
    :param session: User-defined requests.Session object. If not set,
        ``requests.Session()`` is used by default.
    :type session: requests.Session
    :param logger: Logger to record debug messages with. If not set,
        ``logging.getLogger('quadriga')`` is used by default.
    :type logger: logging.Logger

    :cvar version: Client version.
    :vartype version: str | unicode
    :cvar url: QuadrigaCX API base URL.
    :vartype url: str | unicode
    :cvar order_books: Order books supported.
    :vartype order_books: [str | unicode]
    :cvar major_currencies: Major currencies supported.
    :vartype major_currencies: dict

    .. note::
        Parameters **api_key**, **api_secret** and **client_id** are optional.
        See :doc:`public` for details.

    .. _REST API v2: https://www.quadrigacx.com/api_info
    """

    version = __version__

    url = 'https://api.quadrigacx.com/v2'

    order_books = {
        'bch_btc',
        'bch_cad',
        'btc_cad',
        'btc_usd',
        'btg_btc',
        'btg_cad',
        'eth_btc',
        'eth_cad',
        'ltc_btc',
        'ltc_cad',
    }

    major_currencies = {
        'bch': 'bitcoincash',
        'btc': 'bitcoin',
        'btg': 'bitcoingold',
        'eth': 'ether',
        'ltc': 'litecoin'
    }

    def __init__(self,
                 api_key=None,
                 api_secret=None,
                 client_id=None,
                 timeout=None,
                 session=None,
                 logger=None):
        self._rest_client = RestClient(
            url=self.url,
            api_key=api_key,
            api_secret=api_secret,
            client_id=client_id,
            timeout=timeout,
            session=session or requests.Session()
        )
        self._logger = logger or logging.getLogger('quadriga')

    def __repr__(self):
        return '<QuadrigaClient v{}>'.format(__version__)

    def _log(self, message):
        """Log a debug message.

        :param message: Debug message.
        :type message: str | unicode
        """
        self._logger.debug(message)

    def _validate_order_book(self, book):
        """Check if the given order book is valid.

        :param book: Order book name.
        :type book: str | unicode
        :raise InvalidOrderBookError: If an invalid order book is given.
        """
        if book not in self.order_books:
            raise InvalidOrderBookError(
                'Invalid order book \'{}\'. Choose from {}.'
                .format(book, tuple(self.order_books))
            )

    def _validate_currency(self, currency):
        """Check if the given order book is valid.

        :param currency: Major currency name in lowercase.
        :type currency: str | unicode
        :raise InvalidCurrencyError: If an invalid major currency is given.
        """
        if currency not in self.major_currencies:
            raise InvalidCurrencyError(
                'Invalid major currency \'{}\'. Choose from {}.'
                .format(currency, tuple(self.major_currencies))
            )

    def book(self, name):
        """Return an API wrapper for the given order book.

        :param name: Order book name (e.g. "btc_cad").
        :type name: str | unicode
        :return: Order book API wrapper.
        :rtype: quadriga.book.OrderBook
        :raise InvalidOrderBookError: If an invalid order book is given.

        **Example**:

        .. doctest::

            >>> from quadriga import QuadrigaClient
            >>>
            >>> client = QuadrigaClient()
            >>>
            >>> eth = client.book('eth_cad').get_ticker()  # doctest:+ELLIPSIS
            >>> btc = client.book('btc_cad').get_ticker()  # doctest:+ELLIPSIS
        """
        self._validate_order_book(name)
        return OrderBook(name, self._rest_client, self._logger)

    def get_balance(self):
        """Return user's account balance.

        :return: User's account balance.
        :rtype: dict
        """
        self._log("get account balance")
        return self._rest_client.post(endpoint='/balance')

    def lookup_order(self, order_id):
        """Look up one or more orders by ID (64 hexadecmial characters).

        :param order_id: Order ID or list of order IDs.
        :type order_id: str | unicode | [str | unicode]
        :return: Order details.
        :rtype: [dict]
        """
        self._log('look up order(s) {}'.format(order_id))
        return self._rest_client.post(
            endpoint='/lookup_order',
            payload={'id': order_id}
        )

    def cancel_order(self, order_id):
        """Cancel an open order by ID (64 hexadecmial characters).

        :param order_id: Order ID.
        :type order_id: str | unicode
        :return: True if the order was cancelled successfully.
        :rtype: bool
        """
        self._log('cancel order {}'.format(order_id))
        result = self._rest_client.post(
            endpoint='/cancel_order',
            payload={'id': order_id}
        )
        return result == 'true'

    def get_deposit_address(self, currency):
        """Return the deposit address for the given major currency.

        :param currency: Major currency name in lowercase (e.g. "btc", "eth").
        :type currency: str | unicode
        :return: Deposit address.
        :rtype: str | unicode
        """
        self._validate_currency(currency)
        self._log('get deposit address for {}'.format(currency))
        coin_name = self.major_currencies[currency]
        return self._rest_client.post(
            endpoint='/{}_deposit_address'.format(coin_name)
        )

    def withdraw(self, currency, amount, address):
        """Withdraw a major currency from QuadrigaCX to the given wallet.

        :param currency: Major currency name in lowercase (e.g. "btc", "eth").
        :type currency: str | unicode
        :param amount: Withdrawal amount.
        :type amount: int | float | str | unicode | decimal.Decimal
        :param address: Wallet address.
        :type address: str | unicode

        .. warning::
            Specifying incorrect major currency or wallet address could result
            in permanent loss of your coins. Please be careful when using this
            method!
        """
        self._validate_currency(currency)
        self._log('withdraw {} {} to {}'.format(amount, currency, address))
        coin_name = self.major_currencies[currency]
        return self._rest_client.post(
            endpoint='/{}_withdrawal'.format(coin_name)
        )
