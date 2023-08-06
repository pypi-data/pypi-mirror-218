from threading import Lock
from typing import Any, Type


class Registry:
    # The constructor method initializes an instance of the Registry class.
    def __init__(self):
        # The registry dictionary stores the mapping of Builder types to their corresponding struct types.
        self.registry = dict()

        # We use a Lock object to ensure that updates to the registry are thread-safe.
        # This is necessary when you have multiple threads that might be trying to update the registry at the same time.
        self.registry_lock = Lock()

    # The register_type method is used to register a mapping from a builder type to a struct type.
    def register_type(self, builder_type: Type[Any], struct_type: Type[Any]) -> Any:
        # We use a context manager (the "with" statement) to ensure that the lock is properly acquired and released,
        # even if an error occurs within the block of code.
        with self.registry_lock:
            # This check ensures that the provided struct_type is indeed a class.
            if not isinstance(struct_type, type):
                raise ValueError(
                    f"Invalid type: {type(struct_type).__name__}. Expected a class."
                )

            # If struct_type is valid, we add the mapping from builder_type to struct_type to our registry dictionary.
            self.registry[builder_type] = struct_type

            # Create and return a new instance of the builder_type.
            return builder_type()

    # This method is a convenience function for registering a builder and struct instance,
    # rather than their types.
    def register(self, builder_proto: Any, struct_proto: Any) -> Any:
        return self.register_type(type(builder_proto), type(struct_proto))

    # This method retrieves the struct type associated with a given builder type.
    def get_builder_struct_type(self, builder_type: Type[Any]) -> Type[Any]:
        with self.registry_lock:
            # Get the struct_type from the registry dictionary, or None if it does not exist.
            struct_type = self.registry.get(builder_type)
            return struct_type

    # This method creates a new instance of the struct type associated with a given builder type.
    def new_builder_struct(self, builder_type: Type[Any]) -> Any:
        struct_type = self.get_builder_struct_type(builder_type)
        if struct_type is None:
            return None

        # Create and return a new instance of the struct_type.
        new_struct = struct_type()
        return new_struct
