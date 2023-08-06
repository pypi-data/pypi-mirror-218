"""Provides a discount type for plan cost.

Copyright 2023 WPEngine, Inc.  All rights reserved.
"""

from typing import Callable
import decimal
from src.omobono.errors import BadParamOmobonoError, UnparsableObjectOmobonoError
from src.omobono.types.factory import Factory


_DiscountAdjustmentFn = Callable[[decimal.Decimal], decimal.Decimal]

_DiscountAdjustmentFnSource = _DiscountAdjustmentFn | decimal.Decimal | float | str

_ZERO = decimal.Decimal("0.00")


class _DiscountAdjustmentFnFactory(
    Factory[_DiscountAdjustmentFnSource, _DiscountAdjustmentFn, UnparsableObjectOmobonoError]
):
    def __init__(self) -> None:
        super().__init__(lambda a: UnparsableObjectOmobonoError(a, "adjustment function"))

    def _produce(self, a: _DiscountAdjustmentFnSource) -> _DiscountAdjustmentFn:
        if callable(a):
            return a
        match a:
            case decimal.Decimal():
                return lambda c: c * a
            case float() | int() | str():
                return lambda c: c * decimal.Decimal(a).normalize(_ZERO)


_discount_adjustment_fn_factory = _DiscountAdjustmentFnFactory()


class Discount:
    def __init__(
        self, term: int, adjustment_fn_source: _DiscountAdjustmentFnSource
    ) -> None:
        self._term = term
        self._adjustment_fn = _discount_adjustment_fn_factory(adjustment_fn_source)

    @property
    def adjustment_fn(self) -> _DiscountAdjustmentFn:
        return self._adjustment_fn

    @property
    def term(self) -> int:
        return self._term

    def __call__(self, term: int, cost: decimal.Decimal) -> decimal.Decimal:
        return cost if term < self.term else self.adjustment_fn(cost)
