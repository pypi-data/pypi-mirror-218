"""Provides support functions, constants, and type aliases for currency calculations.

(c) 2023 WPEngine, Inc.  All rights reserved.
"""

from typing import Final
import decimal
import re
from src.omobono.errors import UnparsableObjectOmobonoError
from src.omobono.types.factory import Factory

#: Internal type alias for decimals.
_D = decimal.Decimal

#: Currency is just a decimal.
Currency = _D

#: Type alias for input to currency factory.
CurrencySource = _D | int | str | float

#: Useful constant.
ZERO: Final[_D] = _D("0.00")

#: A regular expression for percentages.
_CURR_REGEX: Final[re.Pattern] = re.compile(r"((?:\$\s*)?((\d+([.]\d+)?)|([.]\d+)))")


class _CurrencyFactory(Factory[CurrencySource, Currency, UnparsableObjectOmobonoError]):
    """A factory for currency values."""

    def __init__(self) -> None:
        """Initializes this factory."""
        super().__init__(lambda a: UnparsableObjectOmobonoError(a, "currency"))

    def _produce(self, a: CurrencySource) -> Currency:
        """Produces a currency value.

        Parameters:
            a: the source of the currency to be produced.

        Returns:
            the currency corresponding to the given source
        """
        match a:
            case _D():
                return a
            case int() | float():
                return _D(a)
            case str():
                m = _CURR_REGEX.fullmatch(a.strip())
                return _D(m.group(2)) if m is not None else _D(a)

    def _post_process(self, b: Currency) -> Currency:
        return b.quantize(ZERO)


#: A currency factory.
currency_factory = _CurrencyFactory()
