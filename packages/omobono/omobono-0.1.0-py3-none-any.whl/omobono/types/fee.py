"""Provides a fee for resource usage.

Copyright 2023 WPEngine, Inc.  All rights reserved.
"""

from typing import Callable, Optional
import decimal
import arrow

from src.omobono.errors import BadParamOmobonoError, UnparsableObjectOmobonoError
from src.omobono.types.currency_support import Currency, ZERO
from src.omobono.types.effective_range import EffectiveRange
from src.omobono.types.factory import Factory
from src.omobono.types.resource import Resource
from src.omobono.types.usage import Usage


#: Type alias for a fee cost function.
_FeeCostFn = Callable[[Usage], Currency]

#: Type alias for input to a fee cost function factory.
_FeeCostFnSource = _FeeCostFn | Currency


class _FeeCostFnFactory(
    Factory[_FeeCostFnSource, _FeeCostFn, UnparsableObjectOmobonoError]
):
    def __init__(self) -> None:
        super().__init__(lambda a: UnparsableObjectOmobonoError(a, "cost function"))

    def _produce(self, a: _FeeCostFnSource) -> _FeeCostFn:
        # print(f"src={a}, type={type(a)}, callable?={callable(a)}")
        # f = a if callable(a) else lambda _: a
        # print(f"f(100) = {f(Usage(Resource.VISITOR_COUNT, pint.Quantity(100)))}")
        return a if callable(a) else lambda _: a


_fee_cost_fn_factory = _FeeCostFnFactory()


class Fee:
    """A fee to be applied to resource usage.

    A fee has a name, a range of usages to which it applies, a range of dates during which it applies, and a function
    that maps a usage to a cost.
    """

    def __init__(
        self,
        name: str,
        resource: Resource,
        start_usage: Optional[Usage],
        end_usage: Optional[Usage],
        datetime_range: EffectiveRange[arrow.Arrow],
        cost_fn_source: _FeeCostFnSource,
    ) -> None:
        """Initializes this fee.

        If the `cost_fn_or_const` is a decimal (constant cost), the inferred cost function ignores its input and always
        returns the given constant.

        Parameters:
            name: the name of this fee
            resource: the resource to which this fee applies
            start_usage: the (optional) start of the usage range to which this fee applies
            end_usage: the (optional) end of the usage range to which this fee applies
            datetime_range: the range of dates during which this fee applies
            cost_fn_source: (the source of) the cost function
        """
        if start_usage is not None and start_usage.resource != resource:
            raise BadParamOmobonoError(
                start_usage,
                "start",
                f"usage range start resource {start_usage.resource} does not match given resource {resource}",
            )
        if end_usage is not None and end_usage.resource != resource:
            raise BadParamOmobonoError(
                end_usage,
                "end",
                f"usage range end resource {end_usage.resource} does not match given resource {resource}",
            )
        self._name = name
        self._resource = resource
        self._usage_range = EffectiveRange[Usage](start_usage, end_usage)
        self._datetime_range = datetime_range
        self._cost_fn = _fee_cost_fn_factory(cost_fn_source)

    @property
    def cost_fn(self) -> _FeeCostFn:
        """The function that maps a usage to a cost."""
        return self._cost_fn

    @property
    def datetime_range(self) -> EffectiveRange[arrow.Arrow]:
        """The range of dates during which this fee applies."""
        return self._datetime_range

    @property
    def name(self) -> str:
        """The name of this fee."""
        return self._name

    @property
    def resource(self) -> Resource:
        """The resource associated with this fee."""
        return self._resource

    @property
    def usage_range(self) -> EffectiveRange[Usage]:
        """The range of usage to which this fee applies."""
        return self._usage_range

    def __call__(self, dt: arrow.Arrow, usage: Usage) -> decimal.Decimal:
        if self.resource != usage.resource:
            raise BadParamOmobonoError(
                usage, "usage", "given usage has the wrong resource"
            )
        return (
            max(
                ZERO,
                self.cost_fn(
                    self.usage_range.start.map(lambda s: usage - s).get_or_else(usage)
                ),
            )
            if self.datetime_range.contains(dt) and self.usage_range.contains(usage)
            else ZERO
        )
