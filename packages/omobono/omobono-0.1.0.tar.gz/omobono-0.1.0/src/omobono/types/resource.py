"""Provides an enumeration of resources.

(c) 2023 WPEngine, Inc.  All rights reserved.
"""

import collections
import enum
import pint
from src.omobono.errors import UnparsableObjectOmobonoError
from src.omobono.types.factory import Factory
from src.omobono.types.omobono_unit_registry import OUR


#: NamedTuple wrapper for resource values.
_ResourceValue = collections.namedtuple("_ResourceValue", ["name", "normal_uom"])


class Resource(enum.Enum):
    """An enumeration of resources."""

    #: Bandwidth consumed.
    BANDWIDTH = _ResourceValue("bandwidth", OUR.Gibit)

    #: Storage consumed.
    STORAGE = _ResourceValue("storage", OUR.GiB)

    #: Count of site visitors.
    VISITOR_COUNT = _ResourceValue("visitor count", OUR.kcount)

    @property
    def name(self) -> str:
        """The name of this resource."""
        return self.value.name

    @property
    def normal_uom(self) -> pint.Unit:
        """ "The normalized unit of measure for this resource."""
        return self.value.normal_uom

    def normalize(self, q: pint.Quantity) -> pint.Quantity:
        """Converts the given quantity to the normal unit of measure for this resource.

        Parameters:
            q: the quantity to normalize

        Returns:
            the given quantity, expressed in the normal unit of measure for this resource
        """
        return q.to(self.value.normal_uom)

    def __str__(self):
        return self.name


#: Type alias for input to resource factory.
ResourceSource = Resource | str


class UnparsableResourceOmobonoError(UnparsableObjectOmobonoError[ResourceSource]):
    """Exception signalling inability to parse a resource from a string."""

    def __init__(self, source: ResourceSource) -> None:
        """Initializes this exception.

        Parameters:
            source: the source that could not be parsed
        """
        super().__init__(source, "resource")


class _ResourceFactory(
    Factory[ResourceSource, Resource, UnparsableResourceOmobonoError]
):
    """Produces a resource from the given source.

    Examples:

        >>> factory = _ResourceFactory()
        >>> factory(Resource.STORAGE)  # resource source returns given source
        <Resource.STORAGE: _ResourceValue(name='storage', normal_uom=<Unit('gibibyte')>)>

        >>> factory("storage")  # string source parsed as resource name
        <Resource.STORAGE: _ResourceValue(name='storage', normal_uom=<Unit('gibibyte')>)>
    """

    def __init__(self):
        super().__init__(UnparsableObjectOmobonoError)

    def _produce(self, a: ResourceSource) -> Resource:
        match a:
            case Resource():
                return a
            case str():
                s_ = a.casefold()
                for r in Resource:
                    if r.name.casefold() == s_:
                        return r


resource_factory = _ResourceFactory()
