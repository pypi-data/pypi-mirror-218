from typing import Any, Optional, Protocol, runtime_checkable


@runtime_checkable
class ValuesetProvider(Protocol):
    def get_valueset(self, name: str, scope: Optional[str]) -> dict[str, Any]:
        ...


@runtime_checkable
class ValuesetScopeProvider(ValuesetProvider, Protocol):
    def get_valuesets_in_scope(self, scope: str) -> list[dict[str, Any]]:
        ...
