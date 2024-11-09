from collections.abc import Callable
from typing import TypeVar

from running_app.inject import injector

# Define a type variable T, which can be any type.
T = TypeVar("T")


def on(dependency_class: type[T]) -> Callable[[], T]:
    """Controller에서 DI injecting용 함수입니다.

    Retrieves an instance of the specified dependency class from the injector.
    """
    return lambda: injector.get(dependency_class)
