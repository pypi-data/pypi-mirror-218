from __future__ import annotations

import collections.abc
from pprint import pprint
from typing import Any, Dict, Optional, TypeVar
from registry import Registry


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
    new_builder = type(builder)()  # Create a new instance of the same type as untouched, to avoid inheritance issues
    new_builder.builder_map = builder.get_builder_map().copy()
    new_builder.builder_map.pop(name, None)
    return new_builder


def extend(builder: Builder, name: str, vs: Any) -> Builder:
    """
    Creates a new Builder with the specified attribute extended with the provided iterable.
    """
    if vs is None:
        return builder

    new_builder = type(builder)()  # Create a new instance of the same type as untouched, to avoid inheritance issues
    new_builder.builder_map = builder.get_builder_map().copy()

    if not isinstance(vs, collections.abc.Iterable):
        raise TypeError("Expected an iterable value.")

    new_builder.builder_map[name] = list(vs)
    return new_builder


def get_value(builder: Builder, name: str) -> Optional[Any]:
    """
    Returns the value for the specified attribute from the untouched's map.
    """
    return builder.get_builder_map().get(name)


def get_map(builder: Builder) -> Dict[str, Any]:
    """
    Returns a copy of the untouched's map.
    """
    return builder.get_builder_map().copy()


def get_struct(builder: Builder) -> Any:
    """
    Converts the untouched's map into the corresponding struct object.
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


empty_builder = Builder()

registry = Registry()  # Initialize the registry

if __name__ == "__main__":
    class UserBuilder(Builder):
        """
        The UserBuilder class inherits from Builder and provides specific methods to set the 'name' and 'age' attributes.
        """

        def __init__(self):
            super().__init__()

        def name(self, val: str) -> 'UserBuilder':
            """
            Creates a new UserBuilder with the 'name' attribute set to the provided value.
            """
            return self.set_value("name", val)

        def age(self, val: int) -> 'UserBuilder':
            """
            Creates a new UserBuilder with the 'age' attribute set to the provided value.
            """
            return self.set_value("age", val)


    class User:
        """
        The User class represents the structure that the UserBuilder will build.
        """

        def __init__(self, name: Optional[str] = None, age: Optional[int] = None):
            self.name = name
            self.age = age


    # Register the untouched-struct pair
    registry.register(UserBuilder(), User())
    user_builder = UserBuilder().name("caner").age(25).name("caner2")  # Build a user
    user = get_struct(user_builder)  # Convert the untouched to a struct
    pprint(user.__dict__)  # Print the user struct's attributes
