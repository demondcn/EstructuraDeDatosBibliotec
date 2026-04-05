from __future__ import annotations

from library.system import LibrarySystem


class LibraryCLI:
    def __init__(self) -> None:
        self.system = LibrarySystem()

    def run(self) -> None:
        while True:
            self._show_header()
            option = input("Seleccione una opcion: ").strip()
            print()

            actions = {
                "1": self._register_book,
                "2": self._register_user,
                "3": self._search_books,
                "4": self._lend_book,
                "5": self._return_book,
                "6": self._show_books,
                "7": self._show_users,
                "8": self._show_loans,
                "9": self._show_history,
                "10": self._show_categories,
                "0": self._exit,
            }

            action = actions.get(option)
            if action is None:
                print("Opcion invalida.\n")
                continue
            action()

    def _show_header(self) -> None:
        print("=" * 60)
        print("SISTEMA DE GESTION DE BIBLIOTECA")
        print("=" * 60)
        print("1. Registrar libro")
        print("2. Registrar usuario")
        print("3. Buscar libro")
        print("4. Registrar prestamo")
        print("5. Registrar devolucion")
        print("6. Ver catalogo")
        print("7. Ver usuarios")
        print("8. Ver prestamos activos")
        print("9. Ver historial")
        print("10. Ver categorias")
        print("0. Salir")

    def _register_book(self) -> None:
        print("Registro de libro")
        isbn = input("ISBN: ").strip()
        title = input("Titulo: ").strip()
        author = input("Autor: ").strip()
        category = input("Categoria: ").strip()
        copies_raw = input("Numero de ejemplares: ").strip()
        if not copies_raw.isdigit():
            print("Debe ingresar un numero entero positivo.\n")
            return
        copies = int(copies_raw)
        print(self.system.register_book(isbn, title, author, category, copies))
        print()

    def _register_user(self) -> None:
        print("Registro de usuario")
        user_id = input("ID usuario: ").strip()
        name = input("Nombre: ").strip()
        email = input("Correo: ").strip()
        print(self.system.register_user(user_id, name, email))
        print()

    def _search_books(self) -> None:
        query = input("Ingrese titulo, autor o ISBN: ").strip()
        results = self.system.search_books(query)
        if not results:
            print("No se encontraron coincidencias.\n")
            return
        for book in results:
            self._print_book(book)
        print()

    def _lend_book(self) -> None:
        isbn = input("ISBN del libro: ").strip()
        user_id = input("ID del usuario: ").strip()
        print(self.system.lend_book(isbn, user_id))
        print()

    def _return_book(self) -> None:
        isbn = input("ISBN del libro: ").strip()
        user_id = input("ID del usuario: ").strip()
        print(self.system.return_book(isbn, user_id))
        print()

    def _show_books(self) -> None:
        for book in self.system.books:
            self._print_book(book)
            waitlist = self.system.get_waitlist(book.isbn)
            if waitlist:
                print(f"  Cola de reserva: {', '.join(waitlist)}")
        print()

    def _show_users(self) -> None:
        for user in self.system.users:
            print(f"{user.user_id} | {user.name} | {user.email}")
        print()

    def _show_loans(self) -> None:
        loans = self.system.list_active_loans()
        if not loans:
            print("No hay prestamos activos.\n")
            return
        for loan in loans:
            print(f"Libro {loan.book_isbn} | Usuario {loan.user_id} | Fecha {loan.loan_date}")
        print()

    def _show_history(self) -> None:
        history = self.system.get_recent_history()
        if not history:
            print("No hay acciones registradas.\n")
            return
        for item in history:
            print(item)
        print()

    def _show_categories(self) -> None:
        for index, category in enumerate(self.system.categories.values(), start=1):
            print(f"{index}. {category}")
        print()

    def _exit(self) -> None:
        print("Cierre del sistema.")
        raise SystemExit

    @staticmethod
    def _print_book(book) -> None:
        print(
            f"{book.isbn} | {book.title} | {book.author} | "
            f"Categoria: {book.category} | Disponibles: {book.available_copies}/{book.total_copies}"
        )
