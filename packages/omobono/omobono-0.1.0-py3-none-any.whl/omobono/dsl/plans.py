"""Provides a dsl for defining plans efficiently.

(c) 2023 WPEngine, Inc.  All rights reserved.
"""

from typing import Callable
import enum
import arrow
import src.omobono.types as obt


# === types


class _Term(enum.Enum):
    MONTH = obt.interval_factory("interval 1 month")
    YEAR = obt.interval_factory("interval 1 year")


class _DSLPlanName:
    def __init__(self, name: str) -> None:
        self.name = name
        self.cost_options = []

    def with_cost(self, *options: "_DSLCostOption") -> "_DSLPlanNameAndCost":
        return _DSLPlanNameAndCost(self.name, [o.build() for o in options])


class _DSLPlanNameAndCost:
    def __init__(self, name: str, cost: list[obt.PlanCost]) -> None:
        self.name = name
        self.cost = cost

    def with_fees(self, *fee_lists: list[obt.Fee]) -> obt.Plan:
        return obt.Plan(self.name, self.cost, [f for fl in fee_lists for f in fl])


class _DSLCostOption:
    def __init__(self, cost: obt.Currency, duration: obt.Interval) -> None:
        self.cost = cost
        self.duration = duration
        self.coupons = []

    def build(self) -> obt.PlanCost:
        return obt.PlanCost(self.duration, self.cost, self.coupons)

    def with_coupon(self, discount: obt.CurrencySource) -> "_DSLCoupon":
        return _DSLCoupon(discount, self)


class _DSLCoupon:
    def __init__(self, discount: obt.Currency, parent: _DSLCostOption) -> None:
        self.f = lambda c: c - abs(discount)
        self.parent = parent

    def for_months(self, i: int) -> _DSLCostOption:
        self.parent.coupons.append(
            obt.Coupon(self.f, obt.interval_factory(f"interval {i} month"))
        )
        return self.parent

    def for_years(self, i: int) -> _DSLCostOption:
        self.parent.coupons.append(
            obt.Coupon(self.f, obt.interval_factory(f"interval {i} year"))
        )
        return self.parent


# === constants

monthly = _Term.MONTH
yearly = _Term.YEAR

_FOREVER = obt.EffectiveRange[arrow.Arrow](None, None)


# === functions

def plan(name: str) -> _DSLPlanName:
    return _DSLPlanName(name)


def cost_option(*, cost: obt.CurrencySource, billed: _Term) -> _DSLCostOption:
    return _DSLCostOption(obt.currency_factory(cost), billed.value)


def _fees(resource: obt.Resource) -> Callable:
    def aux(
        *, entitlement: str | None, overage_rate: obt.CurrencySource
    ) -> list[obt.Fee]:
        fees = []
        entitlement_limit = (
            obt.Option.from_optional(entitlement)
            # .map(lambda i: obt.usage_factory((resource, pint.Quantity(i, resource.normal_uom))))
            # .map(lambda i: obt.usage_factory((resource, obt.quantity_factory(i).to(resource.normal_uom))))
            # .map(lambda i: obt.usage_factory((resource, f"{i} {resource.normal_uom}")))
            .map(lambda i: obt.usage_factory((resource, i)))
            .to_optional()
        )
        if entitlement is not None:
            fees.append(
                obt.Fee(
                    name=f"{resource.name} entitlement",
                    resource=resource,
                    start_usage=None,
                    end_usage=entitlement_limit,
                    datetime_range=_FOREVER,
                    cost_fn_source=obt.ZERO,
                )
            )
        fees.append(
            obt.Fee(
                name=f"{resource.name} overages",
                resource=resource,
                start_usage=entitlement_limit,
                end_usage=None,
                datetime_range=_FOREVER,
                cost_fn_source=lambda u: u.quantity.magnitude * obt.currency_factory(overage_rate),
            )
        )
        return fees
    return aux


bandwidth = _fees(obt.Resource.BANDWIDTH)
storage = _fees(obt.Resource.STORAGE)
visitors = _fees(obt.Resource.VISITOR_COUNT)
