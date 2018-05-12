HTTP Session
------------

You can use your own ``requests.Session`` objects for sending HTTP requests to
QuadrigaCX. For example, let's say you want:

* Automatic retries
* Additional request header called ``x-my-header``

You can initialize and inject your session as follows:

.. testcode::

    from requests.adapters import HTTPAdapter
    from requests import Session

    from quadriga import QuadrigaClient

    session = Session()

    # Enable automatic retries.
    adapter = HTTPAdapter(max_retries=5)
    session.mount('https://', adapter)

    # Add your request header.
    session.headers.update({'x-my-header': 'true'})

    # Inject the session during client initialization.
    client = QuadrigaClient(session=session)

    client.book('eth_cad').get_ticker()
    client.book('eth_cad').get_public_orders()

For more information on how to configure a ``requests.Session`` object, refer
to `requests documentation`_.

.. _requests documentation: http://docs.python-requests.org/en/master/user/advanced/#session-objects
