from __future__ import absolute_import, unicode_literals, division

import hashlib
import hmac
import time

from quadriga.exceptions import RequestError


class RestClient(object):
    """REST client using HMAC SHA256 authentication.

    :param url: QuadrigaCX URL.
    :type url: str | unicode
    :param api_key: QuadrigaCX API key.
    :type api_key: str | unicode
    :param api_secret: QuadrigaCX API secret.
    :type api_secret: str | unicode
    :param client_id: QuadrigaCX client ID (number used for user login).
    :type client_id: str | unicode | int
    :param timeout: Number of seconds to wait for QuadrigaCX to respond to an
        API request.
    :type timeout: int | float
    :param session: User-defined requests.Session object.
    :type session: requests.Session
    """

    http_success_status_codes = {200, 201, 202}

    def __init__(self, url, api_key, api_secret, client_id, timeout, session):
        self._url = url
        self._api_key = str(api_key)
        self._hmac_key = str(api_secret).encode('utf-8')
        self._client_id = str(client_id)
        self._timeout = timeout
        self._session = session

    def _handle_response(self, resp):
        """Handle the response from QuadrigaCX.

        :param resp: Response from QuadrigaCX.
        :type resp: requests.models.Response
        :return: Response body.
        :rtype: dict
        :raise quadriga.exceptions.RequestError: If HTTP OK was not returned.
        """
        http_code = resp.status_code
        if http_code not in self.http_success_status_codes:
            raise RequestError(
                response=resp,
                message='[HTTP {}] {}'.format(http_code, resp.reason)
            )
        try:
            body = resp.json()
        except ValueError:
            raise RequestError(
                response=resp,
                message='[HTTP {}] response body: {}'.format(
                    http_code,
                    resp.text
                )
            )
        else:
            if 'error' in body:
                error_code = body['error'].get('code', '?')
                raise RequestError(
                    response=resp,
                    message='[HTTP {}][ERR {}] {}'.format(
                        resp.status_code,
                        error_code,
                        body['error'].get('message', 'no error message')
                    ),
                    error_code=error_code
                )
            return body

    def get(self, endpoint, params=None):
        """Send an HTTP GET request to QuadrigaCX.

        :param endpoint: API endpoint.
        :type endpoint: str | unicode
        :param params: URL parameters.
        :type params: dict
        :return: Response body from QuadrigaCX.
        :rtype: dict
        :raise quadriga.exceptions.RequestError: If HTTP OK was not returned.
        """
        response = self._session.get(
            url=self._url + endpoint,
            params=params,
            timeout=self._timeout
        )
        return self._handle_response(response)

    def post(self, endpoint, payload=None):
        """Send an HTTP POST request to QuadrigaCX.

        :param endpoint: API endpoint.
        :type endpoint: str | unicode
        :param payload: Request payload.
        :type payload: dict
        :return: Response body from QuadrigaCX.
        :rtype: dict
        :raise quadriga.exceptions.RequestError: If HTTP OK was not returned.
        """
        nonce = int(time.time() * 10000)
        hmac_msg = str(nonce) + self._client_id + self._api_key
        signature = hmac.new(
            key=self._hmac_key,
            msg=hmac_msg.encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()

        if payload is None:
            payload = {}
        payload['key'] = self._api_key
        payload['nonce'] = nonce
        payload['signature'] = signature

        response = self._session.post(
            url=self._url + endpoint,
            json=payload,
            timeout=self._timeout
        )
        return self._handle_response(response)
