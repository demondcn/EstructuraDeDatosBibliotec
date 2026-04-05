import unittest

from library.system import LibrarySystem


class LibrarySystemTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.system = LibrarySystem()

    def test_register_book(self) -> None:
        message = self.system.register_book(
            "9780004", "Algoritmos Aplicados", "Carla Diaz", "Tecnologia", 2
        )
        self.assertEqual(message, "Libro registrado correctamente.")
        self.assertIsNotNone(self.system.find_book_by_isbn("9780004"))

    def test_register_user(self) -> None:
        message = self.system.register_user("U003", "Laura Ruiz", "laura@correo.com")
        self.assertEqual(message, "Usuario registrado correctamente.")
        self.assertIsNotNone(self.system.find_user_by_id("U003"))

    def test_search_books(self) -> None:
        results = self.system.search_books("python")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].isbn, "9780002")

    def test_lend_book_when_available(self) -> None:
        message = self.system.lend_book("9780001", "U001")
        self.assertEqual(message, "Prestamo realizado correctamente.")
        book = self.system.find_book_by_isbn("9780001")
        self.assertEqual(book.available_copies, 2)
        self.assertEqual(len(self.system.list_active_loans()), 1)

    def test_waitlist_when_no_stock(self) -> None:
        self.system.register_book("9781000", "Redes", "Autor X", "Tecnologia", 1)
        self.system.register_user("U003", "Laura Ruiz", "laura@correo.com")
        self.system.register_user("U004", "Pedro Lara", "pedro@correo.com")
        self.system.lend_book("9781000", "U003")
        message = self.system.lend_book("9781000", "U004")
        self.assertIn("cola de reserva", message.lower())
        self.assertEqual(self.system.get_waitlist("9781000"), ["U004"])

    def test_return_assigns_reserved_book(self) -> None:
        self.system.register_book("9781001", "Base de Datos", "Autor Y", "Tecnologia", 1)
        self.system.register_user("U003", "Laura Ruiz", "laura@correo.com")
        self.system.register_user("U004", "Pedro Lara", "pedro@correo.com")
        self.system.lend_book("9781001", "U003")
        self.system.lend_book("9781001", "U004")

        message = self.system.return_book("9781001", "U003")
        self.assertEqual(message, "Devolucion procesada correctamente.")
        active_loans = self.system.list_active_loans()
        self.assertEqual(len(active_loans), 1)
        self.assertEqual(active_loans[0].user_id, "U004")


if __name__ == "__main__":
    unittest.main()
