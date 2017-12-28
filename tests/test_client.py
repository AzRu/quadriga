from __future__ import absolute_import, unicode_literals, division

import pytest

from quadriga.exceptions import (
    InvalidCurrencyError,
    InvalidOrderBookError,
    RequestError
)
from quadriga.book import OrderBook
from quadriga.client import QuadrigaClient
from quadriga.version import __version__


def test_quadriga_client(client):
    assert __version__ == client.version
    assert '<QuadrigaClient v{}>'.format(__version__) == repr(client)
    assert 'quadrigacx.com' in client.url
    assert 'btc_cad' in client.order_books
    assert client.major_currencies['btc'] == 'bitcoin'


def test_get_order_book(client):
    book = client.book('btc_cad')
    assert repr(book) == "<OrderBook 'btc_cad'>"
    assert isinstance(book, OrderBook)
    assert book.name == 'btc_cad'
    assert book.major == 'btc'
    assert book.minor == 'cad'

    with pytest.raises(InvalidOrderBookError) as err:
        client.book('invalid')
    assert "Invalid order book 'invalid'" in str(err.value)


def test_get_account_balance(client, session, logger):
    client.get_balance()
    logger.debug_called_with('get account balance')
    session.post_called_with(endpoint='/balance')


def test_lookup_order(client, session, logger):
    client.lookup_order([1, 2, 3])
    logger.debug_called_with('look up order(s) [1, 2, 3]')
    session.post_called_with(
        endpoint='/lookup_order',
        payload={'id': [1, 2, 3]}
    )


def test_cancel_order(client, session, logger):
    client.cancel_order(1)
    logger.debug_called_with('cancel order 1')
    session.post_called_with(
        endpoint='/cancel_order',
        payload={'id': 1}
    )


def test_get_deposit_address(client, session, logger):
    for currency, coin_name in QuadrigaClient.major_currencies.items():
        client.get_deposit_address(currency)
        logger.debug_called_with('get deposit address for {}'.format(currency))
        session.post_called_with(
            endpoint='/{}_deposit_address'.format(coin_name)
        )
    with pytest.raises(InvalidCurrencyError) as err:
        client.get_deposit_address('invalid')
    assert "Invalid major currency 'invalid'" in str(err.value)


def test_withdraw(client, session, logger):
    for currency, coin_name in QuadrigaClient.major_currencies.items():
        client.withdraw(currency, 10, 'foobar')
        logger.debug_called_with('withdraw 10 {} to foobar'.format(currency))
        session.post_called_with(
            endpoint='/{}_withdrawal'.format(coin_name)
        )
    with pytest.raises(InvalidCurrencyError) as err:
        client.withdraw('invalid', 10, 'foobar')
    assert "Invalid major currency 'invalid'" in str(err.value)


def test_request_failure_api_error(response, client):
    response.json.return_value = {'error': {'code': 123, 'message': 'fail'}}
    response.url = 'url'
    response.headers = {'foo': 'bar'}

    with pytest.raises(RequestError) as err:
        client.book('btc_cad').get_ticker()
    assert err.value.url == 'url'
    assert err.value.headers == {'foo': 'bar'}
    assert err.value.http_code == 200
    assert err.value.error_code == 123
    assert str(err.value) == '[HTTP 200][ERR 123] fail'


def test_request_failure_http_error(response, client):
    response.status_code = 400
    response.reason = 'test reason'

    with pytest.raises(RequestError) as err:
        client.book('btc_cad').get_ticker()
    assert err.value.http_code == 400
    assert err.value.error_code is None
    assert str(err.value) == '[HTTP 400] test reason'


def test_request_failure_bad_body(response, client):
    response.text = 'invalid'
    response.json.side_effect = ValueError

    with pytest.raises(RequestError) as err:
        client.book('btc_cad').get_ticker()
    assert err.value.body == 'invalid'
    assert err.value.http_code == 200
    assert err.value.error_code is None
    assert str(err.value) == '[HTTP 200] response body: invalid'
