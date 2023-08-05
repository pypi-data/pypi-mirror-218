from typing import TypeVar, Tuple, Callable, Union

DIMENSION = TypeVar("DIMENSION", bound=Tuple[int, int])

POSITION = TypeVar("POSITION", bound=Tuple[int, int])

CB_RESIZE = TypeVar("CB_RESIZE", bound=Callable[[None], None])

MOVE_DIRECTION = TypeVar("MOVE_DIRECTION", bound="Cursor.Direction")

ERASE_DIRECTION = TypeVar("ERASE_DIRECTION", bound=Union["Cursor.Direction", "Screen.Portion"])
