from pylivetrader.api import (
    record, get_open_orders, get_datetime, cancel_order, order_target,
    order_target_percent
)
from iexfinance.stocks import (
    Stock, get_historical_data, get_collections
)

# This example shows how to do a few things in pylivetrader with a portfolio.
def initialize(context):
    # We'll update orders that have been open for more than this many minutes.
    context.order_timeout = 5

    # Positions that have lost more than this percentage of their cost bases
    # will be liquidated, as a sort of global stop loss.
    context.loss_stop_percent = 12.5

    # Conversely, positions that have gained this much will be sold off as a
    # profit taking measure.
    context.profit_take_percent = 15

    # Positions that have come to occupy more than this percent of the
    # portfolio will be trimmed.
    context.max_portfolio_percent = 6

    # Set up potential stocks to purchase
    context.potential_stocks = Stock(['AAPL', 'GOOG', 'MSFT'])

def handle_data(context, data):
    # Get rid of orders that have gotten too old.
    now = get_datetime('US/Eastern')
    open_orders = get_open_orders()
    for symbol in open_orders.keys():
        for order in open_orders[symbol]:
            age = now - order.dt.astimezone('US/Eastern')
            if age.total_seconds() / 60 > context.order_timeout:
                cancel_order(order)

    # Check the moving averages of the potential stocks
    for asset in context.potential_stocks:
        short_mavg = data.history(asset, 'price', bar_count=100, frequency="1m").mean()
        long_mavg = data.history(asset, 'price', bar_count=300, frequency="1m").mean()
        log.info(f'stock: {asset}')
        logger.info(f'short_mavg: {short_mavg}')
        logger.info(f'long_mavg: {long_mavg}')
        print(asset)

        # Trading logic
        if short_mavg > long_mavg:
            # order_target orders as many shares as needed to
            # achieve the desired number of shares.
            order_target(asset, 100)
        elif short_mavg < long_mavg:
            order_target(asset, 0)

    # Liquidate positions that have reached our profit take or stop loss level.
    for asset in context.portfolio.positions.keys():
        position = context.portfolio.positions[asset]
        change = (position.cost_basis - position.last_sale_price) / position.cost_basis
        change = change * 100
        if change > context.loss_stop_percent or change > context.profit_take_percent:
            order_target(position.asset, 0)

    # Trim positions that exceed a certain percentage of our portfolio
    portfolio_value = context.portfolio.portfolio_value
    for asset in context.portfolio.positions.keys():
        position = context.portfolio.positions[asset]
        position_value = position.amount * position.last_sale_price
        portfolio_share = position_value / portfolio_value * 100
        if portfolio_share > context.max_portfolio_percent:
            order_target_percent(
                position.asset, context.max_portfolio_percent / 100
            )
