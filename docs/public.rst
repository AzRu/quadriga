Public API
----------

If only public API is required, you do not need to provide parameters
**api_key**, **api_secret** and **client_id** when initializing
:class:`quadriga.client.QuadrigaClient`.

**Example:**

.. testcode::

    from quadriga import QuadrigaClient
    from quadriga.exceptions import RequestError

    # Initialize the client without credentials.
    client = QuadrigaClient()

    # Private (user) API calls fail.
    try:
        client.book('btc_cad').get_user_orders()
    except RequestError as err:
        assert err.error_code == 101
    try:
        client.book('btc_cad').get_user_trades()
    except RequestError as err:
        assert err.error_code == 101

    # Public API calls still go through.
    orders = client.book('btc_cad').get_public_orders()
    trades = client.book('btc_cad').get_public_trades()
