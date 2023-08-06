from pydantic import BaseModel
from typing import Callable, Any, Union
from typing_extensions import Self


class Dependency:
    def __init__(self: Self, func: Callable[...,]) -> None:
        self.func = func


class DependencySchema(BaseModel):
    func: Callable[..., Any]
    deps: list["DependencySchema"]

    @classmethod
    def from_func(
        cls: type[Self],
        func: Callable[..., Any],
        visited: Union[Callable[..., Any], None],
        ancestors: Union[Callable[..., Any], None],
    ) -> Self:
        if visited is None:
            visited = []
        if ancestors is None:
            ancestors = []

        deps: list[Self] = _resolve_deps(func, visited, ancestors)

        return cls(func=func, deps=deps)


def _resolve_deps(
    func: Callable[..., Any],
    visited: list[Callable[..., Any]],
    ancestors: list[Callable[..., Any]],
) -> list[DependencySchema]:
    ...
