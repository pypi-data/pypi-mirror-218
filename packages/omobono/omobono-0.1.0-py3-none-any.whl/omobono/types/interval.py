"""Provides a time interval and supporting types and functions.

(c) 2023 WPEngine, Inc.  All rights reserved.
"""

import copy
import datetime
import enum
import re
from typing import Any, ClassVar, Optional
import arrow
from src.omobono.errors import UnparsableObjectOmobonoError
from src.omobono.types.factory import Factory


#: A mapping in which each entry associates a date/time part to its value.
_DTValueMapping = dict["_DTPart", Any]


class _DateTimeUnitValue:
    """A date/time part value."""

    def __init__(self, bq_name: str, arrow_name: Optional[str] = None) -> None:
        """Initializes a date/time part value.

        Parameters:
            bq_name: the name of this date/time part in BigQuery
            arrow_name: the name of this date/time part in the arrow API

        If the arrow API name parameter is omitted, the arrow name for this value will be constructed by adding 's'
        to the given BigQuery name.

        Examples:

            >>> _DateTimeUnitValue("foo", "bar").bq_name == "foo"  # explicit bq name same case match
            True

            >>> _DateTimeUnitValue("foo", "bar").bq_name == "FOO"  # explicit bq name case mismatch
            False

            >>> _DateTimeUnitValue("foo", "bar").arrow_name == "bar"  # explicit arrow name same case match
            True

            >>> _DateTimeUnitValue("foo").bq_name == "foo"  # explicit bq name (implicit arrow name) same case match
            True

            >>> _DateTimeUnitValue("foo").arrow_name == "foos"  # implicit arrow name same case match
            True
        """
        self._bq_name = bq_name
        self._arrow_name = arrow_name if arrow_name is not None else f"{bq_name}s"
        self._str_value = (
            f"{bq_name}(s)"
            if self._arrow_name == f"{self._bq_name}s"
            else f"{bq_name}/{arrow_name}"
        )

    @property
    def arrow_name(self) -> str:
        """Returns the name of this date/time part value in the arrow API."""
        return self._arrow_name

    @property
    def bq_name(self) -> str:
        """Returns the name of this date/time part value in BigQuery."""
        return self._bq_name

    def matches_arrow_name(self, s: str) -> bool:
        """Indicates if the given string matches the arrow API name of this value (under case folding).

        Parameters:
            s: the string to be matched against the arrow API name of this value

        Returns:
            True, if this string matches the arrow API name of this value (under case folding);
            False, otherwise.

        Examples:

            >>> _DateTimeUnitValue("foo", "bar").matches_arrow_name("bar")  # explicit arrow name same case match
            True

            >>> _DateTimeUnitValue("foo", "bar").matches_arrow_name("BAR")  # explicit arrow name case-folded match
            True

            >>> _DateTimeUnitValue("foo", "bar").matches_arrow_name("foo")  # explicit arrow name mismatch
            False

            >>> _DateTimeUnitValue("foo").matches_arrow_name("FOOS")  # implicit arrow name case-folded match
            True
        """
        return self._arrow_name.casefold() == s.casefold()

    def matches_bq_name(self, s: str) -> bool:
        """Indicates if the given string matches the BigQuery name of this value (under case folding).

        Parameters:
            s: the string to be matched against the BigQuery name of this value

        Returns:
            True, if this string matches the BigQuery name of this value (under case folding);
            False, otherwise.

        Examples:

            >>> _DateTimeUnitValue("foo", "bar").matches_bq_name("foo")  # same case match
            True

            >>> _DateTimeUnitValue("foo", "bar").matches_bq_name("FOO")  # case-folded match
            True

            >>> _DateTimeUnitValue("foo", "bar").matches_bq_name("bar")  # mismatched bq name
            False
        """
        return self._bq_name.casefold() == s.casefold()

    def __str__(self) -> str:
        return self._str_value


class DateTimeUnit(enum.Enum):
    """A unit of a date/time."""

    #: A year (12 months).
    YEAR = _DateTimeUnitValue("year")

    #: A quarter (3 months).
    QUARTER = _DateTimeUnitValue("quarter")

    #: A month.
    MONTH = _DateTimeUnitValue("month")

    #: A week (7 days).
    WEEK = _DateTimeUnitValue("week")

    #: A day.
    DAY = _DateTimeUnitValue("day")

    #: An hour (3600 seconds).
    HOUR = _DateTimeUnitValue("hour")

    #: A minute (60 seconds).
    MINUTE = _DateTimeUnitValue("minute")

    #: A second.
    SECOND = _DateTimeUnitValue("second")

    @classmethod
    def from_bq_name(cls, bq_name: str) -> "DateTimeUnit":
        """Return the date/time part corresponding to the given BigQuery name.

        This method compares the given name and the BigQuery names of date/time parts under case-folding.

        Parameters:
            bq_name: the BigQuery name of the date/time part to return

        Returns:
            the date/time part corresponding to the given BigQuery name

        Raises:
            ValueError: if no date/time part has the given BigQuery name

        Examples:

            >>> DateTimeUnit.from_bq_name("hour")  # lower case bq name
            _DTPart.HOUR(hour(s))

            >>> DateTimeUnit.from_bq_name("HOUR")  # upper case bq name
            _DTPart.HOUR(hour(s))
        """
        for dtp in DateTimeUnit:
            if dtp.value.matches_bq_name(bq_name):
                return dtp
        raise UnparsableObjectOmobonoError(bq_name, "date/time part")

    @property
    def arrow_name(self) -> str:
        """Returns the name of this date/time part in the arrow API."""
        return self.value.arrow_name

    @property
    def bq_name(self) -> str:
        """Returns the name of this date/time part in BigQuery."""
        return self.value.bq_name

    def __call__(self, v: int, d: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        new_d = copy.deepcopy(d) if d is not None else {}
        new_d[self.arrow_name] = v
        return new_d

    def __repr__(self) -> str:
        return f"_DTPart.{self.name}({self.value})"


class Interval:
    """Representation of an interval of time."""

    #: A regular expression describing intervals made of exactly 1 date/time part.
    _SINGLE_DTP_REGEX: ClassVar[re.Pattern] = re.compile(
        r"interval\s+(-?\d+)\s+(year|month|day)", flags=re.IGNORECASE
    )

    @staticmethod
    def _parse_dtv_map_from_single_dtp(s: str) -> Optional[_DTValueMapping]:
        """Attempts to parse a date/time value map from a string.

        This parser recognizes strings of the form "interval <int> <date/time part>". See
        https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#construct_interval.

        Parameters:
            s: the string to be parsed

        Returns:
            the parsed date/time part, if the parse was successful; None, otherwise

        Raises:
            UnparsableIntervalOmobonoError: if the parse was successful, but the date/time part name was unrecognized
        """
        mo = Interval._SINGLE_DTP_REGEX.fullmatch(s)
        if mo is None:
            return None
        for dtp in DateTimeUnit:
            if dtp.bq_name.casefold() == mo.group(2):
                return {dtp: int(mo.group(1))}
        raise UnparsableIntervalOmobonoError(s)

    @staticmethod
    def _parse_dtv_map_dtp_range(_s: str) -> Optional[_DTValueMapping]:
        """Attempts to parse a date/time value map from a string.

        NB: This is not yet implemented, so this method always returns None.

        This parser recognizes strings of the form "interval <parts_string> <date/time part> <date/time_part>". See
        https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#construct_interval.

        Parameters:
            _s: the string to be parsed

        Returns:
            the parsed date/time part, if the parse was successful; None, otherwise
        """
        return None  # TODO: add this implementation later

    @staticmethod
    def _parse_dtv_map(s: str):
        """Attempts to parse a date/time value map from a string.

        The given string is stripped and case-folded before being parsed.

        Parameters:
            s: the string to be parsed

        Returns:
            the interval parsed from the given string

        Raises:
            UnparsableIntervalOmobonoError: if the given string could not be parsed
        """
        s_ = s.strip().casefold()
        for f in [
            Interval._parse_dtv_map_from_single_dtp,
            Interval._parse_dtv_map_dtp_range,
        ]:
            i = f(s_)
            if i is not None:
                return i
        raise UnparsableIntervalOmobonoError(s)

    def __init__(self, value: _DTValueMapping | str) -> None:
        """Initializes an interval.

        Parameters:
            value: either a date/time value map, or a string version of such a map

        Raises:
            UnparsableIntervalOmobonoError: if the given value string could not be parsed

        Examples:

            >>> Interval({DateTimeUnit.DAY: 1})  # dictionary of date/time parts
            Interval({_DTPart.DAY: 1})

            >>> Interval("interval 1 day")  # string parsed as interval
            Interval({_DTPart.DAY: 1})
        """
        self._dtv_map = (
            value if isinstance(value, dict) else Interval._parse_dtv_map(value)
        )
        self._kwargs = {k.arrow_name: v for k, v in self._dtv_map.items()}

    @property
    def dtv_map(self) -> dict[DateTimeUnit, Any]:
        """The date/time value map associated with this interval."""
        return self._dtv_map

    @property
    def kwargs(self):
        """Returns the keyword argument associated with this interval."""
        return self._kwargs

    def __eq__(self, other) -> bool:
        if isinstance(other, Interval):
            return self._dtv_map == other._dtv_map
        return False

    def __call__(self, start: arrow.Arrow | datetime.datetime | str) -> arrow.Arrow:
        """Returns a new date/time based on the given date/time, shifted by this interval.

        Parameters:
            start: the date/time to be shifted by this interval

        Returns:
            a new date/time based on the given date/time, shifted by this interval
        """
        start_ = start if isinstance(start, arrow.Arrow) else arrow.get(start)
        return start_.shift(**self._kwargs)

    def __repr__(self) -> str:
        return (
            "Interval({"
            + ", ".join([f"{k}: {v}" for k, v in self._dtv_map.items()])
            + "})"
        )

    def __str__(self) -> str:
        return ", ".join([f"{v} {k.arrow_name}" for k, v in self._dtv_map.items()])


#: A 1-day interval.
ONE_DAY = Interval({DateTimeUnit.DAY: 1})

#: A 1-month interval.
ONE_MONTH = Interval({DateTimeUnit.MONTH: 1})

#: A 1-year interval.
ONE_YEAR = Interval({DateTimeUnit.YEAR: 1})

#: Type alias for input to interval factory.
IntervalSource = Interval | str


class UnparsableIntervalOmobonoError(UnparsableObjectOmobonoError[IntervalSource]):
    """Exception signalling inability to parse an interval from a string."""

    def __init__(self, source: IntervalSource) -> None:
        """Initializes this exception.

        Parameters:
            source: the source that could not be parsed
        """
        super().__init__(source, "interval")


class _IntervalFactory(
    Factory[IntervalSource, Interval, UnparsableIntervalOmobonoError]
):
    """Produces an interval from the given source.

    Examples:

        >>> factory = _IntervalFactory()
        >>> interval_factory(Interval("interval 1 day"))  # interval source returns given source
        Interval({_DTPart.DAY: 1})

        >>> interval_factory("interval 1 day")  # string source parsed as interval
        Interval({_DTPart.DAY: 1})
    """

    def __init__(self):
        super().__init__(UnparsableIntervalOmobonoError)

    def _produce(self, a: IntervalSource) -> Interval:
        match a:
            case Interval():
                return a
            case str():
                return Interval(a)


interval_factory = _IntervalFactory()
