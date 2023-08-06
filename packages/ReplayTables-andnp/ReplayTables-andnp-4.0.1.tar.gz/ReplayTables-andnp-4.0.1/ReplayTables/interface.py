import numpy as np
from typing import cast, Any, NewType, NamedTuple, Protocol, TypeVar

IDX = NewType('IDX', int)
IDXs = NewType('IDXs', np.ndarray)
EID = NewType('EID', int)
EIDs = NewType('EIDs', np.ndarray)

class Addable(Protocol):
    def __add__(self, other: Any, /) -> Any:
        ...

class Ring(Protocol):
    def __add__(self, other: Any, /) -> Any:
        ...

    def __mul__(self, other: Any, /) -> Any:
        ...

    def __rmul__(self, other: Any, /) -> Any:
        ...

    def __pow__(self, other: Any, /) -> Any:
        ...

class Timestep(NamedTuple):
    x: Any | None
    a: Any
    r: Ring | None
    gamma: Ring
    terminal: Any

class TaggedTimestep(NamedTuple):
    x: Any
    a: Any
    r: Ring | None
    gamma: Ring
    terminal: Any
    eid: EID

class Batch(NamedTuple):
    x: np.ndarray
    a: np.ndarray
    r: np.ndarray
    gamma: np.ndarray
    terminal: np.ndarray
    eid: EIDs
    xp: np.ndarray

T = TypeVar('T', bound=Timestep)

def expect_tagged(t: Timestep) -> TaggedTimestep:
    assert hasattr(t, 'eid')
    return cast(Any, t)
