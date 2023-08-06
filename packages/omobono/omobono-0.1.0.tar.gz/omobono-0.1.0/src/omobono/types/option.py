"""Support for monadic optional values.

Instances of the abstract type Option are concretely instances of either Absent or Present.

Copyright 2023 WPEngine, Inc.  All rights reserved.
"""

from typing import Any, Callable, final, Final, Generic, Optional, TypeVar
import abc
import logging
from src.omobono.types.rich_type import RichType, any_type, the_type

#: The logger for this file.
_LOGGER: Final[logging.Logger] = logging.getLogger(__name__)

#: The type of value help by an option.
A_co = TypeVar("A_co", covariant=True)

#: A generic type.
A = TypeVar("A")

#: A generic type.
B = TypeVar("B")


class Option(Generic[A_co], abc.ABC):
    """A monadic optional value."""

    @staticmethod
    @final
    def absent() -> "Option[Any]":
        """Returns an absent value."""
        return Absent()

    @staticmethod
    @final
    def from_optional(a: Optional[A]) -> "Option[A]":
        """Converts the given standard library optional to a monadic option.

        Parameters:
            a: the value to convert

        Returns:
            the given value wrapped in a Present instance, if the value is not None;
            Absent, otherwise

        Examples:

            >>> from typing import Optional
            >>> i: Optional[int] = 3
            >>> Option.from_optional(i)
            Present(3)

            >>> i: Optional[int] = None
            >>> Option.from_optional(i)
            Absent
        """
        return Option.absent() if a is None else Option.present(a)

    @staticmethod
    @final
    def present(a: A, type_parameter: Optional[type[A]] = None) -> "Option[A]":
        """Returns a present value.

        The type parameter can be inferred or made explicit.

        Parameters:
            a: the value to be wrapped in a Present instance
            type_parameter: the type parameter to the value to be returned

        Returns:
            the given value, wrapped in a Present instance

        Examples:

            >>> Option.present(1)
            Present(1)

            >>> Option.present(1, int)
            Present(1)

            >>> Option.present(1, float)
            Present(1.0)
        """
        return (
            Present(a, the_type(type_parameter))
            if type_parameter is None
            else Present(type_parameter(a), the_type(type_parameter))
        )

    def __init__(self, type_parameter: RichType[A_co]):
        """Initializes a new option.

        Parameters:
            type_parameter: the type parameter for this option
        """
        self.__type_parameter = type_parameter

    def type_parameter(self) -> RichType[A_co]:
        """The type parameter for this option."""
        return self.__type_parameter

    @final
    def contains(self, a: A_co) -> bool:  # type: ignore[misc]
        """Indicates whether this option contains the given value.

        Parameters:
            a: the value to be tested

        Returns:
            True, if this option is present and contains the given value;
            False, otherwise

        Raises:
            TypeError, if this option is not Present or Absent

        Examples:

            >>> Option.present(1).contains(1)
            True

            >>> Option.present(1).contains(2)
            False

            >>> Option.absent().contains(1)
            False
        """
        match self:
            case Present(value):
                return a == value
            case Absent():
                return False
            case _:
                raise TypeError(f"""unknown Option subclass {type(self).__name__}""")

    @final
    def exists(self, p: Callable[[A_co], bool]) -> bool:
        """Indicates whether this option is present and matches the given predicate.

        Parameters:
            p: the predicate to test the option, if present

        Returns:
            True, if this option is present and its value matches the given predicate;
            False, otherwise

        Raises:
            TypeError, if this option is not Present or Absent

        Examples:

            >>> Option.present(1).exists(lambda a: a > 0)
            True

            >>> Option.present(-1).exists(lambda a: a > 0)
            False

            >>> Option.absent().exists(lambda a: a > 0)
            False
        """
        match self:
            case Present(value):
                return p(value)
            case Absent():
                return False
            case _:
                raise TypeError(f"""unknown Option subclass {type(self).__name__}""")

    @final
    def filter(self, p: Callable[[A_co], bool]) -> "Option[A_co]":
        """Returns this option if it contains a value that matches the given predicate.

        Parameters:
            p: the predicate to apply to the present value (if it exists)

        Returns:
            this option if it is present and its value matches the given predicate;
            Absent, otherwise

        Raises:
            TypeError, if this option is not Present or Absent

        Examples:

            >>> Option.present(1).filter(lambda a: a > 0)
            Present(1)

            >>> Option.present(-1).filter(lambda a: a > 0)
            Absent

            >>> Option.absent().filter(lambda a: a > 0)
            Absent
        """
        match self:
            case Present(value):
                return self if p(value) else Option.absent()
            case Absent():
                return self
            case _:
                raise TypeError(f"""unknown Option subclass {type(self).__name__}""")

    @final
    def flatmap(self, f: Callable[[A_co], "Option[B]"]) -> "Option[B]":
        """Maps this option through the given function and flattens the result.

        Parameters:
            f: the function

        Returns:
            The flattened result of mapping this option through the given function.

        Raises:
            TypeError, if this option is not Present or Absent

        Examples:

            >>> Option.present(1).flatmap(lambda a: Option.present(a * 2))
            Present(2)

            >>> Option.present(1).flatmap(lambda _: Option.absent())
            Absent

            >>> Option.absent().flatmap(lambda a: Option.present(a * 2))
            Absent
        """
        return self.map(f).flatten()

    @final
    def flatten(self) -> "Option[Any]":
        """Flattens this nested option.

        Returns:
            Present(ffa.value) if this option is present and ffa.value is an option;
            Absent, if this option is absent

        Raises:
            TypeError, if this option is not Present or Absent, or if this is an unnested present option

        Examples:

            >>> Option.present(Option.present(1)).flatten()
            Present(1)

            >>> Option.present(Option.absent()).flatten()
            Absent

            >>> Option.absent().flatten()
            Absent

            >>> Option.present(1).flatten()
            Traceback (most recent call last):
              ...
            TypeError: cannot flatten a flat present option
        """
        match self:
            case Present(value):
                match value:
                    case Present(_) | Absent():
                        return value
                    case _:
                        raise TypeError("""cannot flatten a flat present option""")
            case Absent():
                return self
            case _:
                raise TypeError(f"""unknown Option subclass {type(self).__name__}""")

    @final
    def fold(self, f: Callable[[B, A_co], B], zero: B) -> B:
        """Iteratively applies the given function to this option.

        Parameters:
            f: the function to be applied
            zero: the starting value of the iteration

        Returns:
            f(zero, a), if the given option was Present(a);
            zero, otherwise

        Raises:
            TypeError, if this option is not Present or Absent

        Examples:

            >>> Option.present(1).fold(lambda acc, i: acc + i, 0)
            1

            >>> Option.absent().fold(lambda acc, i: acc + i, 0)
            0
        """
        match self:
            case Present(value):
                return f(zero, value)
            case Absent():
                return zero
            case _:
                raise TypeError(f"""unknown Option subclass {type(self).__name__}""")

    @final
    def forall(self, p: Callable[[A_co], bool]) -> bool:
        """Indicates whether this option is absent or the present value matches the given predicate.

        Parameters:
            p: the predicate to test the value, if present

        Returns:
            True, if this value is absent, or the present value matches the given predicate;
            False, otherwise

        Raises:
            TypeError, if this option is not Present or Absent

        Examples:

            >>> Option.present(1).forall(lambda a: a > 0)
            True

            >>> Option.present(-1).forall(lambda a: a > 0)
            False

            >>> Option.absent().forall(lambda a: a > 0)
            True
        """
        match self:
            case Present(value):
                return p(value)
            case Absent():
                return True
            case _:
                raise TypeError(f"""unknown Option subclass {type(self).__name__}""")

    @final
    def foreach(self, f: Callable[[A_co], Any]) -> None:
        """Runs the given computation on this option, if present.

        Parameters:
            f: the computation to run

        Returns:
            nothing

        Raises:
            TypeError, if this option is not Present or Absent

        Examples:

            >>> Option.present(1).foreach(lambda a: print(a))
            1

            >>> Option.absent().foreach(lambda a: print(a)) is None
            True
        """
        match self:
            case Present(value):
                f(value)
            case Absent():
                pass
            case _:
                raise TypeError(f"""unknown Option subclass {type(self).__name__}""")

    @final
    def get_or_else(self, default: A_co) -> A_co:  # type: ignore[misc]
        """Returns this option, if present, or the given default otherwise.

        Parameters:
            default: the value to be returned if this value is absent

        Returns:
            this value, if present, or the given default otherwise

        Raises:
            TypeError, if this option is not Present or Absent

        Examples:

            >>> Option.present(1).get_or_else(2)
            1

            >>> Option.absent().get_or_else(2)
            2
        """
        match self:
            case Present(value):
                return value
            case Absent():
                return default
            case _:
                raise TypeError(f"""unknown Option subclass {type(self).__name__}""")

    @final
    def is_absent(self) -> bool:
        """Indicates whether this option does not contain a value.

        Returns:
            True, if this value is absent;
            False, otherwise

        Raises:
            TypeError, if this option is not Present or Absent

        Examples:

            >>> Option.present(1).is_absent()
            False

            >>> Option.absent().is_absent()
            True
        """
        match self:
            case Present(_):
                return False
            case Absent():
                return True
            case _:
                raise TypeError(f"""unknown Option subclass {type(self).__name__}""")

    @final
    def is_present(self) -> bool:
        """Indicates whether this option contains a value.

        Returns:
            True, if this value is present;
            False, otherwise

        Raises:
            TypeError, if this option is not Present or Absent

        Examples:

            >>> Option.present(1).is_present()
            True

            >>> Option.absent().is_present()
            False
        """
        match self:
            case Present(_):
                return True
            case Absent():
                return False
            case _:
                raise TypeError(f"""unknown Option subclass {type(self).__name__}""")

    @final
    def map(self, f: Callable[[A_co], B]) -> "Option[B]":
        """Lifts the given function into Option.

        Parameters:
            f: the function to be lifted

        Returns:
            Present(f(a)), if the given option was Present(a);
            Absent, if the given option was Absent

        Raises:
            TypeError, if this option is not Present or Absent

        Examples:

            >>> Option.present(1).map(lambda i: i * 2)
            Present(2)

            >>> Option.absent().map(lambda i: i * 2)
            Absent
        """
        match self:
            case Present(value):
                return Option.present(f(value))
            case Absent():
                return self
            case _:
                raise TypeError(f"""unknown Option subclass {type(self).__name__}""")

    @final
    def or_else(self, alternative: "Option[A_co]") -> "Option[A_co]":
        """Returns this option if present, or the alternative otherwise.

        Parameters:
            alternative: the option to be returned if this option is absent

        Returns:
            this option if present, or the alternative otherwise

        Raises:
            TypeError, if this option is not Present or Absent

        Examples:

            >>> Option.present(1).or_else(Option.present(2))
            Present(1)

            >>> Option.absent().or_else(Option.present(2))
            Present(2)
        """
        match self:
            case Present(_):
                return self
            case Absent():
                return alternative
            case _:
                raise TypeError(f"""unknown Option subclass {type(self).__name__}""")

    @final
    def to_optional(self) -> Optional[A_co]:
        """Converts this option to a standard library optional.

        Returns:
            the present value, or None if this option is absent

        Raises:
            TypeError, if this option is not Present or Absent

        Examples:

            >>> Option.present(1).to_optional()
            1

            >>> Option.absent().to_optional() is None
            True
        """
        match self:
            case Present(value):
                return value
            case Absent():
                return None
            case _:
                raise TypeError(f"""unknown Option subclass {type(self).__name__}""")

    @final
    def __eq__(self, other):
        match self, other:
            case Present(value), Present(other_value):
                return value == other_value
            case Absent(), Absent():
                return True
            case (Absent(), Present(_)) | (Present(_), Absent()):
                return False
            case _:
                raise TypeError(
                    f"""unknown Option subclass {type(self).__name__} and/or {type(other).__name__}"""
                )

    @final
    def __iter__(self):
        match self:
            case Present(value):
                return iter([value])
            case Absent():
                return iter([])
            case _:
                raise TypeError(f"""unknown Option subclass {type(self).__name__}""")


@final
class Absent(Option[A_co]):
    """An optional, absent value."""

    def __new__(cls, *args):
        """Creates a new absent value.

        This method returns a singleton instance of this class.
        """
        if not hasattr(cls, "_instance"):
            cls._instance = super(Absent, cls).__new__(cls)
        return getattr(cls, "_instance")

    def __init__(self):
        """Initializes a new absent value."""
        super().__init__(any_type)

    def __str__(self):
        return "Absent"

    def __repr__(self):
        return str(self)


@final
class Present(Option[A_co], Generic[A_co]):
    """An optional, present value."""

    #: Allows position based structural matching.
    __match_args__ = ("value",)

    def __init__(self, value: A_co, type_parameter: RichType[A_co]):
        """Initializes a new present value.

        Although this can be called directly, in most cases it may be easier to
        call ``Option.present``, which will infer the type parameter and/or
        coerce the value as needed.

        Parameters:
            value: the present value
            type_parameter: the type parameter governing this present value
        """
        super().__init__(type_parameter)
        self.__value = value

    @property
    def value(self) -> A_co:
        """The present value."""
        return self.__value

    def __str__(self):
        return str(self.__value)

    def __repr__(self):
        return f"Present({self.__value})"
