Public API
----------

If you need access to public API only, parameters **api_key**, **api_secret**
and **client_id** are optional when initializing :class:`quadriga.QuadrigaClient`:

.. code-block:: python

    # Initialize the client without the credentials
    client = QuadrigaClient()

    # Public API calls still go through
    client.book('btc_cad').get_public_orders()
    client.book('btc_cad').get_public_trades()

    # Private (user-specific) API calls fail
    client.book('btc_cad').get_user_orders()
    client.book('btc_cad').get_user_trades()
