from typing import Any, Sequence

class MissingCommand(TypeError): ...  # noqa: N818

class BackendProxy:
    backend_module: str
    backend_object: str | None
    backend: Any
    def __init__(self, backend_module: str, backend_obj: str | None) -> None: ...
    def __call__(self, name: str, *args: Any, **kwargs: Any) -> Any: ...
    def _exit(self) -> None: ...
    def _optional_commands(self) -> dict[str, bool]: ...

def run(argv: Sequence[str]) -> int: ...
def read_line(fd: int = 0) -> bytearray: ...
def flush() -> None: ...
