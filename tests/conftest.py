from __future__ import absolute_import, unicode_literals, division

import time
import mock
import pytest

from quadriga import QuadrigaClient


api_key = 'test_api_key'
api_secret = 'test_api_secret'
client_id = 'test_client_id'
nonce = 14914812560000
timeout = 123456789
signature = '6d39de3ac91dd6189993059be99068d2290d90207ab4aeca26dcbbccfef7b57d'


@pytest.fixture(autouse=True)
def patch_time(monkeypatch):
    mock_time = mock.MagicMock()
    mock_time.return_value = nonce // 10000
    monkeypatch.setattr(time, 'time', mock_time)


@pytest.fixture(autouse=True)
def logger():
    mock_logger = mock.MagicMock()

    def debug_called_with(message):
        mock_logger.debug.assert_called_with(message)

    mock_logger.debug_called_with = debug_called_with
    return mock_logger


# noinspection PyShadowingNames
@pytest.fixture(autouse=True)
def response():
    response = mock.MagicMock()
    response.status_code = 200
    return response


# noinspection PyShadowingNames
@pytest.fixture(autouse=True)
def session(response):
    session = mock.MagicMock()
    session.get.return_value = response
    session.post.return_value = response

    def get_called_with(endpoint, params=None):
        session.get.assert_called_with(
            url=QuadrigaClient.url + endpoint,
            params=params,
            timeout=timeout
        )
    session.get_called_with = get_called_with

    def post_called_with(endpoint, payload=None):
        payload = payload or {}
        payload.update({
            'key': api_key,
            'nonce': nonce,
            'signature': signature
        })
        session.post.assert_called_with(
            url=QuadrigaClient.url + endpoint,
            json=payload,
            timeout=timeout
        )
    session.post_called_with = post_called_with
    return session


# noinspection PyShadowingNames
@pytest.fixture(autouse=True)
def client(session, logger):
    return QuadrigaClient(
        api_key=api_key,
        api_secret=api_secret,
        client_id=client_id,
        timeout=timeout,
        session=session,
        logger=logger
    )
