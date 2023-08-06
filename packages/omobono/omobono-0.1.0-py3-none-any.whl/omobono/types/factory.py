from typing import Callable, Generic, TypeVar
import abc
from src.omobono.errors import UnparsableObjectOmobonoError


A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C", bound=UnparsableObjectOmobonoError)


class Factory(Generic[A, B, C], abc.ABC):
    """A factory.

    Type Variables:
        A: the type of source
        B: the type of output
        C: the type of exception in case of failure
    """

    def __init__(self, ex: Callable[[A], C]) -> None:
        self._ex = ex

    @property
    def ex(self) -> Callable[[A], C]:
        return self._ex

    @abc.abstractmethod
    def _produce(self, a: A) -> B:
        raise NotImplementedError("factory subclasses must implement _produce")

    def _post_process(self, b: B) -> B:
        return b

    def __call__(self, a: A) -> B:
        try:
            b = self._produce(a)
            if b is not None:
                return self._post_process(b)
        except Exception as e:
            raise self.ex(a) from e
        raise self.ex(a)
