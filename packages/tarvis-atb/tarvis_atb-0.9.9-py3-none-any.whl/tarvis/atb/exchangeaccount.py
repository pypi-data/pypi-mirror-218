from decimal import Decimal
import logging
from tarvis.common.trading import Exchange


class ExchangeAccountDivision:
    def __init__(
        self,
        indicator_quote_asset: str,
        exchange_base_asset: str,
        allocation: float = 1,
        indicator_base_asset: str = None,
    ):
        if allocation <= 0:
            raise ValueError("allocation must be greater than 0.")
        if indicator_base_asset is None:
            indicator_base_asset = exchange_base_asset

        self.exchange_base_asset = exchange_base_asset
        self.allocation = float(allocation)
        self.indicator_base_asset = indicator_base_asset
        self.indicator_quote_asset = indicator_quote_asset
        self.indicator_asset_pair = (indicator_base_asset, indicator_quote_asset)


class ExchangeAccount:
    def __init__(
        self,
        exchange_account_id: int,
        exchange: Exchange,
        divisions: list[ExchangeAccountDivision],
        exchange_quote_asset: str,
        reserve: Decimal = 0,
        position_limit: Decimal = None,
        leverage_multiplier: float = 1,
        leverage_limit: float = 1,
        policy_cache_expiration: float = 3600,
    ):
        if not divisions:
            raise ValueError("divisions is empty.")
        allocation_total = 0
        indicator_asset_pairs = []
        exchange_asset_pairs = []
        for division in divisions:
            allocation_total += division.allocation
            indicator_asset_pairs.append(division.indicator_asset_pair)
            exchange_asset_pairs.append(
                (division.exchange_base_asset, exchange_quote_asset)
            )
        if allocation_total > 1:
            logging.warning(
                "Total allocations is greater than 100%",
                extra={
                    "exchange_account_id": exchange_account_id,
                    "exchange": exchange.EXCHANGE_NAME,
                    "allocation_total": allocation_total,
                },
            )
        reserve = Decimal(reserve)
        if reserve < 0:
            raise ValueError("reserve must be greater than or equal to 0.")
        if position_limit is not None:
            position_limit = Decimal(position_limit)
            if position_limit <= 0:
                raise ValueError("position_limit must be greater than 0.")
        leverage_multiplier = float(leverage_multiplier)
        if leverage_multiplier <= 0:
            raise ValueError("leverage_multiplier must be greater than 0.")
        leverage_limit = float(leverage_limit)
        if leverage_limit <= 0:
            raise ValueError("leverage_limit must be greater than 0.")

        self.exchange_account_id = exchange_account_id
        self.exchange = exchange
        self.divisions = divisions
        self.exchange_quote_asset = exchange_quote_asset
        self.indicator_asset_pairs = set(indicator_asset_pairs)
        self.exchange_asset_pairs = list(set(exchange_asset_pairs))
        self.reserve = Decimal(reserve)
        self.position_limit = position_limit
        self.leverage_multiplier = leverage_multiplier
        self.leverage_limit = leverage_limit
        self.policy_cache_expiration = policy_cache_expiration

    def indicator_asset_pairs_mapped(self, mapped_pairs: list[tuple[str, str]]) -> bool:
        return any((True for x in mapped_pairs if x in self.indicator_asset_pairs))
