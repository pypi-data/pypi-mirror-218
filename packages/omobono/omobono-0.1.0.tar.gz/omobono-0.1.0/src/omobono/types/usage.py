"""Provides a usage type and supporting types and functions.

(c) 2023 WPEngine, Inc.  All rights reserved.
"""

from typing import Any, Self
import decimal
import functools
import pint
from src.omobono.errors import BadParamOmobonoError, UnparsableObjectOmobonoError
from src.omobono.types.factory import Factory
from src.omobono.types.resource import Resource, ResourceSource, resource_factory
from src.omobono.types.quantity_support import QuantitySource, quantity_factory


@functools.total_ordering
class Usage:
    """Resource usage.

    Usage consists of a quantity and an associated resource.
    """

    def __init__(self, resource: Resource, quantity: pint.Quantity) -> None:
        """Initializes this usage.

        The provided quantity is normalized to the preferred unit of measure for the resource.

        Parameters:
            resource: the resource used
            quantity: the quantity of the usage
        """
        self._resource = resource
        self._quantity = resource.normalize(quantity)

    @property
    def resource(self) -> Resource:
        """The resource used."""
        return self._resource

    @property
    def quantity(self) -> pint.Quantity:
        """The quantity of the usage."""
        return self._quantity

    def __repr__(self) -> str:
        return f"{repr(self._resource)}:{repr(self._quantity)}"

    def __str__(self) -> str:
        return f"{self._quantity} ({self.resource.name})"

    # --- ordering

    def _to_usage(self, other: Any) -> Self:
        """Converts the given ordering argument to a Usage instance."""
        if not isinstance(other, Usage):
            raise BadParamOmobonoError(
                other,
                "other",
                f"cannot compare a Usage instance with a {type(other)} instance",
            )
        if self.resource != other.resource:
            raise BadParamOmobonoError(
                other,
                "other",
                f"cannot compare a {self.resource} usage with {other.resource} usage",
            )
        return other

    def __eq__(self, other: Any):
        return self.quantity == self._to_usage(other).quantity

    def __lt__(self, other: Any):
        return self.quantity < self._to_usage(other).quantity

    # --- math

    @staticmethod
    def _to_magnitude(other: Any) -> decimal.Decimal | float | int:
        """Converts the given math argument to a magnitude."""
        match other:
            case decimal.Decimal() | float() | int():
                return other
            case str():
                return decimal.Decimal(other)
            case _:
                raise BadParamOmobonoError(
                    other,
                    "other",
                    f"cannot convert math arg of type {type(other)} to magnitude"
                )

    def _to_quantity(self, other: Any) -> pint.Quantity:
        """Converts the given math argument to a quantity."""
        match other:
            case Usage():
                return other.quantity
            case _:
                return self.resource.normalize(quantity_factory(other).value)

    def __add__(self, other: Any) -> Self:
        return Usage(self.resource, self.quantity + self._to_quantity(other))

    def __sub__(self, other: Any) -> Self:
        return Usage(self.resource, self.quantity - self._to_quantity(other))

    def __mul__(self, other: Any) -> Self:
        return Usage(self.resource, self.quantity * self._to_magnitude(other))

    def __truediv__(self, other: Any) -> Self:
        return Usage(self.resource, self.quantity / self._to_magnitude(other))

    def __floordiv__(self, other: Any) -> Self:
        return Usage(self.resource, self.quantity // self._to_magnitude(other))

    def __radd__(self, other: Any) -> Self:
        return Usage(self.resource, self._to_quantity(other) + self.quantity)

    def __rsub__(self, other: Any) -> Self:
        return Usage(self.resource, self._to_quantity(other) - self.quantity)

    def __rmul__(self, other: Any) -> Self:
        return Usage(self.resource, self._to_quantity(other) * self.quantity)

    def __rtruediv__(self, other: Any) -> Self:
        return Usage(self.resource, self._to_quantity(other) / self.quantity)

    def __rfloordiv__(self, other: Any) -> Self:
        return Usage(self.resource, self._to_quantity(other) // self.quantity)


#: Type alias for input to usage factory.
UsageSource = Usage | tuple[ResourceSource, QuantitySource]


class UnparsableUsageOmobonoError(UnparsableObjectOmobonoError[UsageSource]):
    """Exception signalling the inability to parse a source as usage."""

    def __init__(self, source: UsageSource) -> None:
        """Initializes this exception.

        Parameters:
            source: the source that could not be parsed
        """
        super().__init__(source, "usage")


class _UsageFactory(Factory[UsageSource, Usage, UnparsableUsageOmobonoError]):
    """Produces usage from the given source.

    Parameters:
        source: the (optional) source of the usage to be produced

    Returns:
        the quantity produced from the given source, wrapped in an option

    Raises:
        UnparsableUsageOmobonoError: if no quantity could be produced from the given source

    Examples:

        >>> factory = _UsageFactory()
        >>> factory(Usage(Resource.VISITOR_COUNT, pint.Quantity("1 count")))  # usage source returns given source
        <Resource.VISITOR_COUNT: _ResourceValue(name='visitor count', normal_uom=<Unit('count')>)>:<Quantity(1, 'count')>

        >>> factory((Resource.VISITOR_COUNT, pint.Quantity("1")))  # (Resource,Quantity)) source passed to Usage
        <Resource.VISITOR_COUNT: _ResourceValue(name='visitor count', normal_uom=<Unit('count')>)>:<Quantity(1, 'count')>

        >>> factory(("visitor count", 1))  # (_,int)) source passed to Usage (with normal uom)
        <Resource.VISITOR_COUNT: _ResourceValue(name='visitor count', normal_uom=<Unit('count')>)>:<Quantity(1, 'count')>

        >>> factory(("visitor count", 1.0))  # (_,float)) as (_,int)
        <Resource.VISITOR_COUNT: _ResourceValue(name='visitor count', normal_uom=<Unit('count')>)>:<Quantity(1.0, 'count')>

        >>> factory(("visitor count", decimal.Decimal("1.0")))  # (_,Decimal)) as (_,int)
        <Resource.VISITOR_COUNT: _ResourceValue(name='visitor count', normal_uom=<Unit('count')>)>:<Quantity(1.0, 'count')>

        >>> factory(("visitor count", "1"))  # (_,str)) as (_,int)
        <Resource.VISITOR_COUNT: _ResourceValue(name='visitor count', normal_uom=<Unit('count')>)>:<Quantity(1, 'count')>

        >>> factory(("visitor count", "1kcount"))  # string may also have explicit unit
        <Resource.VISITOR_COUNT: _ResourceValue(name='visitor count', normal_uom=<Unit('count')>)>:<Quantity(1000.0, 'count')>
    """

    def __init__(self):
        super().__init__(UnparsableObjectOmobonoError)

    def _produce(self, a: UsageSource) -> pint.Quantity:
        match a:
            case Usage():
                return a
            case (resource_source, quantity_source):
                return Usage(resource_factory(resource_source), quantity_factory(quantity_source))


usage_factory = _UsageFactory()
