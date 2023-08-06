import copy
from src.omobono.types.coupon import Coupon
from src.omobono.types.currency_support import (
    Currency,
    CurrencySource,
    currency_factory,
)
from src.omobono.types.interval import Interval, IntervalSource, interval_factory


class PlanCost:
    def __init__(self, period_source: IntervalSource, cost_source: CurrencySource, coupons: list[Coupon]):
        self._period = interval_factory(period_source)
        self._cost = currency_factory(cost_source)
        self._coupons = coupons

    @property
    def cost(self) -> Currency:
        return self._cost

    @property
    def coupons(self) -> list[Coupon]:
        return copy.deepcopy(self._coupons)

    @property
    def period(self) -> Interval:
        return self._period

    def __str__(self) -> str:
        return f"{self._cost} / {self._period}"
