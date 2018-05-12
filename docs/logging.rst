Logging
-------

By default, quadriga client logs API call history using the ``quadriga`` logger
at ``logging.DEBUG`` level. You can customize this logger to suit your usecase.

**Example:**

.. testcode::

    import logging

    from quadriga import QuadrigaClient

    logger = logging.getLogger('quadriga')

    # Set the logging level.
    logger.setLevel(logging.DEBUG)

    # Attach a handler.
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Inject the logger during client initialization.
    client = QuadrigaClient(logger=logger)

    client.book('eth_cad').get_ticker()
    client.book('eth_cad').get_public_orders()


The logging output from above should look something like this:

.. code-block:: console

    [2017-04-12 23:55:52,230] eth_cad: get ticker
    [2017-04-12 23:55:53,741] eth_cad: get public orders

To see full request details, turn on the logging for requests_ library.

.. _requests: https://github.com/requests/requests

**Example**:

.. code-block:: python

    import requests
    import logging

    try:
        # For Python 3.
        from http.client import HTTPConnection
    except ImportError:
        # For Python 2.
        from httplib import HTTPConnection
    HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
