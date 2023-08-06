from typing import Any, Callable


def convert(from_value: Any, to_value: Any) -> Any:
    return type(to_value)(from_value)


def forEach(s: Any, f: Callable[[Any], None]) -> None:
    if not isinstance(s, (list, tuple)):
        raise ValueError(f"Invalid type: {type(s).__name__}. Expected list or tuple.")

    for i in s:
        f(i)
