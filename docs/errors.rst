Error Handling
--------------

When an API request fails, the client raises :class:`quadriga.exceptions.RequestError`,
a light wrapper around the HTTP response returned from QuadrigaCX.

Here is an example on how client exceptions can be caught and handled:

.. code-block:: python

    from quadriga import QuadrigaClient
    from quadriga.exceptions import RequestError

    client = QuadrigaClient(
        api_key='api_key',
        api_secret='api_secret',
        client_id='client_id',
    )
    try:
        client.get_balance()  # Fails due to invalid credentials
    except RequestError as exc:
        print(exc)
        print(exc.url)
        print(exc.body)
        print(exc.headers)
        print(exc.http_code)
        print(exc.error_code)


Exceptions
==========

Below are all exceptions raised by the **quadriga** client.

.. automodule:: quadriga.exceptions
    :members:
