from pylivetrader.api import (
    record, get_open_orders, get_datetime, cancel_order, order_target,
    order_target_percent
)

def trade(orders, wait=30):
    '''This is where we actually submit the orders and wait for them to fill.
    Waiting is an important step since the orders aren't filled automatically,
    which means if your buys happen to come before your sells have filled,
    the buy orders will be bounced. In order to make the transition smooth,
    we sell first and wait for all the sell orders to fill before submitting
    our buy orders.
    '''

    # process the sell orders first
    sells = [o for o in orders if o['side'] == 'sell']
    for order in sells:
        try:
            logger.info(f'submit(sell): {order}')
            api.submit_order(
                symbol=order['symbol'],
                qty=order['qty'],
                side='sell',
                type='market',
                time_in_force='day',
            )
        except Exception as e:
            logger.error(e)
    count = wait
    while count > 0:
        pending = api.list_orders()
        if len(pending) == 0:
            logger.info(f'all sell orders done')
            break
        logger.info(f'{len(pending)} sell orders pending...')
        time.sleep(1)
        count -= 1

    # process the buy orders next
    buys = [o for o in orders if o['side'] == 'buy']
    for order in buys:
        try:
            logger.info(f'submit(buy): {order}')
            api.submit_order(
                symbol=order['symbol'],
                qty=order['qty'],
                side='buy',
                type='market',
                time_in_force='day',
            )
        except Exception as e:
            logger.error(e)
    count = wait
    while count > 0:
        pending = api.list_orders()
        if len(pending) == 0:
            logger.info(f'all buy orders done')
            break
        logger.info(f'{len(pending)} buy orders pending...')
        time.sleep(1)
        count -= 1

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

def handle_data(context, data):
    # Get rid of orders that have gotten too old.
    now = get_datetime('US/Eastern')
    open_orders = get_open_orders()
    for symbol in open_orders.keys():
        for order in open_orders[symbol]:
            age = now - order.dt.astimezone('US/Eastern')
            if age.total_seconds() / 60 > context.order_timeout:
                cancel_order(order)

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
