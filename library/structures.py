from __future__ import annotations

from collections import deque


class Stack:
    def __init__(self) -> None:
        self._items: list[str] = []

    def push(self, item: str) -> None:
        self._items.append(item)

    def pop(self) -> str:
        if self.is_empty():
            raise IndexError("La pila esta vacia.")
        return self._items.pop()

    def peek(self) -> str:
        if self.is_empty():
            raise IndexError("La pila esta vacia.")
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def to_list(self) -> list[str]:
        return list(reversed(self._items))


class Queue:
    def __init__(self) -> None:
        self._items: deque[str] = deque()

    def enqueue(self, item: str) -> None:
        self._items.append(item)

    def dequeue(self) -> str:
        if self.is_empty():
            raise IndexError("La cola esta vacia.")
        return self._items.popleft()

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)

    def to_list(self) -> list[str]:
        return list(self._items)


class FixedArray:
    def __init__(self, size: int) -> None:
        self._items: list[str | None] = [None] * size

    def set_item(self, index: int, value: str) -> None:
        self._validate_index(index)
        self._items[index] = value

    def get_item(self, index: int) -> str | None:
        self._validate_index(index)
        return self._items[index]

    def values(self) -> list[str]:
        return [value for value in self._items if value is not None]

    def _validate_index(self, index: int) -> None:
        if index < 0 or index >= len(self._items):
            raise IndexError("Indice fuera de rango.")
