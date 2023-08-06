from typing import Callable
from src.omobono.types.currency_support import Currency
from src.omobono.types.interval import Interval, IntervalSource, interval_factory


class Coupon:

    def __init__(self, f: Callable[[Currency], Currency], duration_source: IntervalSource) -> None:
        self._f = f
        self._duration = interval_factory(duration_source)

    @property
    def duration(self) -> Interval:
        return self._duration

    @property
    def f(self) -> Callable[[Currency], Currency]:
        return self._f

    def __call__(self, orig_cost: Currency) -> Currency:
        return self.f(orig_cost)
