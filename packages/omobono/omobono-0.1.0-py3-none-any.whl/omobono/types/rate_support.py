"""Provides support functions, constants, and type aliases for rate calculations.

(c) 2023 WPEngine, Inc.  All rights reserved.
"""

from typing import Final
import decimal
import fractions
import re
from src.omobono.errors import UnparsableObjectOmobonoError
from src.omobono.types.currency_support import CurrencySource, ZERO
from src.omobono.types.factory import Factory

#: Internal type alias for decimals.
_D = decimal.Decimal

#: A rate is just a decimal.
Rate = _D

#: Type alias for input to rate factory,
RateSource = fractions.Fraction | tuple[int, int] | CurrencySource

#: A regular expression for percentages.
_PCT_REGEX: Final[re.Pattern] = re.compile(r"((\d+([.]\d+)?)|([.]\d+))%")


class _RateFactory(Factory[RateSource, Rate, UnparsableObjectOmobonoError]):
    def __init__(self) -> None:
        super().__init__(lambda a: UnparsableObjectOmobonoError(a, "rate"))

    def _produce(self, a: RateSource) -> Rate:
        match a:
            case fractions.Fraction():
                return _D(float(a))
            case tuple():
                return _D(float(a[0]) / float(a[1]))
            case _D():
                return a
            case int() | float():
                return _D(a)
            case str():
                m = _PCT_REGEX.fullmatch(a.strip())
                return _D(m.group(1)) if m is not None else _D(a)

    def _post_process(self, b: Rate) -> Rate:
        return b.quantize(ZERO)


rate_factory = _RateFactory()
