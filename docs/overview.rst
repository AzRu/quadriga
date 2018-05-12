Getting Started
---------------

Here is an example showing how a **quadriga** client can be initialized and used:

.. code-block:: python

    from quadriga import QuadrigaClient

    client = QuadrigaClient(
        api_key='api_key',
        api_secret='api_secret',
        client_id='client_id',
    )
    client.get_balance()                # Get the user's account balance    
    client.lookup_order(['order_id'])   # Look up one or more orders by ID
    client.cancel_order('order_id')     # Cancel an order by ID
 
    client.get_deposit_address('bch')   # Get the funding address for BCH
    client.get_deposit_address('btc')   # Get the funding address for BTC
    client.get_deposit_address('btg')   # Get the funding address for BTG
    client.get_deposit_address('eth')   # Get the funding address for ETH
    client.get_deposit_address('ltc')   # Get the funding address for LTC

    client.withdraw('bch', 1, 'bch_wallet_address')  # Withdraw 1 BCH to wallet
    client.withdraw('btc', 1, 'btc_wallet_address')  # Withdraw 1 BTC to wallet
    client.withdraw('btg', 1, 'btg_wallet_address')  # Withdraw 1 BTG to wallet
    client.withdraw('eth', 1, 'eth_wallet_address')  # Withdraw 1 ETH to wallet
    client.withdraw('ltc', 1, 'ltc_wallet_address')  # Withdraw 1 LTC to wallet

    book = client.book('btc_cad')
    book.get_ticker()                   # Get the latest ticker information
    book.get_user_orders()              # Get user's open orders
    book.get_user_trades()              # Get user's transactions
    book.get_public_orders()            # Get public open orders
    book.get_public_trades()            # Get recent public transactions
    book.buy_market_order(10)           # Buy 10 BTC at market price
    book.buy_limit_order(5, 10)         # Buy 5 BTC at limit price of $10 CAD
    book.sell_market_order(10)          # Sell 10 BTC at market price
    book.sell_limit_order(5, 10)        # Sell 5 BTC at limit price of $10 CAD

See :doc:`specs` for more details.
