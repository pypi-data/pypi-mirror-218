"""Provides factory support for quantities.

(c) 2023 WPEngine, Inc.  All rights reserved.
"""

import datetime
import arrow
from src.omobono.errors import UnparsableObjectOmobonoError
from src.omobono.types.factory import Factory


#: Type alias for input to arrow factory.
ArrowSource = arrow.Arrow | datetime.date | datetime.datetime | str


class UnparsableArrowOmobonoError(UnparsableObjectOmobonoError[ArrowSource]):
    """Exception signalling the inability to parse a source as an arrow date/time."""

    def __init__(self, source: ArrowSource) -> None:
        """Initializes this exception.

        Parameters:
            source: the source that could not be parsed
        """
        super().__init__(source, "arrow date/time")


class _ArrowFactory(Factory[ArrowSource, arrow.Arrow, UnparsableArrowOmobonoError]):
    """Produces an arrow date/time from the given source.

    Examples:

        >>> factory = _ArrowFactory()
        >>> factory(arrow.get("2023-06-01T01:23:34Z"))  # arrow source returns given source
        <Arrow [2023-06-01T01:23:34+00:00]>

        >>> factory(datetime.datetime(2023, 6, 1, 1, 23, 34))  # datetime source converted to arrow
        <Arrow [2023-06-01T01:23:34+00:00]>

        >>> factory(datetime.date(2023, 6, 1))  # date source converted to arrow
        <Arrow [2023-06-01T00:00:00+00:00]>

        >>> factory("2023-06-01")  # string source parsed as arrow
        <Arrow [2023-06-01T00:00:00+00:00]>
    """

    def __init__(self):
        super().__init__(UnparsableArrowOmobonoError)

    def _produce(self, a: ArrowSource) -> arrow.Arrow:
        match a:
            case arrow.Arrow():
                return a
            case datetime.datetime():
                return arrow.Arrow.fromdatetime(a)
            case datetime.date():
                return arrow.Arrow.fromdate(a)
            case str():
                return arrow.get(a)


arrow_factory = _ArrowFactory()
