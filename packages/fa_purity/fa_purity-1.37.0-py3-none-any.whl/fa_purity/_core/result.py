from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from fa_purity._core.coproduct import (
    Coproduct,
    CoproductFactory,
    CoproductTransform,
)
from typing import (
    Callable,
    Generic,
    Optional,
    Type,
    TypeVar,
    Union,
)

_S = TypeVar("_S")
_F = TypeVar("_F")
_T = TypeVar("_T")


@dataclass(frozen=True)
class _Result(Generic[_S, _F]):
    value: Coproduct[_S, _F]


@dataclass(frozen=True)
class PureResult(Generic[_S, _F]):
    "Equivalent to Coproduct[_S, _F], but designed to handle explicit errors"
    _inner: _Result[_S, _F]

    @staticmethod
    def success(
        val: _S, _type: Optional[Type[_F]] = None
    ) -> PureResult[_S, _F]:
        item: Coproduct[_S, _F] = Coproduct.inl(val)
        return PureResult(_Result(item))

    @staticmethod
    def failure(
        val: _F, _type: Optional[Type[_S]] = None
    ) -> PureResult[_S, _F]:
        item: Coproduct[_S, _F] = Coproduct.inr(val)
        return PureResult(_Result(item))

    def map(self, function: Callable[[_S], _T]) -> PureResult[_T, _F]:
        factory: CoproductFactory[_T, _F] = CoproductFactory()
        val = self._inner.value.map(
            lambda s: factory.inl(function(s)),
            lambda f: factory.inr(f),
        )
        return PureResult(_Result(val))

    def alt(self, function: Callable[[_F], _T]) -> PureResult[_S, _T]:
        factory: CoproductFactory[_S, _T] = CoproductFactory()
        val = self._inner.value.map(
            lambda s: factory.inl(s),
            lambda f: factory.inr(function(f)),
        )
        return PureResult(_Result(val))

    def to_coproduct(self) -> Coproduct[_S, _F]:
        return self._inner.value

    def bind(
        self, function: Callable[[_S], PureResult[_T, _F]]
    ) -> PureResult[_T, _F]:
        factory: CoproductFactory[_T, _F] = CoproductFactory()
        val = self._inner.value.map(
            lambda s: function(s).to_coproduct(),
            lambda f: factory.inr(f),
        )
        return PureResult(_Result(val))

    def lash(
        self, function: Callable[[_F], PureResult[_S, _T]]
    ) -> PureResult[_S, _T]:
        factory: CoproductFactory[_S, _T] = CoproductFactory()
        val = self._inner.value.map(
            lambda s: factory.inl(s),
            lambda f: function(f).to_coproduct(),
        )
        return PureResult(_Result(val))

    def swap(self) -> PureResult[_F, _S]:
        val = CoproductTransform(self._inner.value).swap()
        return PureResult(_Result(val))

    def apply(
        self, wrapped: PureResult[Callable[[_S], _T], _F]
    ) -> PureResult[_T, _F]:
        return wrapped.bind(lambda f: self.map(f))

    def cop_value_or(self, default: _T) -> Coproduct[_S, _T]:
        factory: CoproductFactory[_S, _T] = CoproductFactory()
        val = self._inner.value.map(
            lambda s: factory.inl(s),
            lambda _: factory.inr(default),
        )
        return val

    def cop_or_else_call(
        self, function: Callable[[], _T]
    ) -> Coproduct[_S, _T]:
        factory: CoproductFactory[_S, _T] = CoproductFactory()
        val = self._inner.value.map(
            lambda s: factory.inl(s),
            lambda _: factory.inr(function()),
        )
        return val

    def value_or(self, default: _T) -> Union[_S, _T]:
        return CoproductTransform(self.cop_value_or(default)).to_union()

    def or_else_call(self, function: Callable[[], _T]) -> Union[_S, _T]:
        return CoproductTransform(self.cop_or_else_call(function)).to_union()

    def to_union(self) -> Union[_S, _F]:
        return CoproductTransform(self._inner.value).to_union()
