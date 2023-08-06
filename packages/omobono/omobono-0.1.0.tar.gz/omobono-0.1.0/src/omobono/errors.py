"""Types for expressing Omobono exceptions.

(c) 2023 WPEngine, Inc.  All rights reserved.
"""

from typing import Any, Generic, Optional, TypeVar
import collections.abc as cabc
import pandas
import pint


#: A generic type variable.
A = TypeVar("A")


# === base exceptions


class OmobonoError(Exception):
    """Base class for Omobono exceptions."""

    def __init__(self, message: str) -> None:
        """Initializes this exception.

        Parameters:
            message: a message describing this exception
        """
        self._message = message

    @property
    def message(self) -> str:
        """A message describing this exception."""
        return self._message


class BadInputDataError(OmobonoError):
    """Exception signalling that the input into Omobono was malformed."""

    def __init__(self, msg: str) -> None:
        """Initializes this exception.

        Parameters:
            msg: a message describing the failure
        """
        super().__init__(msg)


class UnparsableObjectOmobonoError(Generic[A], OmobonoError):
    """Exception signalling the inability to parse a source as an object."""

    def __init__(self, source: A, name: Optional[str] = None) -> None:
        """Initializes this exception.

        Parameters:
            source: the source that could not be parsed
            name: the name of the
        """
        super(OmobonoError, self).__init__(
            f'could not parse "{source}"'
            f'{f" as a(n) {name}" if name is not None else ""}'
        )
        self._source = source

    @property
    def source(self) -> A:
        """The source that could not be parsed."""
        return self._source


# === library exceptions


class BadInputDataframeTypeError(BadInputDataError):
    """Exception signalling a column in an input dataframe contained unexpected types."""

    def __init__(
        self,
        col: str,
        expected_type: type,
        unexpected_types: cabc.Iterable[type],
    ) -> None:
        """Initializes this exception.

        Parameters:
            col: the name of the column containing unexpected types
            expected_type: the expected type
            unexpected_types: the unexpected types found
        """
        super().__init__(
            f"""column {col} of the input dataframe"""
            f""" should only contain instances of {expected_type}"""
            f""" -- actual types included ({", ".join(unexpected_types)})"""
        )


class BadParamOmobonoError(OmobonoError):
    """Exception signalling a value was inappropriate as a parameter to a function."""

    def __init__(
        self,
        param_value: Any,
        param_name: Optional[str] = None,
        msg: Optional[str] = None,
    ) -> None:
        """Initializes this exception.

        Parameters:
            param_value: the inappropriate value
            param_name: the name of the parameter that was the target of the given value (optional)
            msg: an (optional) message describing the failure
        """
        super().__init__(
            msg
            if msg is not None
            else (
                "bad parameter value"
                f"""{"" if param_name is None else f" for {param_name}"}"""
            )
        )
        self._param_value = param_value
        self._param_name = param_name

    @property
    def param_name(self) -> Optional[str]:
        """The name of the parameter that was the target of the given value, if provided."""
        return self._param_name

    @property
    def param_value(self) -> Any:
        """The inappropriate value."""
        return self._param_value


class IncompleteInputDataframeError(BadInputDataError):
    """Exception signalling an expected column in an input dataframe was missing."""

    def __init__(self, expected: str, df: pandas.DataFrame) -> None:
        """Initializes this exception.

        Parameters:
            expected: the expected field not found in the input
            df: the input
        """
        super().__init__(
            f"""no column named "{expected}" in the input dataframe"""
            f""" --- actual columns: {", ".join(list(df))}"""
        )


class UomDimensionalityOmobonoError(OmobonoError):
    """Exception signalling a mismatch between expected and actual unit dimensionality."""

    def __init__(
        self, *, expected: pint.util.UnitsContainer, actual_uom: pint.Unit
    ) -> None:
        """Initializes this exception.

        Parameters:
            expected: the expected dimensionality
            actual_uom: the mismatched unit of measure
        """
        super().__init__(
            "unit of measure dimensionality mismatch: "
            f"""actual unit "{actual_uom}" with dimensionality {actual_uom.dimensionality} """
            f"""does not match expected dimensionality {expected}"""
        )
        self._expected = expected
        self._actual_uom = actual_uom

    @property
    def actual(self) -> pint.util.UnitsContainer:
        """The actual dimensionality."""
        return self._actual_uom.dimensionality

    @property
    def actual_uom(self) -> pint.util.UnitsContainer:
        """A unit of measure with the actual dimensionality."""
        return self._actual_uom

    @property
    def expected(self) -> pint.util.UnitsContainer:
        """The actual dimensionality."""
        return self._expected
