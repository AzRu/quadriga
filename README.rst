Python Client for QuadrigaCX
----------------------------

.. image:: https://travis-ci.org/joowani/quadriga.svg?branch=master
    :target: https://travis-ci.org/joowani/quadriga

.. image:: https://badge.fury.io/py/quadriga.svg
    :target: https://badge.fury.io/py/quadriga
    :alt: Package version

.. image:: https://img.shields.io/badge/python-2.7%2C%203.4%2C%203.5%2C%203.6-blue.svg
    :target: https://github.com/joowani/quadriga
    :alt: Python Versions

.. image:: https://coveralls.io/repos/github/joowani/quadriga/badge.svg?branch=master
    :target: https://coveralls.io/github/joowani/quadriga?branch=master
    :alt: Test Coverage

.. image:: https://img.shields.io/github/issues/joowani/quadriga.svg
    :target: https://github.com/joowani/quadriga/issues
    :alt: Issues Open

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://raw.githubusercontent.com/joowani/quadriga/master/LICENSE
    :alt: MIT License

|

Introduction
============

**Quadriga** is a Python client for Canadian cryptocurrency exchange platform
QuadrigaCX_. It wraps the exchange's `REST API v2`_ using `requests`_ library.

.. _QuadrigaCX: https://www.quadrigacx.com
.. _REST API v2: https://www.quadrigacx.com/api_info
.. _requests: https://github.com/requests/requests


Announcements
=============

* **Quadriga** has been completely overhauled in version `2.0.0`_.
* Please see the releases_ page for details on the latest updates.

.. _2.0.0: https://github.com/joowani/quadriga/releases/tag/2.0.0
.. _releases: https://github.com/joowani/quadriga/releases


Requirements
============

- Python 2.7, 3.4, 3.5 or 3.6.
- QuadrigaCX API secret, API key and client ID (the number used for your login).

Installation
============

To install a stable version from PyPi_:

.. code-block:: bash

    ~$ pip install quadriga

To install the latest version directly from GitHub_:

.. code-block:: bash

    ~$ pip install -e git+git@github.com:joowani/quadriga.git@master#egg=quadriga

You may need to use ``sudo`` depending on your environment.

.. _PyPi: https://pypi.python.org/pypi/quadriga
.. _GitHub: https://github.com/joowani/quadriga


Getting Started
===============

Here are some usage examples:

.. code-block:: python

    from quadriga import QuadrigaClient

    client = QuadrigaClient(
        api_key='api_key',
        api_secret='api_secret',
        client_id='client_id',
    )
    client.get_balance()                # Get the user's account balance
    client.lookup_order(['order_id'])   # Look up one or more orders by ID
    client.cancel_order('order_id')     # Cancel an order by ID

    client.get_deposit_address('bch')   # Get the funding address for BCH
    client.get_deposit_address('btc')   # Get the funding address for BTC
    client.get_deposit_address('btg')   # Get the funding address for BTG
    client.get_deposit_address('eth')   # Get the funding address for ETH
    client.get_deposit_address('ltc')   # Get the funding address for LTC

    client.withdraw('bch', 1, 'bch_wallet_address')  # Withdraw 1 BCH to wallet
    client.withdraw('btc', 1, 'btc_wallet_address')  # Withdraw 1 BTC to wallet
    client.withdraw('btg', 1, 'btg_wallet_address')  # Withdraw 1 BTG to wallet
    client.withdraw('eth', 1, 'eth_wallet_address')  # Withdraw 1 ETH to wallet
    client.withdraw('ltc', 1, 'ltc_wallet_address')  # Withdraw 1 LTC to wallet

    book = client.book('btc_cad')
    book.get_ticker()                   # Get the latest ticker information
    book.get_user_orders()              # Get user's open orders
    book.get_user_trades()              # Get user's trade history
    book.get_public_orders()            # Get public open orders
    book.get_public_trades()            # Get recent public trade history
    book.buy_market_order(10)           # Buy 10 BTC at market price
    book.buy_limit_order(5, 10)         # Buy 5 BTC at limit price of $10 CAD
    book.sell_market_order(10)          # Sell 10 BTC at market price
    book.sell_limit_order(5, 10)        # Sell 5 BTC at limit price of $10 CAD

Check out the `documentation`_ for more details.

.. _documentation: http://quadriga.readthedocs.io/en/latest/index.html


Contributing
============

Please have a look at this page_ before submitting a pull request. Thanks!

.. _page: http://quadriga.readthedocs.io/en/latest/contributing.html


Donation
========

If you found this library useful, feel free to donate.

* **BTC**: 3QG2wSQnXNbGv1y88oHgLXtTabJwxfF8mU
* **ETH**: 0x1f90a2a456420B38Bdb39086C17e61BF5C377dab


Disclaimer
==========

The author(s) of this project is in no way affiliated with QuadrigaCX, and
shall not accept any liability, obligation or responsibility whatsoever for
any cost, loss or damage arising from the use of this client. Please use at
your own risk.
