"""Provides a range with open or closed start and end points.

Copyright 2023 WPEngine, Inc.  All rights reserved.
"""

from typing import Generic, Optional, TypeVar
from src.omobono.types.option import Option


#: The type of start and end point in a range.
A = TypeVar("A")


class EffectiveRange(Generic[A]):
    """A range of values, with open or closed end points."""

    def __init__(self, start: Optional[A], end: Optional[A]) -> None:
        """Initializes this range.

        If no start value if provided, this range will contain arbitrarily small values.  If no end value is
        provided, this range will contain arbitrarily large values.

        Parameters:
            start: the (optional) start value for this range (inclusive)
            end: the (optional) end value for this range (inclusive)
        """
        self._start = Option.from_optional(start)
        self._end = Option.from_optional(end)

    @property
    def start(self) -> Option[A]:
        """The (optional) start value for this range (inclusive)."""
        return self._start

    @property
    def end(self) -> Option[A]:
        """The (optional) end value for this range (inclusive)."""
        return self._end

    def contains(self, a: A) -> bool:
        """Indicates whether the given value is contained within this range.

        Parameters:
            a: the value to check for containment in this range

        Returns:
            True, if this value is contained in this range; False, otherwise
        """
        start_ok = self.start.map(lambda s: a >= s).get_or_else(True)
        end_ok = self.end.map(lambda e: a <= e).get_or_else(True)
        return start_ok and end_ok
