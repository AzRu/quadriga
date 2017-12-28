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

    :param api_key: The QuadrigaCX API key.
    :type api_key: str | unicode
    :param api_secret: The QuadrigaCX API secret.
    :type api_secret: str | unicode
    :param client_id: The QuadrigaCX client ID (the number used for login).
    :type client_id: int | str | unicode
    :param timeout: The number of seconds to wait for QuadrigaCX to respond.
    :type timeout: int | float
    :param session: Custom requests.Session object to send HTTP requests with.
        If not set, ``requests.Session()`` is used by default.
    :type session: requests.Session
    :param logger: Logger to record debug messages with. If not set,
        ``logging.getLogger('quadriga')`` is used by default.
    :type logger: logging.Logger

    :cvar version: The client version number.
    :vartype version: str | unicode
    :cvar url: The QuadrigaCX API endpoint.
    :vartype url: str | unicode
    :cvar order_books: The order books supported by the client.
    :vartype order_books: [str | unicode]
    :cvar major_currencies: The major currencies supported by the client.
    :vartype major_currencies: dict

    .. note::
        Parameters **api_key**, **api_secret** and **client_id** are optional
        for public API. See the documentation_ for details.

    .. _REST API v2: https://www.quadrigacx.com/api_info
    .. _documentation: https://quadriga.readthedocs.io/en/latest/public.html

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

        :param message: The message to log.
        :type message: str | unicode
        """
        self._logger.debug(message)

    def _validate_order_book(self, book):
        """Check if the given order book is valid.

        :param book: The name of the order book.
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

        :param currency: The 3 letter code of the major currency in lowercase.
        :type currency: str | unicode
        :raise InvalidCurrencyError: If an invalid major currency is given.
        """
        if currency not in self.major_currencies:
            raise InvalidCurrencyError(
                'Invalid major currency \'{}\'. Choose from {}.'
                .format(currency, tuple(self.major_currencies))
            )

    def book(self, name):
        """Return an instance of :class:`quadriga.book.OrderBook`, an order
        book API wrapper object.

        :param name: The name of the order book.
        :param name: str | unicode
        :return: The order book wrapper object.
        :rtype: quadriga.book.OrderBook
        :raise InvalidOrderBookError: If an invalid order book is given.

        **Example**:

        .. code-block:: python

            >>> from quadriga import QuadrigaClient
            >>>
            >>> client = QuadrigaClient()
            >>>
            >>> client.book('eth_cad').get_ticker()
            >>> client.book('btc_cad').get_ticker()
        """
        self._validate_order_book(name)
        return OrderBook(name, self._rest_client, self._logger)

    def get_balance(self):
        """Return the user's account balance.

        :return: The user's account balance.
        :rtype: dict
        """
        self._log("get account balance")
        return self._rest_client.post(endpoint='/balance')

    def lookup_order(self, order_id):
        """Look up one or more orders by ID (64 hexadecmial characters).

        :param order_id: The order ID, or a list of order IDs.
        :type order_id: str | unicode | list
        :return: The order details.
        :rtype: [dict]
        """
        self._log('look up order(s) {}'.format(order_id))
        return self._rest_client.post(
            endpoint='/lookup_order',
            payload={'id': order_id}
        )

    def cancel_order(self, order_id):
        """Cancel an open order by ID (64 hexadecmial characters).

        :param order_id: The order ID.
        :type order_id: str | unicode
        :return: True if the order has been cancelled successfully.
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

        :param currency: The 3 letter code of the major currency in lowercase
            (e.g. "btc", "eth", "ltc").
        :type currency: str | unicode
        :return: The deposit address.
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

        :param currency: The 3 letter code of the major currency in lowercase
            (e.g. "btc", "eth", "ltc").
        :type currency: str | unicode
        :param amount: The withdrawal amount.
        :type amount: int | float | str | unicode | decimal.Decimal
        :param address: The wallet address.
        :type address: str | unicode

        .. warning::
            Specifying an incorrect major currency and/or wallet address could
            result in permanent loss of your coins. Please be careful when you
            use this method!
        """
        self._validate_currency(currency)
        self._log('withdraw {} {} to {}'.format(amount, currency, address))
        coin_name = self.major_currencies[currency]
        return self._rest_client.post(
            endpoint='/{}_withdrawal'.format(coin_name)
        )
