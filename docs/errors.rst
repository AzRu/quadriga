Error Handling
--------------

When an API request fails, :class:`quadriga.exceptions.RequestError` is raised.
The exception object contains the error message, error code and HTTP request
response details.

**Example:**

.. testcode::

    from quadriga import QuadrigaClient
    from quadriga.exceptions import RequestError

    client = QuadrigaClient(
        api_key='api_key',
        api_secret='api_secret',
        client_id='client_id',
    )
    try:
        client.get_balance()    # Fails due to invalid credentials
    except RequestError as err:
        err.message             # Error message
        err.url                 # API endpoint
        err.body                # Raw response body from QuadrigaCX
        err.headers             # Response headers
        err.http_code           # HTTP status code
        err.error_code          # Error code from QuadrigaCX
        err.response            # requests.Response object
        err.response.request    # requests.Request object


Exceptions
==========

Below are exceptions raised by quadriga client.

.. automodule:: quadriga.exceptions
    :members:
