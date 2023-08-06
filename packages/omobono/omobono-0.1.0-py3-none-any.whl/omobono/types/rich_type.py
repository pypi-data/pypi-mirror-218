"""Provides a wrapper to augment operations on instances of type.

Copyright 2023 WPEngine, Inc.  All rights reserved.
"""

from typing import Final, Generic, Optional, TypeVar
import functools
import inspect
import logging


#: The logger for this file.
_LOGGER: Final[logging.Logger] = logging.getLogger(__name__)

#: A generic type.
A = TypeVar("A")

#: A generic type.
B = TypeVar("B")


class RichType(Generic[A]):
    """Wrapper for a type that provides some useful functions.

    If no type is passed to the initializer, the effective type is treated as
    "Any".
    """

    def __init__(self, typ: Optional[type[A]]):
        """Creates a new type wrapper."""
        self.__typ = typ
        _LOGGER.debug("wrapping type %s", typ)

    def accepts(self, b: type[B] | B) -> bool:
        """Indicates whether the wrapped type accepts the given type or variable.

        The effective type to be checked is either the given type, or the type
        of the given variable.

        Parameters:
            b: either a type or a variable

        Returns:
            True, if the wrapped type is in the MRO of the effective given type;
            False, otherwise.

        Examples:

        >>> class Animal:
        ...     pass
        >>> class Dog(Animal):
        ...     pass
        >>> class Retriever(Dog):
        ...     pass
        >>> the_type(Dog).accepts(Animal)
        False

        >>> the_type(Dog).accepts(Dog)
        True

        >>> the_type(Dog).accepts(Retriever)
        True

        >>> the_type(Dog).accepts(float)
        False

        >>> the_type(None).accepts(Dog)
        True

        >>> the_type(Dog).accepts(Animal())
        False

        >>> the_type(Dog).accepts(Dog())
        True

        >>> the_type(Dog).accepts(Retriever())
        True

        >>> the_type(Dog).accepts(1.0)
        False
        """
        if self.__typ is None:
            return True
        b_typ = b if isinstance(b, type) else type(b)
        _LOGGER.debug("effective type to test against %s is %s", self.__typ, b_typ)
        return self.__typ in inspect.getmro(b_typ)


#: A convenient constant for the "any" type.
any_type: RichType = RichType(None)


@functools.cache
def the_type(typ: Optional[type[A]]) -> RichType[A]:
    """Returns a type wrapper for the given type."""
    return RichType[A](typ) if typ is not None else any_type


def the_type_of(a: A) -> RichType[A]:
    """Returns a type wrapper for the type of the given parameter."""
    return the_type(type(a))
