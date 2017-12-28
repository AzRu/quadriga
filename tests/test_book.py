from __future__ import absolute_import, unicode_literals, division


def test_get_ticker(client, session, logger):
    client.book('btc_cad').get_ticker()
    session.get_called_with(
        endpoint='/ticker',
        params={'book': 'btc_cad'}
    )
    logger.debug_called_with('btc_cad: get ticker')


def test_get_public_orders_grouped(client, session, logger):
    client.book('btc_cad').get_public_orders(group=True)
    session.get_called_with(
        endpoint='/order_book',
        params={'book': 'btc_cad', 'group': 1}
    )
    logger.debug_called_with('btc_cad: get public orders')


def test_get_public_orders_not_grouped(client, session, logger):
    client.book('btc_cad').get_public_orders(group=False)
    session.get_called_with(
        endpoint='/order_book',
        params={'book': 'btc_cad', 'group': 0}
    )
    logger.debug_called_with('btc_cad: get public orders')


def test_get_public_trades_by_hour(client, session, logger):
    client.book('btc_cad').get_public_trades()
    session.get_called_with(
        endpoint='/transactions',
        params={'book': 'btc_cad', 'time': 'hour'}
    )
    logger.debug_called_with('btc_cad: get public trades')


def test_get_public_trades_by_minute(client, session, logger):
    client.book('btc_cad').get_public_trades(time_frame='minute')
    session.get_called_with(
        endpoint='/transactions',
        params={'book': 'btc_cad', 'time': 'minute'}
    )
    logger.debug_called_with('btc_cad: get public trades')


def test_get_user_orders(client, session, logger):
    client.book('btc_cad').get_user_orders()
    session.post_called_with(
        endpoint='/open_orders',
        payload={'book': 'btc_cad'}
    )
    logger.debug_called_with('btc_cad: get user orders')


def test_get_user_trades_no_params(client, session, logger, response):
    response.json.return_value = []
    book = client.book('btc_cad')
    assert [] == book.get_user_trades()
    session.post_called_with(
        endpoint='/user_transactions',
        payload={
            'book': 'btc_cad',
            'limit': 0,
            'offset': 0,
            'sort': 'desc'
        }
    )
    logger.debug_called_with('btc_cad: get user trades')


def test_get_user_trades_with_params(client, session, logger, response):
    response.json.return_value = [1, 2]
    book = client.book('btc_cad')
    assert [1] == book.get_user_trades(limit=1, offset=1, sort='asc')
    session.post_called_with(
        endpoint='/user_transactions',
        payload={
            'book': 'btc_cad',
            'limit': 1,
            'offset': 1,
            'sort': 'asc'
        }
    )
    logger.debug_called_with('btc_cad: get user trades')


def test_buy_market_order(client, session, logger):
    book = client.book('btc_cad')
    book.buy_market_order(10)
    session.post_called_with(
        endpoint='/buy',
        payload={
            'book': 'btc_cad',
            'amount': '10'
        }
    )
    logger.debug_called_with("btc_cad: buy 10 btc at market price")


def test_buy_limit_order(client, session, logger):
    book = client.book('btc_cad')
    book.buy_limit_order(10, 5)
    session.post_called_with(
        endpoint='/buy',
        payload={
            'book': 'btc_cad',
            'amount': '10',
            'price': '5'
        }
    )
    logger.debug_called_with("btc_cad: buy 10 btc at limit price of 5 cad")


def test_sell_market_order(client, session, logger):
    book = client.book('btc_cad')
    book.sell_market_order(10)
    session.post_called_with(
        endpoint='/sell',
        payload={
            'book': 'btc_cad',
            'amount': '10'
        }
    )
    logger.debug_called_with("btc_cad: sell 10 btc at market price")


def test_sell_limit_order(client, session, logger):
    book = client.book('btc_cad')
    book.sell_limit_order(10, 5)
    session.post_called_with(
        endpoint='/sell',
        payload={
            'book': 'btc_cad',
            'amount': '10',
            'price': '5'
        }
    )
    logger.debug_called_with("btc_cad: sell 10 btc at limit price of 5 cad")
