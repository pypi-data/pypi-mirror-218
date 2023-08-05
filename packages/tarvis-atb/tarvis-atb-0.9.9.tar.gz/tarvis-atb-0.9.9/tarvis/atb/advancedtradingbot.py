from dependency_injector.wiring import Provide, inject
from decimal import Decimal
import logging
from tarvis.common import time
from tarvis.common.cache.local import LocalCache
from tarvis.common.monitoring import WatchdogLogTimer
from tarvis.common.trading import (
    BasicTradingIndicator,
    BasicTradingIndicatorSource,
    MarketPosition,
    OrderSide,
    OrderType,
    TradingPolicy,
)
from threading import Thread
from . import ExchangeAccount


class AdvancedTradingBot:
    @inject
    def __init__(
        self,
        bot_id: int,
        indicator_source: BasicTradingIndicatorSource,
        accounts: list[ExchangeAccount],
        short_selling: bool,
        interval: float,
        delay: float,
        retries: int,
        retry_delay: float,
        indicator_expiration: float,
        price_deviation_limit: float,
        premium_limit: Decimal,
        stop_loss: Decimal,
        watchdog_timeout: float,
        watchdog=Provide["watchdog"],
    ):
        """
        :param price_deviation_limit: percentage (i.e. 0.00025 is 0.025% deviation)
        :param premium_limit: percentage (i.e. 0.00025 is 0.025% premium)
        :param stop_loss: percentage (i.e. 0.2 is 20%), 0 is none
        """
        short_selling = bool(short_selling)
        interval = float(interval)
        if interval <= 0:
            raise ValueError("interval must be greater than 0.")
        delay = float(delay)
        if delay <= 0:
            raise ValueError("delay must be greater than 0.")
        if delay >= interval:
            raise ValueError("delay must be less than interval.")
        retries = int(retries)
        if retries < 0:
            raise ValueError("retries must be greater than or equal to 0.")
        retry_delay = float(retry_delay)
        if (retries * retry_delay) >= interval:
            raise ValueError(
                "The product of retries and retry_delay must be less than the interval."
            )
        indicator_expiration = float(indicator_expiration)
        if indicator_expiration <= 0:
            raise ValueError("indicator_expiration must be greater than 0.")
        price_deviation_limit = float(price_deviation_limit)
        if (price_deviation_limit < 0) or (price_deviation_limit >= 1):
            raise ValueError(
                "price_deviation_limit must be equal to 0 "
                "or greater than 0 and less than 1."
            )
        premium_limit = Decimal(premium_limit)
        if (premium_limit < 0) or (premium_limit >= 1):
            raise ValueError(
                "premium_limit must be equal to 0 or greater than 0 and less than 1."
            )
        stop_loss = Decimal(stop_loss)
        if (stop_loss < 0) or (stop_loss >= 1):
            raise ValueError(
                "stop_loss must be equal to 0 or greater than 0 and less than 1."
            )
        watchdog_timeout = float(watchdog_timeout)
        if watchdog_timeout < interval:
            raise ValueError("watchdog_timeout must be greater than interval.")

        indicator_asset_pairs = []
        for account in accounts:
            indicator_asset_pairs.extend(account.indicator_asset_pairs)
        indicator_asset_pairs = list(set(indicator_asset_pairs))

        self._logger = logging.getLogger(self.__class__.__name__)
        self._indicator_source = indicator_source
        self._accounts = accounts
        self._indicator_asset_pairs = indicator_asset_pairs
        self._short_selling = short_selling
        self._interval = interval
        self._delay = delay
        self._retries = retries
        self._retry_delay = retry_delay
        self._indicator_expiration = indicator_expiration
        self._price_deviation_limit = price_deviation_limit
        self._premium_limit = premium_limit
        self._stop_loss = stop_loss
        self._log_extra = {
            "bot_id": bot_id,
            "indicator_source": indicator_source.INDICATOR_SOURCE_NAME,
            "indicator_assets_pairs": indicator_asset_pairs,
            "interval": interval,
        }
        self._watchdog_timeout = watchdog_timeout
        self._watchdog = watchdog
        self._watchdog_timer = WatchdogLogTimer(
            watchdog_timeout, logging.ERROR, self.__class__.__name__, self._log_extra
        )
        self._watchdog.add_timer(self._watchdog_timer)
        self._accounts_threads = {}
        self._policy_cache = LocalCache()

    def _update_account_base_asset(
        self,
        account: ExchangeAccount,
        indicator: BasicTradingIndicator,
        trading_policy: TradingPolicy,
        positions: dict[str, Decimal],
        base_asset: str,
        quote_asset_position: Decimal,
        quote_price: Decimal,
        available_value: Decimal,
        allocation: float,
        log_extra_iteration: dict,
    ) -> bool:
        exchange = account.exchange
        quote_asset = account.exchange_quote_asset

        match indicator.direction:
            case MarketPosition.FLAT:
                order_side_opposing = None
                price_deviation_limit = 0
                price_allowance = 0
                stop_loss_price_ratio = None
            case MarketPosition.LONG:
                order_side_opposing = OrderSide.SELL
                price_deviation_limit = 1 + self._price_deviation_limit
                price_allowance = 1 + self._premium_limit
                stop_loss_price_ratio = 1 - self._stop_loss
            case MarketPosition.SHORT:
                order_side_opposing = OrderSide.BUY
                price_deviation_limit = 1 - self._price_deviation_limit
                price_allowance = 1 - self._premium_limit
                stop_loss_price_ratio = 1 + self._stop_loss
            case _:
                raise ValueError("Indicator direction is invalid.")

        base_asset_position = positions.get(base_asset, 0)
        orders = exchange.get_open_orders(base_asset, quote_asset)
        minimum_order_quantity = trading_policy.get_minimum_order_quantity(quote_price)
        flatten_vector = 0
        direction_vector = 0
        stop_loss_orders = []
        stop_loss_vector = 0

        for order in orders:
            cancel_order = False
            order_vector = order.get_quantity(quote_price) - order.filled_quantity

            # Cancel all (except stop loss) orders placed before the indicator
            if (order.creation_time < indicator.time) and (
                order.order_type != OrderType.STOP_LOSS
            ):
                cancel_order = True

            # Cancel all orders that are not market orders if indicator is flat
            elif (indicator.direction == MarketPosition.FLAT) and (
                order.order_type != OrderType.MARKET
            ):
                cancel_order = True

            # Cancel all stop loss orders that are not against the
            elif (order.order_type == OrderType.STOP_LOSS) and (
                order.side != order_side_opposing
            ):
                cancel_order = True

            else:
                if order.side == OrderSide.BUY:
                    order_vector = order_vector
                else:
                    order_vector = -order_vector

                # Only cancel the market orders that are not flattening
                if order.order_type == OrderType.MARKET:
                    # Cancel all sell orders if current position is short
                    # Cancel all buy orders if current position is long
                    # Tally the flattening orders
                    if (
                        (order.side == OrderSide.BUY) and (base_asset_position >= 0)
                    ) or (
                        (order.side == OrderSide.SELL) and (base_asset_position <= 0)
                    ):
                        cancel_order = True
                    else:
                        flatten_vector += order_vector

                # Tally the directional and stop loss orders
                elif order.order_type == OrderType.LIMIT:
                    direction_vector += order_vector
                elif order.order_type == OrderType.STOP_LOSS:
                    stop_loss_orders.append(order)
                    stop_loss_vector += order_vector

            if cancel_order:
                # noinspection PyProtectedMember
                self._logger.info(
                    "Cancelling order.",
                    extra={
                        **log_extra_iteration,
                        "order_side": order.side.name,
                        "order_type": order.order_type.name,
                        "order_quantity": order._quantity,
                        "order_amount": order._amount,
                    },
                )
                exchange.cancel_order(order)

        opposing_position = base_asset_position + flatten_vector
        match indicator.direction:
            case MarketPosition.LONG:
                if opposing_position > 0:
                    opposing_position = 0
            case MarketPosition.SHORT:
                if opposing_position < 0:
                    opposing_position = 0
        flatten_quantity = abs(trading_policy.align_quantity(opposing_position))

        if (flatten_quantity != 0) and (flatten_quantity >= minimum_order_quantity):
            flatten_quantity = trading_policy.limit_quantity_maximum(
                flatten_quantity, quote_price
            )
            if opposing_position > 0:
                flatten_order_side = OrderSide.SELL
            else:
                flatten_order_side = OrderSide.BUY
            self._logger.info(
                "Placing flattening order.",
                extra={
                    **log_extra_iteration,
                    "order_side": flatten_order_side.name,
                    "order_quantity": flatten_quantity,
                },
            )
            exchange.place_order(
                trading_policy,
                base_asset,
                quote_asset,
                flatten_order_side,
                OrderType.MARKET,
                flatten_quantity,
                price=quote_price,
                increasing_position=False,
            )
            return False

        if indicator.direction == MarketPosition.FLAT:
            return True

        else:
            # If indicator has expired or is impossible to complete, do not move
            if (time.time() > (indicator.time + self._indicator_expiration)) or (
                (indicator.direction == MarketPosition.SHORT)
                and (
                    (not self._short_selling) or (not exchange.short_selling_supported)
                )
            ):
                direction_completed = True

            # If the quoted price deviates too far from the indicator, do not move
            elif (indicator.price is not None) and (
                (
                    (indicator.direction == MarketPosition.LONG)
                    and (quote_price > (indicator.price * price_deviation_limit))
                )
                or (
                    (indicator.direction == MarketPosition.SHORT)
                    and (quote_price < (indicator.price * price_deviation_limit))
                )
            ):
                self._logger.debug(
                    "Directional order not placed due to excessive price deviation.",
                    extra={
                        **log_extra_iteration,
                        "quote_price": quote_price,
                    },
                )
                direction_completed = True

            # Otherwise, attempt to move in the direction
            else:
                order_price = quote_price * price_allowance
                order_price = trading_policy.align_price(order_price)

                # Value is in quote asset price
                base_value = base_asset_position * quote_price

                leverage = indicator.leverage * account.leverage_multiplier
                if leverage > account.leverage_limit:
                    leverage = account.leverage_limit

                current_ratio = abs(base_value) / available_value
                desired_ratio = Decimal(
                    (1 - indicator.take_profit)
                    * allocation
                    * leverage
                    * indicator.averaging_factor
                )

                order_ratio = desired_ratio - current_ratio
                order_vector = order_ratio * available_value / order_price

                if indicator.direction == MarketPosition.SHORT:
                    order_vector = -order_vector

                order_vector -= direction_vector
                order_vector = trading_policy.align_quantity(order_vector)
                if order_vector > 0:
                    order_side = OrderSide.BUY
                else:
                    order_side = OrderSide.SELL
                order_quantity = abs(order_vector)

                self._logger.debug(
                    "Directional determinants calculated.",
                    extra={
                        **log_extra_iteration,
                        "positions": positions,
                        "base_asset_position": base_asset_position,
                        "quote_asset_position": quote_asset_position,
                        "quote_price": quote_price,
                        "order_price": order_price,
                        "current_ratio": current_ratio,
                        "desired_ratio": desired_ratio,
                        "direction_vector": direction_vector,
                        "order_vector": order_vector,
                        "minimum_order_quantity": minimum_order_quantity,
                    },
                )

                # If there is no profit taking, then do not move against the position
                if (indicator.take_profit == 0) and (order_side == order_side_opposing):
                    direction_completed = True

                # If profit taking has begun, do not move further into the position
                elif (indicator.take_profit > 0) and (
                    order_side != order_side_opposing
                ):
                    direction_completed = True

                # If profit taking, do not move further until previous orders complete
                elif (direction_vector != 0) and (indicator.take_profit > 0):
                    direction_completed = True

                # If the order quantity does not meet the minimum, do not order
                elif (order_quantity == 0) or (order_quantity < minimum_order_quantity):
                    direction_completed = True

                # Otherwise, place a limit order to move in the direction
                else:
                    direction_completed = False

                    # Some exchanges will automatically create stop losses when an order
                    # is filled
                    if self._stop_loss == 0:
                        stop_loss_price = None
                    else:
                        stop_loss_price = quote_price * stop_loss_price_ratio
                        stop_loss_price = trading_policy.align_price(stop_loss_price)

                    order_quantity = trading_policy.limit_quantity_maximum(
                        order_quantity, order_price
                    )
                    self._logger.info(
                        "Placing directional order.",
                        extra={
                            **log_extra_iteration,
                            "order_side": order_side.name,
                            "order_quantity": order_quantity,
                            "order_price": order_price,
                            "order_amount": order_quantity * order_price,
                        },
                    )
                    exchange.place_order(
                        trading_policy,
                        base_asset,
                        quote_asset,
                        order_side,
                        OrderType.LIMIT,
                        order_quantity,
                        price=order_price,
                        stop_loss_price=stop_loss_price,
                        increasing_position=True,
                    )

            # If stop loss is not possible or requested, do not add a stop loss
            if (not exchange.stop_loss_orders_supported) or (self._stop_loss == 0):
                stop_loss_completed = True

            # If the direction has not been achieved, no stop loss is needed
            elif (
                (indicator.direction == MarketPosition.LONG)
                and (base_asset_position <= 0)
            ) or (
                (indicator.direction == MarketPosition.SHORT)
                and (base_asset_position >= 0)
            ):
                stop_loss_completed = True

            # Otherwise, add or adjust the stop loss
            else:
                stop_loss_position = base_asset_position + stop_loss_vector
                stop_loss_excessive = (
                    (indicator.direction == MarketPosition.LONG)
                    and (stop_loss_position < 0)
                ) or (
                    (indicator.direction == MarketPosition.SHORT)
                    and (stop_loss_position > 0)
                )
                stop_loss_quantity = abs(
                    trading_policy.align_quantity(stop_loss_position)
                )

                stop_loss_completed = (not stop_loss_excessive) and (
                    stop_loss_quantity < minimum_order_quantity
                )

                if stop_loss_excessive:
                    order = stop_loss_orders.pop()
                    # noinspection PyProtectedMember
                    self._logger.info(
                        "Cancelling excessive stop-loss order.",
                        extra={
                            **log_extra_iteration,
                            "order_side": order.side.name,
                            "order_type": order.order_type.name,
                            "order_quantity": order._quantity,
                            "order_amount": order._amount,
                        },
                    )
                    exchange.cancel_order(order)

                elif stop_loss_quantity >= minimum_order_quantity:
                    stop_loss_price = quote_price * stop_loss_price_ratio
                    stop_loss_price = trading_policy.align_price(stop_loss_price)
                    stop_loss_quantity = trading_policy.limit_quantity_maximum(
                        stop_loss_quantity, stop_loss_price
                    )
                    self._logger.info(
                        "Placing stop loss order.",
                        extra={
                            **log_extra_iteration,
                            "order_side": order_side_opposing.name,
                            "order_quantity": stop_loss_quantity,
                            "order_price": stop_loss_price,
                        },
                    )
                    # TODO: Pass a price for when the stop loss is a stop limit order
                    exchange.place_order(
                        trading_policy,
                        base_asset,
                        quote_asset,
                        order_side_opposing,
                        OrderType.STOP_LOSS,
                        stop_loss_quantity,
                        stop_loss_price=stop_loss_price,
                        increasing_position=False,
                    )

            return direction_completed and stop_loss_completed

    def _update_account_iteration(
        self,
        account: ExchangeAccount,
        indicators: dict[tuple[str, str], BasicTradingIndicator],
        trading_policies: dict[tuple[str, str], TradingPolicy],
        quotes: dict[tuple[str, str], Decimal],
        log_extra_update: dict,
    ) -> bool:
        exchange = account.exchange
        exchange_quote_asset = account.exchange_quote_asset
        positions = exchange.get_positions()
        quote_asset_position = positions.get(exchange_quote_asset, 0)

        total_value = quote_asset_position
        for exchange_asset_pair in account.exchange_asset_pairs:
            exchange_base_asset, _ = exchange_asset_pair
            amount = positions.get(exchange_base_asset, 0)
            if amount != 0:
                quote_price = quotes[exchange_asset_pair]
                total_value += quote_price * amount

        available_value = total_value - account.reserve
        if (account.position_limit is not None) and (
            available_value > account.position_limit
        ):
            available_value = account.position_limit

        completed = True
        for indicator_asset_pair, indicator in indicators.items():
            indicator_base_asset, _ = indicator_asset_pair
            for account_division in account.divisions:
                if account_division.indicator_asset_pair == indicator_asset_pair:
                    exchange_base_asset = account_division.exchange_base_asset
                    allocation = account_division.allocation
                    asset_pair = (
                        exchange_base_asset,
                        exchange_quote_asset,
                    )
                    trading_policy = trading_policies[asset_pair]
                    quote_price = quotes[asset_pair]

                    log_extra_iteration = {
                        **log_extra_update,
                        "indicator_time": indicator.time,
                        "indicator_direction": indicator.direction.name,
                        "exchange_account_id": account.exchange_account_id,
                        "exchange": exchange.EXCHANGE_NAME,
                        "exchange_base_asset": exchange_base_asset,
                        "exchange_quote_asset": exchange_quote_asset,
                    }
                    if indicator.price is not None:
                        log_extra_iteration["indicator_price"] = indicator.price

                    try:
                        update_completed = self._update_account_base_asset(
                            account,
                            indicator,
                            trading_policy,
                            positions,
                            exchange_base_asset,
                            quote_asset_position,
                            quote_price,
                            available_value,
                            allocation,
                            log_extra_iteration,
                        )
                        completed = completed and update_completed
                    except Exception as unhandled_exception:
                        completed = False
                        self._logger.critical(
                            f"Unhandled exception: {unhandled_exception}",
                            extra=log_extra_iteration,
                            exc_info=True,
                        )

        return completed

    def _update_account(
        self,
        account: ExchangeAccount,
        indicators: dict[tuple[str, str], BasicTradingIndicator],
    ) -> None:
        exchange_watchdog_timer = None
        log_extra_update = None

        try:
            exchange = account.exchange
            exchange_account_id = account.exchange_account_id
            log_extra_update = {
                **self._log_extra,
                "exchange_account_id": exchange_account_id,
                "exchange": exchange.EXCHANGE_NAME,
            }

            self._logger.debug(
                f"Exchange {exchange.EXCHANGE_NAME} {exchange_account_id} updating.",
                extra=log_extra_update,
            )

            exchange_watchdog_timer = WatchdogLogTimer(
                self._watchdog_timeout,
                logging.ERROR,
                self.__class__.__name__,
                log_extra_update,
            )
            self._watchdog.add_timer(exchange_watchdog_timer)
            exchange_watchdog_timer.reset()

            trading_policies = self._policy_cache.get(exchange_account_id)
            if trading_policies is None:
                trading_policies = exchange.get_policies(account.exchange_asset_pairs)
                self._policy_cache.set(
                    exchange_account_id,
                    trading_policies,
                    ttl=account.policy_cache_expiration,
                )

            quotes = exchange.get_quotes(account.exchange_asset_pairs)

            completed = False
            retries = self._retries
            while (not completed) and (retries >= 0):
                retries -= 1
                exchange_watchdog_timer.reset()
                completed = self._update_account_iteration(
                    account, indicators, trading_policies, quotes, log_extra_update
                )
                if (not completed) and (retries >= 0):
                    time.sleep(self._retry_delay)

            if not completed:
                self._logger.warning(
                    f"Exchange {exchange.EXCHANGE_NAME} {exchange_account_id} "
                    f"failed updating after {self._retries} retries.",
                    extra=log_extra_update,
                )

        except Exception as unhandled_exception:
            self._logger.critical(
                f"Unhandled exception: {unhandled_exception}",
                extra=log_extra_update,
                exc_info=True,
            )

        if exchange_watchdog_timer is not None:
            self._watchdog.remove_timer(exchange_watchdog_timer)

    def _trade(self) -> None:
        while True:
            try:
                self._watchdog_timer.reset()

                now = time.time()

                indicators = self._indicator_source.get_indicators(
                    now, self._indicator_asset_pairs
                )

                if not indicators:
                    self._logger.warning("No Indicators.", extra=self._log_extra)
                else:
                    indicator_asset_pairs = list(indicators.keys())
                    for account in self._accounts:
                        if account.indicator_asset_pairs_mapped(indicator_asset_pairs):
                            account_thread = self._accounts_threads.pop(account, None)
                            if (
                                account_thread is not None
                            ) and account_thread.is_alive():
                                exchange_name = account.exchange.EXCHANGE_NAME
                                exchange_account_id = account.exchange_account_id
                                self._logger.warning(
                                    f"Exchange {exchange_name} {exchange_account_id} "
                                    "is still updating from last interval.",
                                    extra={
                                        **self._log_extra,
                                        "exchange_account_id": exchange_account_id,
                                        "exchange": exchange_name,
                                    },
                                )
                            else:
                                account_thread = Thread(
                                    target=self._update_account,
                                    args=(account, indicators),
                                )
                                account_thread.start()

                            self._accounts_threads[account] = account_thread

            except Exception as unhandled_exception:
                self._logger.critical(
                    f"Unhandled exception: {unhandled_exception}",
                    extra=self._log_extra,
                    exc_info=True,
                )

            next_time = time.next_interval(time.time(), self._interval)
            next_time += self._delay
            time.sleep_until(next_time)

    def start(self) -> Thread:
        accounts_text = []
        accounts_list = []
        for account in self._accounts:
            exchange_name = account.exchange.EXCHANGE_NAME
            exchange_account_id = account.exchange_account_id
            accounts_text.append(
                f"{exchange_name} {exchange_account_id}: "
                f"{account.exchange_asset_pairs} "
            )
            accounts_list.append(
                {
                    "exchange": exchange_name,
                    "exchange_account_id": exchange_account_id,
                    "exchange_asset_pairs": account.exchange_asset_pairs,
                }
            )
        self._logger.info(
            f"Starting trading with indicators {self._indicator_asset_pairs} "
            f"on accounts {accounts_text} every {self._interval} seconds.",
            extra={**self._log_extra, "accounts": accounts_list},
        )
        trading_thread = Thread(target=self._trade)
        trading_thread.start()
        return trading_thread
