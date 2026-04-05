from __future__ import annotations

from datetime import date

from library.models import Book, Loan, User
from library.structures import FixedArray, Queue, Stack


class LibrarySystem:
    def __init__(self) -> None:
        self.books: list[Book] = []
        self.users: list[User] = []
        self.loans: list[Loan] = []
        self.history = Stack()
        self.categories = FixedArray(6)
        self.waitlists: dict[str, Queue] = {}
        self._load_default_categories()
        self._load_sample_data()

    def _load_default_categories(self) -> None:
        base_categories = [
            "Ciencia",
            "Literatura",
            "Historia",
            "Tecnologia",
            "Arte",
            "Infantil",
        ]
        for index, category in enumerate(base_categories):
            self.categories.set_item(index, category)

    def _load_sample_data(self) -> None:
        self.register_book("9780001", "Estructuras de Datos", "Luis Perez", "Tecnologia", 3)
        self.register_book("9780002", "Introduccion a Python", "Ana Rojas", "Tecnologia", 2)
        self.register_book("9780003", "Cien Anos de Soledad", "Gabriel Garcia Marquez", "Literatura", 4)
        self.register_user("U001", "Maria Gomez", "maria@correo.com")
        self.register_user("U002", "Juan Torres", "juan@correo.com")

    def register_book(
        self,
        isbn: str,
        title: str,
        author: str,
        category: str,
        total_copies: int,
    ) -> str:
        if self.find_book_by_isbn(isbn):
            return "Ya existe un libro con ese ISBN."
        if total_copies <= 0:
            return "La cantidad de ejemplares debe ser mayor que cero."

        book = Book(
            isbn=isbn,
            title=title,
            author=author,
            category=category,
            total_copies=total_copies,
            available_copies=total_copies,
        )
        self.books.append(book)
        self.waitlists[isbn] = Queue()
        self.history.push(f"Libro registrado: {title} ({isbn})")
        return "Libro registrado correctamente."

    def register_user(self, user_id: str, name: str, email: str) -> str:
        if self.find_user_by_id(user_id):
            return "Ya existe un usuario con ese identificador."
        user = User(user_id=user_id, name=name, email=email)
        self.users.append(user)
        self.history.push(f"Usuario registrado: {name} ({user_id})")
        return "Usuario registrado correctamente."

    def search_books(self, query: str) -> list[Book]:
        normalized = query.strip().lower()
        return [
            book
            for book in self.books
            if normalized in book.title.lower()
            or normalized in book.author.lower()
            or normalized in book.isbn.lower()
        ]

    def search_users(self, query: str) -> list[User]:
        normalized = query.strip().lower()
        return [
            user
            for user in self.users
            if normalized in user.user_id.lower()
            or normalized in user.name.lower()
            or normalized in user.email.lower()
        ]

    def lend_book(self, isbn: str, user_id: str) -> str:
        book = self.find_book_by_isbn(isbn)
        user = self.find_user_by_id(user_id)
        if not book:
            return "El libro no existe."
        if not user:
            return "El usuario no existe."
        if self._user_has_active_loan(isbn, user_id):
            return "El usuario ya tiene este libro prestado."

        if book.is_available():
            book.available_copies -= 1
            self.loans.append(Loan(book_isbn=isbn, user_id=user_id, loan_date=date.today()))
            self.history.push(f"Prestamo registrado: {isbn} para {user_id}")
            return "Prestamo realizado correctamente."

        self.waitlists[isbn].enqueue(user_id)
        book.waitlist_size = len(self.waitlists[isbn])
        self.history.push(f"Reserva en cola: {isbn} para {user_id}")
        return "No hay ejemplares disponibles. El usuario fue agregado a la cola de reserva."

    def return_book(self, isbn: str, user_id: str) -> str:
        active_loan = next(
            (
                loan
                for loan in self.loans
                if loan.book_isbn == isbn and loan.user_id == user_id and not loan.returned
            ),
            None,
        )
        if not active_loan:
            return "No existe un prestamo activo con esos datos."

        active_loan.returned = True
        book = self.find_book_by_isbn(isbn)
        if book is None:
            return "El libro asociado no existe."

        if not self.waitlists[isbn].is_empty():
            next_user_id = self.waitlists[isbn].dequeue()
            self.loans.append(Loan(book_isbn=isbn, user_id=next_user_id, loan_date=date.today()))
            self.history.push(f"Prestamo automatico por reserva: {isbn} para {next_user_id}")
        else:
            book.available_copies += 1

        book.waitlist_size = len(self.waitlists[isbn])
        self.history.push(f"Devolucion registrada: {isbn} por {user_id}")
        return "Devolucion procesada correctamente."

    def list_active_loans(self) -> list[Loan]:
        return [loan for loan in self.loans if not loan.returned]

    def list_user_active_loans(self, user_id: str) -> list[Loan]:
        return [loan for loan in self.loans if loan.user_id == user_id and not loan.returned]

    def get_waitlist(self, isbn: str) -> list[str]:
        queue = self.waitlists.get(isbn)
        if queue is None:
            return []
        return queue.to_list()

    def get_recent_history(self) -> list[str]:
        return self.history.to_list()

    def find_book_by_isbn(self, isbn: str) -> Book | None:
        return next((book for book in self.books if book.isbn == isbn), None)

    def find_user_by_id(self, user_id: str) -> User | None:
        return next((user for user in self.users if user.user_id == user_id), None)

    def _user_has_active_loan(self, isbn: str, user_id: str) -> bool:
        return any(
            loan.book_isbn == isbn and loan.user_id == user_id and not loan.returned
            for loan in self.loans
        )
