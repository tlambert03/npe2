from __future__ import annotations

from typing import AbstractSet, Any, Callable, Iterable, Mapping, NamedTuple

import pydantic
from pydantic import fields
from pydantic.types import conlist as pydantic_conlist

PYDANTIC_V2 = pydantic.__version__.startswith("2")


try:
    Undefined = fields.Undefined
except AttributeError:

    class _UndefinedType:
        """Singleton class to represent an undefined value."""

        def __repr__(self) -> str:
            return "PydanticUndefined"

        def __copy__(self) -> _UndefinedType:
            return self

        def __reduce__(self) -> str:
            return "Undefined"

        def __deepcopy__(self, _: Any) -> _UndefinedType:
            return self

    Undefined = _UndefinedType()


class FieldInfo(NamedTuple):
    annotation: Any = None
    default: Any = Undefined
    default_factory: Callable[[], Any] | None = None
    alias: str | None = None
    alias_priority: int | None = None
    title: str | None = None
    description: str | None = None
    examples: list[Any] | None = None
    exclude: AbstractSet[int | str] | Mapping[int | str, Any] | Any = None
    include: AbstractSet[int | str] | Mapping[int | str, Any] | Any = None
    metadata: list[Any] = []
    repr: bool = True
    discriminator: str | None = None
    json_schema_extra: dict[str, Any] | None = None
    # currently only used on dataclasses
    init_var: bool | None = None
    kw_only: bool | None = None
    validate_default: bool | None = None

    @property
    def required(self) -> bool:
        return self.default is Undefined and self.default_factory is None

    def get_default(self) -> Any:
        return self.default if self.default_factory is None else self.default_factory()


if PYDANTIC_V2:
    FROZEN = {"frozen": True}

    def iter_fields(cls: pydantic.BaseModel) -> Iterable[tuple[str, FieldInfo]]:
        for name, field_info in cls.model_fields.items():
            _field_info = FieldInfo(
                annotation=field_info.annotation,
                default=field_info.default,
                default_factory=field_info.default_factory,
                alias=field_info.alias,
                alias_priority=field_info.alias_priority,
                title=field_info.title,
                description=field_info.description,
                examples=field_info.examples,
                exclude=field_info.exclude,
                include=field_info.include,
                metadata=field_info.metadata,
                repr=field_info.repr,
                discriminator=field_info.discriminator,
                json_schema_extra=field_info.json_schema_extra,
            )
            yield name, _field_info

    def conlist(
        item_type: type,
        *,
        min_items: int = None,
        max_items: int = None,
        unique_items: bool = None,  # !!!
    ):
        return pydantic_conlist(item_type, min_length=min_items, max_length=max_items)

else:
    FROZEN = {"allow_mutation": False}
    conlist = pydantic_conlist

    def list_like(v: Any) -> bool:
        return isinstance(v, (list, tuple, set, frozenset))

    def iter_fields(cls: pydantic.BaseModel) -> Iterable[tuple[str, FieldInfo]]:
        for name, model_field in cls.__fields__.items():
            field_info = model_field.field_info
            _field_info = FieldInfo(
                annotation=model_field.outer_type_ or model_field.type_,
                default=model_field.default,
                default_factory=model_field.default_factory,
                alias=model_field.alias,
                # alias_priority=model_field.alias_priority,
                title=field_info.title,
                description=field_info.description,
                # examples=field_info.examples,
                exclude=field_info.exclude,
                include=field_info.include,
                # metadata=field_info.metadata,
                repr=field_info.repr,
                discriminator=field_info.discriminator,
                # json_schema_extra=field_info.json_schema_extra,
            )

            yield name, _field_info
