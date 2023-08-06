"""Provides factory support for quantities.

(c) 2023 WPEngine, Inc.  All rights reserved.
"""

import decimal
import pint
from src.omobono.errors import UnparsableObjectOmobonoError
from src.omobono.types.factory import Factory


#: Type alias for input to quantity factory.
QuantitySource = pint.Quantity | decimal.Decimal | int | float | str


class UnparsableQuantityOmobonoError(UnparsableObjectOmobonoError[QuantitySource]):
    """Exception signalling the inability to parse a source as a quantity."""

    def __init__(self, source: QuantitySource) -> None:
        """Initializes this exception.

        Parameters:
            source: the source that could not be parsed
        """
        super().__init__(source, "quantity")


class _QuantityFactory(Factory[QuantitySource, pint.Quantity, UnparsableQuantityOmobonoError]):
    """Produces a quantity from the given source.

    Examples:

        >>> factory = _QuantityFactory()
        >>> factory(pint.Quantity("1m"))  # quantity source returns given source
        <Quantity(1, 'meter')>

        >>> factory(1)  # int source converted to dimensionless quantity
        <Quantity(1, 'dimensionless')>

        >>> factory(1.0)  # float source converted to dimensionless quantity
        <Quantity(1.0, 'dimensionless')>

        >>> factory(decimal.Decimal("1.0"))  # decimal source converted to dimensionless quantity
        <Quantity(1.0, 'dimensionless')>

        >>> factory("1m")  # string source with unit converted to quantity
        <Quantity(1, 'meter')>

        >>> factory("1")  # string source without unit converted to dimensionless quantity
        <Quantity(1, 'dimensionless')>
    """

    def __init__(self) -> None:
        super().__init__(UnparsableQuantityOmobonoError)

    def _produce(self, a: QuantitySource) -> pint.Quantity:
        match a:
            case pint.Quantity():
                return a
            case decimal.Decimal():
                return pint.Quantity(a)
            case int() | float():
                return pint.Quantity(decimal.Decimal(a))
            case str():
                try:
                    return pint.Quantity(decimal.Decimal(a))
                except decimal.InvalidOperation:
                    return pint.Quantity(a)


quantity_factory = _QuantityFactory()
