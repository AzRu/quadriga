Logging
-------

By default, the client logs API call history using the ``quadriga`` logger at
``logging.DEBUG`` level.

Here is an example showing how the logger can be enabled and customized:

.. code-block:: python

    import logging

    from quadriga import QuadrigaClient

    logger = logging.getLogger('quadriga')

    # Set the logging level
    logger.setLevel(logging.DEBUG)

    # Attach a custom handler
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Initialize and use the client to see the changes
    client = QuadrigaClient(
        api_key='api_key',
        api_secret='api_secret',
        client_id='client_id'
    )
    client.get_balance()
    client.book('eth_cad').get_ticker()
    client.book('eth_cad').get_public_orders()


The logging output from above should look something like this:

.. code-block:: console

    [2017-04-12 23:55:51,954] get account balance
    [2017-04-12 23:55:52,230] eth_cad: get ticker
    [2017-04-12 23:55:53,741] eth_cad: get public orders

In order to see the full request information, turn on logging for requests_:

.. _requests: https://github.com/requests/requests

.. code-block:: python

    import requests
    import logging

    try: # for Python 3
        from http.client import HTTPConnection
    except ImportError:
        from httplib import HTTPConnection
    HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
