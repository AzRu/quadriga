from __future__ import absolute_import, unicode_literals, division


class OrderBook(object):
    """Represents an order book on QuadrigaCX.

    .. note::
        This class is not meant to be instantiated directly. Use
        :func:`quadriga.client.QuadrigaClient.book` instead.
    """

    def __init__(self, name, rest_client, logger):
        self.name = name
        self.major, self.minor = name.split('_')
        self._rest_client = rest_client
        self._logger = logger

    def __repr__(self):
        return '<OrderBook \'{}\'>'.format(self.name)

    def _log(self, message):
        """Log a debug message.

        :param message: The message to log.
        :type message: str | unicode
        """
        self._logger.debug("{}: {}".format(self.name, message))

    def get_ticker(self):
        """Return the latest ticker information.

        :return: The latest ticker information.
        :rtype: dict
        """
        self._log('get ticker')
        return self._rest_client.get(
            endpoint='/ticker',
            params={'book': self.name}
        )

    def get_public_orders(self, group=False):
        """Return public orders currently open.

        :param group: If set to True (default: False), orders with the same
            price are grouped.
        :type group: bool
        :return: Public orders currently open.
        :rtype: dict
        """
        self._log('get public orders')
        return self._rest_client.get(
            endpoint='/order_book',
            params={'book': self.name, 'group': int(group)}
        )

    def get_public_trades(self, time_frame='hour'):
        """Return public trades (transactions) completed recently.

        :param time_frame: The time frame. Allowed values are "minute" for
            trades in the last minute, or "hour" for trades in the last hour
            (default: "hour").
        :type time_frame: str | unicode
        :return: Public trades completed recently.
        :rtype: [dict]
        """
        self._log('get public trades')
        return self._rest_client.get(
            endpoint='/transactions',
            params={'book': self.name, 'time': time_frame}
        )

    def get_user_orders(self):
        """Return user's orders currently open.

        :return: The list of user's open orders.
        :rtype: [dict]
        """
        self._log('get user orders')
        return self._rest_client.post(
            endpoint='/open_orders',
            payload={'book': self.name}
        )

    def get_user_trades(self, limit=0, offset=0, sort='desc'):
        """Return the user's trade (transaction) history.

        :param limit: The maximum number of trades to return. If set to 0 or
            lower, all trades are returned (default: 0).
        :type limit: int
        :param offset: The number of trades to skip.
        :type offset: int
        :param sort: The method used to sort the results by date and time.
            Allowed values are "desc" for descending order and "asc" for
            ascending order (default: "desc").
        :type sort: str | unicode
        :return: The user's trade history.
        :rtype: [dict]
        """
        self._log('get user trades')
        res = self._rest_client.post(
            endpoint='/user_transactions',
            payload={
                'book': self.name,
                'limit': limit,
                'offset': offset,
                'sort': sort
            }
        )
        # TODO Workaround for the broken limit param in QuadrigaCX API
        return res[:limit] if len(res) > limit > 0 else res

    def buy_market_order(self, amount):
        """Place a buy order at market price.

        :param amount: The amount of major currency to buy at market price.
        :type amount: int | float | str | unicode | decimal.Decimal
        :return: The order details.
        :rtype: dict
        """
        amount = str(amount)
        self._log("buy {} {} at market price".format(amount, self.major))
        return self._rest_client.post(
            endpoint='/buy',
            payload={
                'book': self.name,
                'amount': amount
            }
        )

    def buy_limit_order(self, amount, price):
        """Place a buy order at the given limit price.

        :param amount: The amount of major currency to buy at the limit price.
        :type amount: int | float | str | unicode | decimal.Decimal
        :param price: The limit price.
        :type price: int | float | str | unicode | decimal.Decimal
        :return: The order details.
        :rtype: dict
        """
        amount = str(amount)
        price = str(price)
        self._log("buy {} {} at limit price of {} {}".format(
            amount, self.major, price, self.minor
        ))
        return self._rest_client.post(
            endpoint='/buy',
            payload={
                'book': self.name,
                'amount': amount,
                'price': price
            }
        )

    def sell_market_order(self, amount):
        """Place a sell order at market price.

        :param amount: The amount of major currency to sell at market price.
        :type amount: int | float | str | unicode | decimal.Decimal
        :return: The order details.
        :rtype: dict
        """
        amount = str(amount)
        self._log("sell {} {} at market price".format(amount, self.major))
        return self._rest_client.post(
            endpoint='/sell',
            payload={
                'book': self.name,
                'amount': amount
            }
        )

    def sell_limit_order(self, amount, price):
        """Place a sell order at the given limit price.

        :param amount: The amount of major currency to sell at the limit price.
        :type amount: int | float | str | unicode | decimal.Decimal
        :param price: The limit price.
        :type price: int | float | str | unicode | decimal.Decimal
        :return: The order details.
        :rtype: dict
        """
        amount = str(amount)
        price = str(price)
        self._log("sell {} {} at limit price of {} {}".format(
            amount, self.major, price, self.minor
        ))
        return self._rest_client.post(
            endpoint='/sell',
            payload={
                'book': self.name,
                'amount': amount,
                'price': price
            }
        )
