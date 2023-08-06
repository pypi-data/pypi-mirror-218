# Untouched

https://pypi.org/project/untouched/

https://github.com/DAMACANER/untouched


Carbon copy of https://github.com/lann/builder for making a Python NoSQL query builder.

Installing:

```python
poetry add untouched
```

Example:

```python
from src.untouched.builder import Builder, get_struct, T
from src.untouched.registry import Registry
from typing import Optional
from pprint import pprint

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


    # Register the builder-struct pair
    registry.register(UserBuilder(), User())
    user_builder = UserBuilder().name("caner").age(25).name("caner2")  # Build a user
    user = user_builder.get_builder_map()
    pprint(user.__dict__)  # Print the user struct's attributes


# Output:
# 
# {'age': 25, 'name': 'caner2'}
```

Thanks a lot to Lann for the original builder package, this is wonderful.

Not a perfect copy of the library, yet it works! Which is, what python is right? It is fast enough, and it works.