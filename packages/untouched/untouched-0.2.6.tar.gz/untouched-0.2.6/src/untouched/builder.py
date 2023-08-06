from __future__ import annotations

import collections.abc
from typing import Any, Dict, Optional, TypeVar

from .registry import Registry

# any subclass of Builder will be able to use the methods defined in Builder, or the methods defined in its subclasses
T = TypeVar('T', bound='Builder')


class Builder:
    """
    The Builder class is the base class for all builders.
    It provides the base functionality to manage a dictionary that will represent a structure.
    """

    def __init__(self):
        self.builder_map = {}

    def set_value(self: T, name: str, v: Any) -> T:
        new_builder = type(self)()
        new_builder.builder_map = self.builder_map.copy()
        new_builder.builder_map[name] = v
        return new_builder

    def get_builder_map(self) -> Dict:
        return self.builder_map


def delete_value(builder: Builder, name: str) -> Builder:
    """
    Creates a new Builder with the specified attribute removed.
    """
    new_builder = type(builder)()  # Create a new instance of the same type as builder, to avoid inheritance issues
    new_builder.builder_map = builder.get_builder_map().copy()
    new_builder.builder_map.pop(name, None)
    return new_builder


def extend(builder: Builder, name: str, vs: Any) -> Builder:
    """
    Creates a new Builder with the specified attribute extended with the provided iterable.
    """
    if vs is None:
        return builder

    new_builder = type(builder)()  # Create a new instance of the same type as builder, to avoid inheritance issues
    new_builder.builder_map = builder.get_builder_map().copy()

    if not isinstance(vs, collections.abc.Iterable):
        raise TypeError("Expected an iterable value.")

    new_builder.builder_map[name] = list(vs)
    return new_builder


def get_value(builder: Builder, name: str) -> Optional[Any]:
    """
    Returns the value for the specified attribute from the immutable's map.
    """
    return builder.get_builder_map().get(name)


def get_map(builder: Builder) -> Dict[str, Any]:
    """
    Returns a copy of the builders map.
    """
    return builder.get_builder_map().copy()


def get_struct(builder: Builder, registry: Registry) -> Any:
    """
    Converts the builder's map into the corresponding struct object.
    """
    builder_type = type(builder)
    struct_type = registry.get_builder_struct_type(builder_type)
    if struct_type is None:
        return None

    new_struct = registry.new_builder_struct(builder_type)
    struct_dict = builder.get_builder_map()
    for name, value in struct_dict.items():
        setattr(new_struct, name, value)
    return new_struct

