from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass
class User:
    user_id: str
    name: str
    email: str


@dataclass
class Loan:
    book_isbn: str
    user_id: str
    loan_date: date
    returned: bool = False


@dataclass
class Book:
    isbn: str
    title: str
    author: str
    category: str
    total_copies: int
    available_copies: int
    waitlist_size: int = field(default=0)

    def is_available(self) -> bool:
        return self.available_copies > 0
